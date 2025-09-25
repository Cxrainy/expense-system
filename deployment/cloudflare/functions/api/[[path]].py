"""
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
    from app.main import app
    from app.config import get_config
    
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
