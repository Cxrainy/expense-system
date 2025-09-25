#!/usr/bin/env python3
"""
修复文件上传问题的脚本
1. 清理数据库中不存在的文件记录
2. 创建测试文件以验证文件上传功能
"""

from app import app, db, ExpenseFile, Expense
import os
import shutil
from PIL import Image

def create_test_files():
    """创建一些测试文件"""
    upload_dir = app.config['UPLOAD_FOLDER']
    
    # 创建一个简单的测试图片
    test_image_path = os.path.join(upload_dir, 'test_receipt.png')
    
    # 创建一个简单的彩色图片
    img = Image.new('RGB', (400, 300), color='lightblue')
    
    # 在图片上添加一些文本（模拟报销凭证）
    try:
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # 尝试使用系统字体，如果没有就跳过文字
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 100), "测试报销凭证", fill='black', font=font)
        draw.text((50, 140), "Test Receipt", fill='black', font=font)
        draw.text((50, 180), "金额: ¥123.45", fill='red', font=font)
        
    except ImportError:
        # 如果没有PIL，就创建一个简单的文件
        pass
    
    img.save(test_image_path)
    print(f"创建测试图片: {test_image_path}")
    
    return test_image_path

def fix_file_records():
    """修复文件记录"""
    with app.app_context():
        print("=== 开始修复文件记录 ===")
        
        # 检查所有文件记录
        files = ExpenseFile.query.all()
        
        for file_record in files:
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], file_record.filename)
            
            if not os.path.exists(full_path):
                print(f"文件不存在，删除记录: {file_record.filename}")
                
                # 删除文件记录
                db.session.delete(file_record)
        
        db.session.commit()
        print("文件记录修复完成")
        
        # 创建测试文件
        test_file_path = create_test_files()
        
        # 为第一个报销记录添加测试文件
        first_expense = Expense.query.first()
        if first_expense:
            test_filename = os.path.basename(test_file_path)
            
            # 创建文件记录
            new_file = ExpenseFile(
                filename=test_filename,
                original_filename="测试报销凭证.png",
                file_path=test_file_path,
                file_size=os.path.getsize(test_file_path),
                file_type="png",
                expense_id=first_expense.id
            )
            
            db.session.add(new_file)
            db.session.commit()
            
            print(f"为报销记录 {first_expense.id} 添加了测试文件")

if __name__ == '__main__':
    fix_file_records()
    print("修复完成！")