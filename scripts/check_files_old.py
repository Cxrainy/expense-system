#!/usr/bin/env python3
from app import app, db, ExpenseFile
import os

with app.app_context():
    print("=== 检查数据库中的文件记录 ===")
    files = ExpenseFile.query.all()
    
    if not files:
        print("没有找到任何文件记录")
    else:
        for f in files:
            print(f'ID: {f.id}')
            print(f'文件名: {f.filename}')
            print(f'原始文件名: {f.original_filename}')
            print(f'文件路径: {f.file_path}')
            print(f'文件大小: {f.file_size} bytes')
            print(f'文件类型: {f.file_type}')
            
            # 检查文件是否存在
            full_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            if os.path.exists(full_file_path):
                print("✅ 文件存在")
            else:
                print("❌ 文件不存在")
            print("-" * 40)
    
    print(f"\n上传目录配置: {app.config['UPLOAD_FOLDER']}")
    print(f"上传目录是否存在: {os.path.exists(app.config['UPLOAD_FOLDER'])}")