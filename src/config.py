from typing import Dict

DB_CONFIG = {
    "mysql": {
        "host": "localhost",
        "user": "user",
        "password": "password",
        "database": "database"
    }
}

DASHSCOPE_CONFIG = {
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "api_key": "your-api-key-here"
}

# 尝试从本地配置文件导入实际配置
try:
    from config_local import DB_CONFIG as LOCAL_DB_CONFIG, DASHSCOPE_CONFIG as LOCAL_DASHSCOPE_CONFIG
    DB_CONFIG.update(LOCAL_DB_CONFIG)
    DASHSCOPE_CONFIG.update(LOCAL_DASHSCOPE_CONFIG)
except ImportError:
    print("未找到本地配置文件 config_local.py，使用默认配置") 