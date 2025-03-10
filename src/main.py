import asyncio
from db_agent import DBQueryAgent, MySQLConnector
from config import DB_CONFIG, DASHSCOPE_CONFIG

async def main():
    # 初始化数据库连接器
    db_connector = MySQLConnector(DB_CONFIG["mysql"])
    
    # 初始化查询智能体
    agent = DBQueryAgent(db_connector, DASHSCOPE_CONFIG["api_key"], DASHSCOPE_CONFIG["base_url"])
    
    while True:
        try:
            # 获取用户输入
            user_query = input("请输入您的查询 (输入 'quit' 退出): ")
            
            if user_query.lower() == 'quit':
                break
                
            # 处理查询
            response = await agent.process_query(user_query)  # 始终使用 await
            print("\n回答:", response, "\n")
            
        except Exception as e:
            print(f"发生错误: {str(e)}")
            import traceback
            print(traceback.format_exc())  # 添加详细的错误追踪

if __name__ == "__main__":
    asyncio.run(main()) 