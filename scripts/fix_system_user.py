#!/usr/bin/env python3
"""
修复系统用户问题脚本
"""
import sys
import os
from werkzeug.security import generate_password_hash

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.main import app, db, User

def fix_system_user():
    """修复系统用户的问题"""
    with app.app_context():
        print("🔧 修复系统用户...")
        
        # 查找系统用户
        system_user = User.query.filter_by(email='system@example.com').first()
        
        if system_user:
            print(f"📋 找到系统用户: {system_user.username} ({system_user.email})")
            print(f"   当前角色: {system_user.role}")
            
            # 选择1: 设置已知密码
            # 选择2: 将其设为管理员
            # 选择3: 删除系统用户
            
            print("\n请选择处理方式:")
            print("1. 为系统用户设置已知密码 (123456)")
            print("2. 将系统用户升级为管理员")
            print("3. 删除系统用户")
            print("4. 查看所有用户信息")
            
            choice = input("请输入选择 (1-4): ").strip()
            
            if choice == "1":
                # 设置已知密码
                system_user.password = generate_password_hash("123456")
                db.session.commit()
                print("✅ 系统用户密码已设置为: 123456")
                
            elif choice == "2":
                # 升级为管理员
                system_user.role = 'admin'
                system_user.password = generate_password_hash("123456")
                db.session.commit()
                print("✅ 系统用户已升级为管理员，密码设置为: 123456")
                
            elif choice == "3":
                # 删除系统用户
                # 首先检查是否有关联数据
                expense_count = db.session.execute(db.text("SELECT COUNT(*) FROM expense WHERE user_id = :user_id"), {"user_id": system_user.id}).scalar()
                
                if expense_count > 0:
                    print(f"⚠️ 系统用户有 {expense_count} 条关联费用记录，无法直接删除")
                    print("请先处理关联数据或将记录转移到其他用户")
                    return
                
                confirm = input(f"确定要删除系统用户 '{system_user.username}' 吗? (y/N): ").lower()
                if confirm == 'y':
                    db.session.delete(system_user)
                    db.session.commit()
                    print("✅ 系统用户已删除")
                else:
                    print("❌ 操作已取消")
                    
            elif choice == "4":
                # 查看所有用户
                users = User.query.all()
                print("\n📋 所有用户信息:")
                print("-" * 60)
                for user in users:
                    role_icon = "👑" if user.role == "admin" else "👤"
                    print(f"{role_icon} ID: {user.id} | {user.username} | {user.email} | {user.role}")
                print("-" * 60)
                
            else:
                print("❌ 无效选择")
                
        else:
            print("❌ 没有找到系统用户")

def test_login():
    """测试登录功能"""
    print("\n🧪 测试登录功能...")
    
    with app.app_context():
        from werkzeug.security import check_password_hash
        
        # 测试admin用户
        admin_user = User.query.filter_by(email='admin@expense.com').first()
        if admin_user:
            print(f"📋 测试管理员用户: {admin_user.username}")
            # 这里无法直接测试，因为我们不知道密码
            print("   请尝试用您设置的密码登录")
        
        # 测试系统用户
        system_user = User.query.filter_by(email='system@example.com').first()
        if system_user:
            print(f"📋 测试系统用户: {system_user.username}")
            if check_password_hash(system_user.password, "123456"):
                print("   ✅ 密码 '123456' 验证成功")
            else:
                print("   ❌ 密码 '123456' 验证失败")

if __name__ == "__main__":
    print("🚀 系统用户修复工具")
    print("=" * 40)
    
    fix_system_user()
    test_login()
    
    print("\n🎉 修复完成！现在您可以尝试登录：")
    print("   管理员: admin@expense.com (您创建时设置的密码)")
    print("   系统用户: system@example.com (密码: 123456，如果您选择了选项1或2)")
