#!/usr/bin/env python3
"""
Cloudflare部署准备脚本
自动化部署前的准备工作
"""

import os
import json
import shutil
import subprocess
from pathlib import Path

def create_functions_structure():
    """创建Cloudflare Functions目录结构"""
    print("📁 创建Functions目录结构...")
    
    functions_dir = Path("functions")
    functions_dir.mkdir(exist_ok=True)
    
    api_dir = functions_dir / "api"
    api_dir.mkdir(exist_ok=True)
    
    # 创建主要的API处理器
    api_handler = api_dir / "[[path]].py"
    
    handler_content = '''"""
Cloudflare Functions API处理器
处理所有API请求
"""

import json
import os
import sys
from urllib.parse import parse_qs

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

# 导入Flask应用
try:
    from app import app
    from config import get_config
    
    # 应用配置
    app.config.from_object(get_config())
    
except ImportError as e:
    print(f"导入错误: {e}")
    app = None

def on_request(context):
    """Cloudflare Functions入口点"""
    request = context.request
    
    if not app:
        return Response("Application not available", status=500)
    
    try:
        # 构建WSGI环境
        environ = build_wsgi_environ(request)
        
        # 处理Flask应用
        response_data = []
        def start_response(status, headers):
            response_data.extend([status, headers])
        
        # 执行Flask应用
        result = app(environ, start_response)
        
        # 构建响应
        if response_data:
            status_code = int(response_data[0].split()[0])
            headers = dict(response_data[1])
            body = b''.join(result)
            
            return Response(
                body,
                status=status_code,
                headers=headers
            )
        else:
            return Response("No response data", status=500)
            
    except Exception as e:
        print(f"处理请求时出错: {e}")
        return Response(
            json.dumps({"error": "Internal server error"}),
            status=500,
            headers={"Content-Type": "application/json"}
        )

def build_wsgi_environ(request):
    """构建WSGI环境字典"""
    url = request.url
    
    environ = {
        'REQUEST_METHOD': request.method,
        'PATH_INFO': url.pathname,
        'QUERY_STRING': url.search[1:] if url.search else '',
        'CONTENT_TYPE': request.headers.get('content-type', ''),
        'CONTENT_LENGTH': str(len(request.body)) if request.body else '0',
        'SERVER_NAME': url.hostname,
        'SERVER_PORT': str(url.port or (443 if url.scheme == 'https' else 80)),
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': url.scheme,
        'wsgi.input': request.body or b'',
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # 添加HTTP头
    for key, value in request.headers.items():
        key = 'HTTP_' + key.upper().replace('-', '_')
        environ[key] = value
    
    return environ

class Response:
    """简单的响应类"""
    def __init__(self, body, status=200, headers=None):
        self.body = body if isinstance(body, bytes) else body.encode('utf-8')
        self.status = status
        self.headers = headers or {}
'''
    
    with open(api_handler, 'w', encoding='utf-8') as f:
        f.write(handler_content)
    
    print("✅ Functions结构创建完成")

def update_requirements():
    """更新requirements.txt以适配Cloudflare"""
    print("📦 更新依赖文件...")
    
    # 读取现有requirements
    requirements = []
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
    
    # 添加Cloudflare特定依赖
    cloudflare_deps = [
        'werkzeug>=2.0.0',
        'gunicorn>=20.1.0',  # 备用WSGI服务器
    ]
    
    for dep in cloudflare_deps:
        if not any(dep.split('>=')[0] in req for req in requirements):
            requirements.append(dep)
    
    # 写回文件
    with open('requirements.txt', 'w') as f:
        f.write('\n'.join(filter(None, requirements)))
    
    print("✅ 依赖文件更新完成")

def create_static_pages():
    """创建静态HTML页面"""
    print("📄 创建静态页面...")
    
    # 这里可以预渲染一些静态页面
    # 或者创建简单的入口页面
    
    index_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>报销管理系统</title>
    <script>
        // 重定向到仪表盘
        window.location.href = '/dashboard';
    </script>
</head>
<body>
    <p>正在跳转到仪表盘...</p>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print("✅ 静态页面创建完成")

def validate_environment():
    """验证部署环境"""
    print("🔍 验证环境配置...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'config.py',
        'wrangler.toml',
        '_headers',
        '_redirects'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 环境验证通过")
    return True

def create_deployment_checklist():
    """创建部署检查清单"""
    checklist = """# 🚀 Cloudflare部署检查清单

## 部署前准备
- [ ] 代码已推送到GitHub仓库
- [ ] 数据库服务已设置 (PlanetScale/Supabase)
- [ ] Cloudinary账户已创建 (文件存储)
- [ ] 环境变量已准备

## Cloudflare设置
- [ ] 已登录Cloudflare Dashboard
- [ ] 创建新的Pages项目
- [ ] 连接GitHub仓库
- [ ] 设置构建命令: `pip install -r requirements.txt`
- [ ] 设置构建输出目录: `.`

## 环境变量配置
在Cloudflare Pages设置中添加以下环境变量:

```
DATABASE_URL=your-database-connection-string
SECRET_KEY=your-secure-random-key
ENVIRONMENT=production
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
MAIL_SERVER=smtp.gmail.com (可选)
MAIL_USERNAME=your-email@gmail.com (可选)
MAIL_PASSWORD=your-app-password (可选)
```

## 部署后测试
- [ ] 访问首页是否正常
- [ ] 用户登录/注册功能
- [ ] 报销申请创建
- [ ] 文件上传功能
- [ ] 审批流程
- [ ] 报表导出
- [ ] 仪表盘显示

## 性能优化
- [ ] 启用Cloudflare缓存
- [ ] 配置自定义域名
- [ ] 设置SSL证书
- [ ] 监控性能指标

## 安全检查
- [ ] 所有敏感信息已移除代码
- [ ] HTTPS强制开启
- [ ] 安全headers已配置
- [ ] 数据库访问权限正确

---

**注意**: 首次部署可能需要5-10分钟才能完全生效。
"""
    
    with open('DEPLOYMENT_CHECKLIST.md', 'w', encoding='utf-8') as f:
        f.write(checklist)
    
    print("✅ 部署检查清单已创建")

def main():
    """主部署准备流程"""
    print("🚀 开始Cloudflare部署准备...")
    print("=" * 50)
    
    try:
        # 验证环境
        if not validate_environment():
            return False
        
        # 创建必要结构
        create_functions_structure()
        update_requirements()
        create_static_pages()
        create_deployment_checklist()
        
        print("\n" + "=" * 50)
        print("✅ 部署准备完成!")
        print("\n📋 下一步操作:")
        print("1. 查看 DEPLOYMENT_CHECKLIST.md 文件")
        print("2. 推送代码到GitHub")
        print("3. 在Cloudflare Pages中创建项目")
        print("4. 配置环境变量")
        print("5. 部署并测试")
        
        return True
        
    except Exception as e:
        print(f"❌ 部署准备失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
