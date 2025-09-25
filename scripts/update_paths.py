#!/usr/bin/env python3
"""
更新数据库中的文件路径格式
"""

from app import app, db, ExpenseFile
import os

def update_file_paths():
    """更新文件路径格式"""
    with app.app_context():
        print("=== 更新文件路径格式 ===")
        
        files = ExpenseFile.query.all()
        
        for file_record in files:
            # 如果file_path包含完整路径，则只保留文件名
            if os.path.sep in file_record.file_path or '/' in file_record.file_path:
                file_record.file_path = file_record.filename
                print(f"更新文件路径: {file_record.filename}")
        
        db.session.commit()
        print("文件路径格式更新完成")

if __name__ == '__main__':
    update_file_paths()