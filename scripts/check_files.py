#!/usr/bin/env python3
from app import app, db, ExpenseFile, Expense
import os

with app.app_context():
    print("=== 检查所有报销记录和文件 ===")
    
    # 检查所有报销记录
    expenses = Expense.query.all()
    for expense in expenses:
        print(f"\n报销ID: {expense.id}")
        print(f"标题: {expense.title}")
        print(f"状态: {expense.status}")
        print(f"关联文件数量: {len(expense.files)}")
        
        for file in expense.files:
            print(f"  - 文件ID: {file.id}")
            print(f"  - 文件名: {file.filename}")
            print(f"  - 原始文件名: {file.original_filename}")
            
            # 检查文件是否存在
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            exists = os.path.exists(full_path)
            print(f"  - 文件存在: {'✅' if exists else '❌'}")
            
            if not exists:
                print(f"  - 期望路径: {full_path}")
    
    print(f"\n=== 检查uploads目录中的实际文件 ===")
    upload_dir = app.config['UPLOAD_FOLDER']
    if os.path.exists(upload_dir):
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                print(f"实际文件: {filename}")
                # 检查是否在数据库中有记录
                db_file = ExpenseFile.query.filter_by(filename=filename).first()
                if db_file:
                    print(f"  - 数据库中有记录 ✅")
                else:
                    print(f"  - 数据库中无记录 ❌")