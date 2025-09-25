#!/usr/bin/env python3
from app import app, db, ExpenseFile, Expense

with app.app_context():
    print("=== 搜索问题文件记录 ===")
    
    # 搜索可能的问题文件名
    problem_filename = "ce3d0cc8-7e05-4dd9-b060-62fe76b3c87c_20250910112942_21_16.png"
    
    # 检查是否有这个文件名的记录
    problem_file = ExpenseFile.query.filter_by(filename=problem_filename).first()
    if problem_file:
        print(f"找到问题文件记录:")
        print(f"  - ID: {problem_file.id}")
        print(f"  - 文件名: {problem_file.filename}")
        print(f"  - 原始文件名: {problem_file.original_filename}")
        print(f"  - 关联的报销ID: {problem_file.expense_id}")
        
        # 检查关联的报销记录
        expense = Expense.query.get(problem_file.expense_id)
        if expense:
            print(f"  - 关联报销标题: {expense.title}")
            print(f"  - 关联报销状态: {expense.status}")
        
        print("\n删除这个无效的文件记录...")
        db.session.delete(problem_file)
        db.session.commit()
        print("✅ 已删除无效文件记录")
    else:
        print("未找到该文件记录")
    
    # 搜索所有包含UUID格式的文件名
    print("\n=== 搜索所有UUID格式的文件名 ===")
    all_files = ExpenseFile.query.all()
    for f in all_files:
        if len(f.filename) > 32 and '-' in f.filename:  # UUID格式特征
            print(f"发现UUID格式文件: {f.filename}")
            
            # 检查文件是否存在
            import os
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            if not os.path.exists(full_path):
                print(f"  ❌ 文件不存在，建议删除记录")
                print(f"  关联报销ID: {f.expense_id}")
            else:
                print(f"  ✅ 文件存在")