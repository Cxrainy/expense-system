"""
报销管理系统 - 核心应用模块
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 全局变量
db = SQLAlchemy()

def create_app(config_object=None):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 加载配置
    if config_object:
        app.config.from_object(config_object)
    else:
        from .config import get_config
        app.config.from_object(get_config())
    
    # 初始化扩展
    db.init_app(app)
    
    # 注册蓝图
    from .main import app as main_app
    return main_app

__version__ = '1.0.0'
