#!/usr/bin/env python3
"""
创建管理员账户脚本
修复管理员登录问题
"""
import sys
import os
import getpass
from werkzeug.security import generate_password_hash

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.main import app, db, User

def create_admin_user():
    """创建管理员用户"""
    with app.app_context():
        try:
            # 检查是否已存在管理员
            admin_user = User.query.filter_by(role='admin').first()
            
            if admin_user:
                print(f"✅ 管理员账户已存在: {admin_user.username} ({admin_user.email})")
                choice = input("是否要重置管理员密码? (y/N): ").lower()
                if choice != 'y':
                    return True
                    
                # 重置密码
                print("\n🔧 重置管理员密码...")
                password = getpass.getpass("请输入新密码: ")
                confirm_password = getpass.getpass("请确认密码: ")
                
                if password != confirm_password:
                    print("❌ 密码不匹配！")
                    return False
                    
                admin_user.password = generate_password_hash(password)
                db.session.commit()
                print(f"✅ 管理员密码重置成功！用户名: {admin_user.username}")
                
            else:
                # 创建新管理员
                print("🔧 创建新的管理员账户...")
                
                username = input("请输入管理员用户名 (默认: admin): ").strip() or "admin"
                email = input("请输入管理员邮箱 (默认: admin@expense.com): ").strip() or "admin@expense.com"
                
                # 检查用户名和邮箱是否已存在
                if User.query.filter_by(username=username).first():
                    print(f"❌ 用户名 '{username}' 已存在！")
                    return False
                    
                if User.query.filter_by(email=email).first():
                    print(f"❌ 邮箱 '{email}' 已存在！")
                    return False
                
                password = getpass.getpass("请输入密码: ")
                confirm_password = getpass.getpass("请确认密码: ")
                
                if password != confirm_password:
                    print("❌ 密码不匹配！")
                    return False
                
                if len(password) < 6:
                    print("❌ 密码长度不能少于6位！")
                    return False
                
                # 创建管理员用户
                admin_user = User(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    role='admin'
                )
                
                db.session.add(admin_user)
                db.session.commit()
                
                print(f"✅ 管理员账户创建成功！")
                print(f"   用户名: {username}")
                print(f"   邮箱: {email}")
                print(f"   角色: admin")
                
        except Exception as e:
            print(f"❌ 操作失败: {e}")
            db.session.rollback()
            return False
            
    return True

def list_all_users():
    """列出所有用户"""
    with app.app_context():
        users = User.query.all()
        print("\n📋 当前系统用户列表:")
        print("-" * 50)
        for user in users:
            role_emoji = "👑" if user.role == "admin" else "👤"
            print(f"{role_emoji} ID: {user.id:2d} | {user.username:15s} | {user.email:25s} | {user.role}")
        print("-" * 50)

if __name__ == "__main__":
    print("🚀 管理员账户管理工具")
    print("=" * 40)
    
    # 显示当前用户
    list_all_users()
    
    if create_admin_user():
        print("\n🎉 操作完成！")
        list_all_users()
    else:
        print("\n💥 操作失败！")
        sys.exit(1)
