#!/usr/bin/env python3
"""
数据库升级脚本
添加 read_at 字段到 notification 表
"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.main import app, db
from datetime import datetime

def upgrade_database():
    """升级数据库schema"""
    with app.app_context():
        try:
            # 检查是否已经有 read_at 字段
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('notification')]
            
            if 'read_at' not in columns:
                print("🔧 正在添加 read_at 字段到 notification 表...")
                
                # 添加 read_at 字段
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE notification ADD COLUMN read_at DATETIME'))
                
                print("✅ read_at 字段添加成功！")
            else:
                print("✅ read_at 字段已存在，无需升级")
                
            # 确保所有表都存在
            print("🔧 检查并创建缺失的表...")
            db.create_all()
            print("✅ 数据库检查完成！")
            
        except Exception as e:
            print(f"❌ 数据库升级失败: {e}")
            return False
            
    return True

if __name__ == "__main__":
    print("🚀 开始数据库升级...")
    if upgrade_database():
        print("🎉 数据库升级完成！")
    else:
        print("💥 数据库升级失败！")
        sys.exit(1)
