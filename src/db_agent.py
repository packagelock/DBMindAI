from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import openai
from datetime import datetime
import mysql.connector
import re


class DatabaseConnector(ABC):
    @abstractmethod
    async def execute_query(self, query: str) -> Any:
        pass

class MySQLConnector(DatabaseConnector):
    def __init__(self, config: Dict[str, str]):
        self.config = config  # 保存配置以便重连
        self.connection = None
        self._connect()
        self.schema_cache = None  # 添加schema缓存
    
    def _connect(self):
        try:
            if self.connection and self.connection.is_connected():
                return
            self.connection = mysql.connector.connect(**self.config)
        except mysql.connector.Error as e:
            raise Exception(f"数据库连接失败: {str(e)}")
    
    async def execute_query(self, query: str) -> Any:
        try:
            self._connect()  # 确保连接可用
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as e:
            self.connection.close()
            raise Exception(f"查询执行失败: {str(e)}")

    async def get_database_schema(self) -> Dict:
        """获取数据库结构信息"""
        if self.schema_cache:
            return self.schema_cache
            
        schema = {}
        try:
            self._connect()
            cursor = self.connection.cursor()
            
            # 获取所有表
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                # 获取表结构
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                schema[table_name] = {
                    'columns': [
                        {
                            'name': col[0],
                            'type': col[1],
                            'null': col[2],
                            'key': col[3],
                            'default': col[4],
                            'extra': col[5]
                        }
                        for col in columns
                    ]
                }
            
            cursor.close()
            self.schema_cache = schema
            return schema
            
        except mysql.connector.Error as e:
            raise Exception(f"获取数据库结构失败: {str(e)}")


class DBQueryAgent:
    def __init__(self, db_connector: DatabaseConnector, api_key: str, base_url: str):
        self.db_connector = db_connector
        self.api_key = api_key
        self.base_url = base_url
        self.llm = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        # 添加会话历史存储
        self.conversation_history = []
        self.max_history_length = 10  # 保存最近10条对话记录
        
    async def process_query(self, user_query: str) -> str:
        # 首先判断是否是简单的问候或闲聊
        greetings = ['你好', '您好', 'hi', 'hello', '嗨']
        if user_query.lower() in greetings:
            response = "你好！我是你的数据库助手。我可以帮你查询数据，也可以和你聊天。需要查询数据时，请告诉我你想知道什么，比如'查询总用户数'或'显示用户表结构'。"
            self._update_conversation_history("user", user_query)
            self._update_conversation_history("assistant", response)
            return response
            
        # 获取数据库结构
        try:
            schema = await self.db_connector.get_database_schema()
        except Exception as e:
            return f"未知错误: 获取数据库结构失败 - {str(e)}"
        
        # 构建系统提示，包含数据库结构信息
        system_prompt = f"""以下是数据库的表结构:{self._format_schema(schema)}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        try:
            # 1. 将自然语言转换为SQL或获取聊天回复
            result = self._generate_sql(user_query, messages)
            
            # 如果返回的是元组，说明是聊天回复
            if isinstance(result, tuple):
                return result[1]  # 直接返回聊天回复
            
            # 检查SQL语句的基本语法
            sql_query = result
            if not self._validate_sql_syntax(sql_query):
                return f"未知错误: SQL语法错误 - {sql_query}"
                
            # 执行SQL查询
            results = await self.db_connector.execute_query(sql_query)
            response = self._generate_response(results, user_query)
            return response
            
        except Exception as e:
            return f"未知错误: {str(e)}"
            
    def _validate_sql_syntax(self, sql: str) -> bool:
        """
        简单验证SQL语句的基本语法
        """
        # 移除空行和前后空格
        sql = '\n'.join(line.strip() for line in sql.split('\n') if line.strip())
        
        # 检查是否以分号结尾
        if not sql.endswith(';'):
            return False
            
        # 检查基本的SQL语法结构
        sql_upper = sql.upper()
        first_word = sql_upper.split()[0] if sql_upper.split() else ''
        if first_word not in ['SELECT', 'SHOW', 'DESC', 'DESCRIBE']:
            return False
            
        # 检查括号是否匹配
        if sql.count('(') != sql.count(')'):
            return False
            
        # 检查引号是否匹配
        if sql.count("'") % 2 != 0 or sql.count('"') % 2 != 0:
            return False
            
        return True
    
    def _format_schema(self, schema: Dict) -> str:
        """格式化数据库结构信息"""
        formatted = []
        for table, info in schema.items():
            formatted.append(f"\n表名: {table}")
            formatted.append("字段:")
            for column in info['columns']:
                formatted.append(f"- {column['name']}: {column['type']}")
        return "\n".join(formatted)
    
    def _generate_sql(self, user_query: str, messages: list) -> str | tuple[bool, str]:
        # 添加历史对话上下文
        full_messages = messages.copy()
        if self.conversation_history:
            # 在system prompt之后，插入历史对话记录
            full_messages[1:1] = self.conversation_history
        
        # 添加更明确的SQL生成提示
        full_messages.append({
            "role": "system",
            "content": """
            现在,请仔细分析用户的查询,并生成相应的SQL语句。
            如果用户的查询不需要SQL查询(例如打招呼或闲聊),请以'CHAT:'开头回复一个友好的回应。
            如果需要生成SQL查询:
            1. 请使用标准SQL语法
            2. 只生成SELECT、SHOW、DESC或DESCRIBE语句
            3. 确保语句以分号结尾
            4. 使用```sql 或 ` 包裹SQL语句
            5. 尽量写出最优和最简洁的查询
            6. 避免使用复杂的子查询和JOIN,除非必要
            7. 注意使用适当的WHERE条件和排序
            8. 对于模糊查询,使用LIKE语句
            请基于上述数据库结构生成查询。
            """
        })
        
        response = self.llm.chat.completions.create(
            model="qwq-32b",
            messages=full_messages,
            stream=True
        )
        
        # 收集流式响应
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                
        response_text = full_response.strip()
        
        # 检查是否是聊天回复
        if response_text.upper().startswith('CHAT:'):
            return (True, response_text[5:].strip())
            
        # 提取SQL语句
        sql_match = re.search(r'```sql\n?(.*?)\n?```|`(.*?)`', response_text, re.DOTALL)
        if sql_match:
            sql = sql_match.group(1) or sql_match.group(2)
            sql = sql.strip()
            
            # 移除SQL注释
            sql = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
            sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
            sql = '\n'.join(line.strip() for line in sql.split('\n') if line.strip())
        else:
            # 如果包含SELECT等关键字，尝试直接使用响应文本
            if any(keyword in response_text.upper() for keyword in ['SELECT', 'SHOW', 'DESC', 'DESCRIBE']):
                sql = response_text.strip()
            else:
                return (True, "抱歉，我没能理解您的查询。请尝试更具体的描述，例如'查询总用户数'或'显示用户表结构'。")
            
        # 确保SQL语句以分号结尾
        if not sql.endswith(';'):
            sql += ';'
            
        # 简单的SQL注入防护
        if any(dangerous_word in sql.upper() for dangerous_word in ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'TRUNCATE']):
            return (True, "抱歉，我只能执行查询操作。")
            
        return sql
    
    # ------------------------------------------------------------------------
    # 响应生成与对话管理
    # ------------------------------------------------------------------------
    def _generate_response(self, query_results: Any, original_query: str) -> str:
        results_str = str(query_results)
        prompt = f"""
        基于以下查询结果，生成一个自然、易懂的响应。
        原始查询：{original_query}
        查询结果：{results_str}
        """
        
        response = self.llm.chat.completions.create(
            model="qwq-32b",
            messages=[
                {"role": "system", "content": "你是一个数据分析师，负责将查询结果转换为易懂的自然语言描述。"},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        
        # 收集流式响应
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                
        # 更新对话历史
        self._update_conversation_history("user", original_query)
        self._update_conversation_history("assistant", full_response.strip())
        
        return full_response.strip()
        
    def _update_conversation_history(self, role: str, content: str):
        """更新对话历史"""
        self.conversation_history.append({"role": role, "content": content})
        # 保持历史记录在指定长度内
        if len(self.conversation_history) > self.max_history_length * 2:  # *2是因为每轮对话包含用户和助手两条消息
            self.conversation_history = self.conversation_history[-self.max_history_length * 2:]
            
    def clear_conversation_history(self):
        """清空对话历史"""
        self.conversation_history = [] 