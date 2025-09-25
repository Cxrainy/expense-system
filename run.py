#!/usr/bin/env python3
"""
报销管理系统启动入口
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.main import app

if __name__ == "__main__":
    # 开发环境启动
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    
    print(f"🚀 启动报销管理系统...")
    print(f"📍 访问地址: http://localhost:{port}")
    print(f"🔧 调试模式: {'开启' if debug else '关闭'}")
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )
