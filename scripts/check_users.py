#!/usr/bin/env python3
"""
检查用户账户状态脚本
"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.main import app, db, User

def check_all_users():
    """检查所有用户状态"""
    with app.app_context():
        users = User.query.all()
        print("📋 当前系统用户详情:")
        print("=" * 60)
        
        for user in users:
            has_password = "✅ 有密码" if user.password else "❌ 无密码"
            role_icon = "👑" if user.role == "admin" else "👤"
            
            print(f"{role_icon} ID: {user.id}")
            print(f"   用户名: {user.username}")
            print(f"   邮箱: {user.email}")
            print(f"   角色: {user.role}")
            print(f"   密码状态: {has_password}")
            if user.password:
                print(f"   密码哈希: {user.password[:30]}...")
            print("-" * 60)

if __name__ == "__main__":
    check_all_users()
