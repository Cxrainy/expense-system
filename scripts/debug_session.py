#!/usr/bin/env python3
"""
调试会话信息脚本
"""
import sys
import os
from werkzeug.security import check_password_hash

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.main import app, db, User

def test_login_process():
    """测试登录过程"""
    with app.app_context():
        print("🧪 测试登录流程...")
        
        # 模拟登录系统用户
        system_user = User.query.filter_by(email='system@example.com').first()
        if system_user:
            print(f"📋 系统用户信息:")
            print(f"   ID: {system_user.id}")
            print(f"   用户名: {system_user.username}")
            print(f"   邮箱: {system_user.email}")
            print(f"   角色: {system_user.role}")
            print(f"   密码验证: {'✅' if check_password_hash(system_user.password, '123456') else '❌'}")
            
            # 模拟会话设置
            print(f"\n🔐 登录时会话将设置为:")
            print(f"   session['user_id'] = {system_user.id}")
            print(f"   session['username'] = '{system_user.username}'")
            print(f"   session['role'] = '{system_user.role}'")
            
        # 模拟登录管理员用户
        admin_user = User.query.filter_by(email='admin@expense.com').first()
        if admin_user:
            print(f"\n📋 管理员用户信息:")
            print(f"   ID: {admin_user.id}")
            print(f"   用户名: {admin_user.username}")
            print(f"   邮箱: {admin_user.email}")
            print(f"   角色: {admin_user.role}")
            
            print(f"\n🔐 登录时会话将设置为:")
            print(f"   session['user_id'] = {admin_user.id}")
            print(f"   session['username'] = '{admin_user.username}'")
            print(f"   session['role'] = '{admin_user.role}'")

def analyze_permission_logic():
    """分析权限逻辑"""
    print(f"\n🔍 权限逻辑分析:")
    print(f"1. 管理员页面权限检查: session.get('role') != 'admin'")
    print(f"2. 模板显示检查: {{% if session.role == 'admin' %}}")
    print(f"3. API权限检查: session.get('role') != 'admin'")
    
    print(f"\n⚠️ 可能的问题:")
    print(f"1. 如果系统用户能访问管理功能，说明其session['role']被设置为'admin'")
    print(f"2. 这可能是由于数据库中角色被意外修改")
    print(f"3. 或者存在某种权限绕过机制")

if __name__ == "__main__":
    print("🚀 会话调试工具")
    print("=" * 50)
    
    test_login_process()
    analyze_permission_logic()
    
    print("\n💡 建议:")
    print("1. 用system@example.com + 123456登录，检查是否能看到管理菜单")
    print("2. 用admin@expense.com + 您的密码登录，检查管理功能")
    print("3. 如果系统用户仍能访问管理功能，检查浏览器中的session数据")
