# DBMindAI 🔍

<div align="center">

![DBMindAI Logo](https://img.shields.io/badge/DBMindAI-智能数据库助手-blue)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.7+-yellow)
![MySQL](https://img.shields.io/badge/MySQL-Support-orange)

</div>

[English](README.md) | 简体中文

## 项目简介 📖

DBMindAI 是一款基于人工智能的数据库助手。

核心能力:
🔹 将AI助手连接到数据库
• 只需用日常语句描述需求，自动生成精准查询数据，将数据分析后，以自然语言的方式返回给用户。

## 主要特性 ✨

- 🤖 **自然语言转SQL**: 支持将日常用语转换为准确的SQL查询语句
- 🎯 **智能理解**: 基于先进的AI模型，准确理解用户意图
- 📊 **数据库结构感知**: 自动识别和理解数据库表结构
- 🛡️ **安全防护**: 内置SQL注入防护机制
- 🔄 **实时响应**: 支持流式输出，提供即时反馈
- 📝 **智能解释**: 自动将查询结果转化为易懂的自然语言描述

## 技术栈 🛠️

- Python 3.7+
- MySQL
- OpenAI API / DashScope API
- asyncio 异步编程
- MySQL Connector

## 快速开始 🚀

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

在 `config.py` 中配置您的数据库连接信息：

```python
DB_CONFIG = {
    "mysql": {
        "host": "your_host",
        "user": "your_username",
        "password": "your_password",
        "database": "your_database"
    }
}
```

### 3. 配置API密钥

在 `config.py` 中设置您的API密钥：

```python
BASE_URL = "your_base_url"
API_KEY = "your_api_key"
```

### 4. 配置模型

在 `db_agent.py` 中设置您的模型：

```python
model = "your_model"
```

### 5. 运行程序

```bash
python src/main.py
```

## 使用示例 📝

1. **有多少个用户**
   ```
   回答: 目前系统中共有93位用户。
   ```

2. **是25年的注册用户多 还是24年的**
   ```
   回答: 根据查询结果，2024年的注册用户数量（55）比2025年（38）更多。因此，注册用户更多的年份是2024年。
   ```

## 项目结构 📁

```
src/
├── main.py          # 主程序入口
├── db_agent.py      # 主要功能模块
└── config.py        # 数据库配置文件
```

## 贡献指南 🤝

欢迎提交 Pull Request 或创建 Issue！

## 开源协议 📄

本项目采用 MIT 协议开源，详情请参见 [LICENSE](LICENSE) 文件。

## 联系方式 📮

如有任何问题或建议，欢迎通过以下方式联系：

- 提交 Issue
- 发送邮件至: [zhouhaos@outlook.com]

---

<div align="center">

**DBMindAI** - 让数据查询更简单

</div> 