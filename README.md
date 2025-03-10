# DBMindAI 🔍

<div align="center">

![DBMindAI Logo](https://img.shields.io/badge/DBMindAI-Intelligent%20Database%20Assistant-blue)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.7+-yellow)
![MySQL](https://img.shields.io/badge/MySQL-Support-orange)

</div>

English | [简体中文](README.zh-CN.md)

## Introduction 📖

DBMindAI is an AI-powered database assistant.

Core Capability:
🔹 Connects AI assistant to databases
• Simply describe your needs in natural language, and it automatically generates precise queries, analyzes the data, and returns results in natural language.

## Key Features ✨

- 🤖 **Natural Language to SQL**: Converts everyday language into accurate SQL queries
- 🎯 **Intelligent Understanding**: Accurately comprehends user intent using advanced AI models
- 📊 **Database Structure Awareness**: Automatically identifies and understands database schema
- 🛡️ **Security Protection**: Built-in SQL injection protection mechanism
- 🔄 **Real-time Response**: Supports streaming output for immediate feedback
- 📝 **Smart Interpretation**: Automatically transforms query results into easily understandable natural language

## Tech Stack 🛠️

- Python 3.7+
- MySQL
- OpenAI API / DashScope API
- asyncio Asynchronous Programming
- MySQL Connector

## Quick Start 🚀

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

Configure your database connection in `config.py`:

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

### 3. Configure API Key

Set your API key in `config.py`:

```python
BASE_URL = "your_base_url"
API_KEY = "your_api_key"
```

### 4. Configure Model

Set your model in `db_agent.py`:

```python
model = "your_model"
```

### 5. Run the Program

```bash
python src/main.py
```

## Usage Examples 📝

1. **How many users are there?**
   ```
   Answer: There are currently 93 users in the system.
   ```

2. **Are there more registered users in 2025 or 2024?**
   ```
   Answer: Based on the query results, 2024 has more registered users (55) compared to 2025 (38). Therefore, 2024 has more registered users.
   ```

## Project Structure 📁

```
src/
├── main.py          # Main program entry
├── db_agent.py      # Core functionality module
└── config.py        # Database configuration file
```

## Contributing 🤝

Pull requests and issues are welcome!

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact 📮

For any questions or suggestions, feel free to:

- Submit an Issue
- Send an email to: [zhouhaos@outlook.com]

---

<div align="center">

**DBMindAI** - Making Database Queries Simpler

</div> 