#!/usr/bin/env python3
"""
应用功能验证脚本
验证重构后的应用是否正常工作
"""

import sys
import os
import requests
import time

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_app_availability():
    """测试应用可用性"""
    print("🔍 测试应用可用性...")
    
    try:
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("✅ 应用首页响应正常")
            return True
        elif response.status_code == 302:
            print("✅ 应用重定向正常")
            return True
        else:
            print(f"⚠️ 应用响应状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到应用")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_database_connection():
    """测试数据库连接"""
    print("🔍 测试数据库连接...")
    
    try:
        from app.main import app, db, User, Expense
        
        with app.app_context():
            # 测试用户表
            user_count = User.query.count()
            print(f"✅ 用户表连接正常，共有 {user_count} 个用户")
            
            # 测试报销表
            expense_count = Expense.query.count()
            print(f"✅ 报销表连接正常，共有 {expense_count} 条记录")
            
            return True
            
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("🔍 测试API端点...")
    
    api_tests = [
        ('/api/dashboard_stats', '仪表盘统计'),
        ('/api/currencies', '货币列表'),
        ('/api/categories', '分类列表'),
    ]
    
    success_count = 0
    
    for endpoint, name in api_tests:
        try:
            response = requests.get(f'http://localhost:5000{endpoint}', timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} API 正常")
                success_count += 1
            else:
                print(f"⚠️ {name} API 状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ {name} API 测试失败: {e}")
    
    return success_count == len(api_tests)

def test_static_files():
    """测试静态文件"""
    print("🔍 测试静态文件...")
    
    static_tests = [
        ('/static/css/styles.css', 'CSS样式文件'),
        ('/static/js/utils.js', 'JS工具文件'),
    ]
    
    success_count = 0
    
    for path, name in static_tests:
        try:
            response = requests.get(f'http://localhost:5000{path}', timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} 加载正常")
                success_count += 1
            else:
                print(f"⚠️ {name} 状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ {name} 测试失败: {e}")
    
    return success_count == len(static_tests)

def test_project_structure():
    """测试项目结构"""
    print("🔍 测试项目结构...")
    
    required_dirs = [
        'app',
        'templates', 
        'deployment',
        'docs',
        'scripts',
        'uploads'
    ]
    
    required_files = [
        'run.py',
        'requirements.txt',
        '.env.example',
        'app/main.py',
        'app/config.py'
    ]
    
    success = True
    
    # 检查目录
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ 目录 {dir_name}/ 存在")
        else:
            print(f"❌ 目录 {dir_name}/ 不存在")
            success = False
    
    # 检查文件
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ 文件 {file_name} 存在")
        else:
            print(f"❌ 文件 {file_name} 不存在")
            success = False
    
    return success

def main():
    """主验证函数"""
    print("🚀 开始验证重构后的应用...")
    print("=" * 50)
    
    tests = [
        ("项目结构", test_project_structure),
        ("数据库连接", test_database_connection),
        ("应用可用性", test_app_availability),
        ("API端点", test_api_endpoints),
        ("静态文件", test_static_files),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}测试:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 输出结果
    print("\n" + "=" * 50)
    print("📊 验证结果汇总:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！应用重构成功！")
        return True
    else:
        print("⚠️ 部分测试失败，请检查相关问题")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
