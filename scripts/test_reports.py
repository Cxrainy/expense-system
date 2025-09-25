#!/usr/bin/env python3
"""
报表功能测试脚本
用于验证报表导出功能是否正常工作
"""

import requests
import json
from datetime import datetime, timedelta

# 测试配置
BASE_URL = 'http://localhost:5000'
ADMIN_LOGIN = {
    'email': 'admin@company.com',
    'password': 'admin123'
}

def test_admin_login():
    """测试管理员登录"""
    print("🔐 测试管理员登录...")
    
    session = requests.Session()
    response = session.post(f'{BASE_URL}/login', json=ADMIN_LOGIN)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("✅ 管理员登录成功")
            return session
        else:
            print(f"❌ 登录失败: {result.get('message')}")
            return None
    else:
        print(f"❌ 登录请求失败: {response.status_code}")
        return None

def test_reports_page_access(session):
    """测试报表页面访问"""
    print("\n📊 测试报表页面访问...")
    
    response = session.get(f'{BASE_URL}/reports')
    
    if response.status_code == 200:
        if '报表导出' in response.text:
            print("✅ 报表页面访问成功")
            return True
        else:
            print("❌ 页面内容不正确")
            return False
    else:
        print(f"❌ 页面访问失败: {response.status_code}")
        return False

def test_preview_api(session):
    """测试预览API"""
    print("\n🔍 测试预览API...")
    
    # 设置测试数据
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    preview_data = {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'status': 'all'
    }
    
    response = session.post(
        f'{BASE_URL}/api/reports/preview',
        json=preview_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            data = result.get('data', {})
            print("✅ 预览API测试成功")
            print(f"   📈 总记录数: {data.get('total_records', 0)}")
            print(f"   📂 报销类型: {data.get('total_categories', 0)}")
            print(f"   💰 总金额: ${data.get('total_amount', 0):.2f}")
            print(f"   🖼️  包含图片: {data.get('with_images', 0)}")
            return True, data
        else:
            print(f"❌ 预览失败: {result.get('message')}")
            return False, None
    else:
        print(f"❌ 预览API请求失败: {response.status_code}")
        return False, None

def test_export_api(session):
    """测试导出API（不实际下载文件）"""
    print("\n📥 测试导出API...")
    
    # 设置测试数据
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)  # 只测试最近7天避免文件过大
    
    export_data = {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'status': 'all',
        'include_images': 'true',
        'group_by_category': 'true',
        'include_comments': 'true',
        'image_quality': 'medium'
    }
    
    # 注意：这里我们只测试API是否响应，不实际下载大文件
    response = session.post(f'{BASE_URL}/api/reports/export', data=export_data, stream=True)
    
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type', '')
        if 'spreadsheet' in content_type or 'excel' in content_type:
            print("✅ 导出API测试成功")
            print(f"   📄 Content-Type: {content_type}")
            
            # 检查文件大小（读取前1KB确认有内容）
            chunk = next(response.iter_content(1024), b'')
            if chunk:
                print(f"   📊 文件开始部分已生成（{len(chunk)} bytes）")
                return True
            else:
                print("❌ 导出文件为空")
                return False
        else:
            print(f"❌ 返回类型错误: {content_type}")
            return False
    else:
        print(f"❌ 导出API请求失败: {response.status_code}")
        try:
            error_msg = response.json().get('error', 'Unknown error')
            print(f"   错误信息: {error_msg}")
        except:
            print(f"   响应内容: {response.text[:200]}...")
        return False

def run_tests():
    """运行所有测试"""
    print("🚀 开始报表功能测试\n")
    
    # 测试1: 管理员登录
    session = test_admin_login()
    if not session:
        print("\n❌ 测试终止：无法登录")
        return False
    
    # 测试2: 页面访问
    if not test_reports_page_access(session):
        print("\n❌ 测试终止：无法访问报表页面")
        return False
    
    # 测试3: 预览API
    success, preview_data = test_preview_api(session)
    if not success:
        print("\n❌ 测试终止：预览API失败")
        return False
    
    # 测试4: 导出API（仅在有数据时测试）
    if preview_data and preview_data.get('total_records', 0) > 0:
        if not test_export_api(session):
            print("\n⚠️  警告：导出API测试失败")
    else:
        print("\n⚠️  跳过导出测试：没有可导出的数据")
    
    print("\n🎉 报表功能测试完成！")
    return True

if __name__ == '__main__':
    try:
        run_tests()
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
