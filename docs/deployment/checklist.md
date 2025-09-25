# 🚀 Cloudflare部署检查清单

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
