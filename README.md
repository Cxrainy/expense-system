# 报销系统

一个简洁的报销申请和审批系统，基于Flask和SQLite构建。

## 功能特点

- 用户登录认证
- 报销申请提交
- 管理员审批功能
- 简洁的前后端分离架构

## 技术栈

- 后端：Python Flask
- 数据库：SQLite
- 前端：HTML + CSS + JavaScript
- UI设计：基于原ERP模板的简洁风格

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 初始化数据库：
```bash
python init_db.py
```

3. 运行应用：
```bash
python app.py
```

4. 访问：http://localhost:5000

## 默认账户

- 管理员：admin@company.com / admin123
- 员工：user@company.com / user123

## 项目结构

```
expense-system/
├── app.py              # 主应用文件
├── init_db.py          # 数据库初始化脚本
├── requirements.txt    # 依赖列表
├── templates/          # HTML模板
├── static/            # 静态文件
│   ├── css/           # 样式文件
│   └── js/            # JavaScript文件
└── expense_system.db  # SQLite数据库（自动生成）
```

## 🚀 快速启动

### 开发环境
```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件设置你的配置

# 启动应用
python run.py
```

### 生产环境
```bash
# 使用Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app.main:app

# 或使用Flask内置服务器
export FLASK_APP=app.main
export FLASK_ENV=production
flask run
```

## 📁 项目结构

```
expense-system/
├── app/                    # 核心应用代码
│   ├── main.py            # 主应用文件
│   ├── config.py          # 配置文件
│   └── static/            # 静态资源
├── templates/             # 模板文件
├── deployment/           # 部署相关文件
├── docs/                 # 文档
├── scripts/              # 开发脚本
├── uploads/              # 上传文件
├── requirements.txt      # 依赖文件
└── run.py               # 启动入口
```

## 📚 文档

- [Cloudflare部署指南](docs/deployment/cloudflare_guide.md)
- [快速部署指南](docs/deployment/quick_deploy.md)
- [功能文档](docs/features/)
- [修复记录](docs/fixes/)

