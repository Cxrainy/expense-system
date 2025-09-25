"""
数据库初始化脚本
创建数据库表和添加示例数据
"""
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.main import app, db, User, Expense, ExpenseFile, Currency, Category
from datetime import datetime, date

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 检查是否已经有数据
        if User.query.count() > 0:
            print("数据库已经初始化过了")
            return
        
        # 创建测试用户
        admin_user = User(
            username='管理员',
            email='admin@company.com',
            password='admin123',  # 在生产环境中应该使用密码哈希
            role='admin'
        )
        
        employee_user = User(
            username='张三',
            email='user@company.com',
            password='user123',
            role='employee'
        )
        
        db.session.add(admin_user)
        db.session.add(employee_user)
        db.session.commit()
        
        # 创建默认货币
        default_currencies = [
            Currency(code='USD', name='美元', symbol='$', exchange_rate=1.0000, created_by=admin_user.id),
            Currency(code='CNY', name='人民币', symbol='¥', exchange_rate=7.2500, created_by=admin_user.id),  # 约7.25人民币=1美元
            Currency(code='EUR', name='欧元', symbol='€', exchange_rate=0.9091, created_by=admin_user.id),  # 约0.91欧元=1美元
            Currency(code='GBP', name='英镑', symbol='£', exchange_rate=0.8000, created_by=admin_user.id),  # 约0.8英镑=1美元
            Currency(code='JPY', name='日元', symbol='¥', exchange_rate=149.25, created_by=admin_user.id),  # 约149日元=1美元
            Currency(code='KRW', name='韩元', symbol='₩', exchange_rate=1428.57, created_by=admin_user.id),  # 约1429韩元=1美元
            Currency(code='HKD', name='港元', symbol='HK$', exchange_rate=7.8000, created_by=admin_user.id),  # 约7.8港元=1美元
            Currency(code='SGD', name='新加坡元', symbol='S$', exchange_rate=1.3514, created_by=admin_user.id),  # 约1.35新元=1美元
            Currency(code='AUD', name='澳元', symbol='A$', exchange_rate=1.4925, created_by=admin_user.id),  # 约1.49澳元=1美元
            Currency(code='CAD', name='加元', symbol='C$', exchange_rate=1.3514, created_by=admin_user.id),  # 约1.35加元=1美元
        ]
        
        for currency in default_currencies:
            db.session.add(currency)
        
        # 创建默认分类
        default_categories = [
            Category(name='餐饮费', description='工作餐、客户招待等餐饮费用', created_by=admin_user.id),
            Category(name='交通费', description='出差交通、打车、公交等交通费用', created_by=admin_user.id),
            Category(name='办公费', description='办公用品、文具、设备等办公费用', created_by=admin_user.id),
            Category(name='差旅费', description='出差住宿、机票等差旅费用', created_by=admin_user.id),
            Category(name='通讯费', description='电话、网络、邮寄等通讯费用', created_by=admin_user.id),
            Category(name='其他', description='其他类型的报销费用', created_by=admin_user.id),
        ]
        
        for category in default_categories:
            db.session.add(category)
        
        db.session.commit()
        
        # 创建示例报销记录（以美元为基准）
        sample_expenses = [
            Expense(
                title='商务午餐费用',
                description='与客户商务会谈午餐费用',
                amount=385.00,
                currency='CNY',
                exchange_rate=0.1379,  # CNY to USD 汇率 (1 CNY = 0.1379 USD)
                usd_amount=53.09,  # 385 * 0.1379
                category='餐饮费',
                expense_date=date.today(),
                status='pending',
                user_id=employee_user.id
            ),
            Expense(
                title='出租车费',
                description='从公司到机场的出租车费',
                amount=42.50,
                currency='USD',
                exchange_rate=1.0000,  # USD 基准货币
                usd_amount=42.50,
                category='交通费',
                expense_date=date.today(),
                status='approved',
                user_id=employee_user.id,
                approved_by=admin_user.id,
                approved_at=datetime.utcnow(),
                approval_comment='费用合理，审批通过'
            ),
            Expense(
                title='会议用品采购',
                description='购买会议室所需的文具用品',
                amount=22.30,
                currency='EUR',
                exchange_rate=1.1000,  # EUR to USD 汇率 (1 EUR = 1.1 USD)
                usd_amount=24.53,  # 22.30 * 1.1
                category='办公费',
                expense_date=date.today(),
                status='pending',
                user_id=employee_user.id
            ),
            Expense(
                title='客户招待费',
                description='与重要客户的商务晚餐',
                amount=95.50,
                currency='GBP',
                exchange_rate=1.2500,  # GBP to USD 汇率 (1 GBP = 1.25 USD)
                usd_amount=119.38,  # 95.50 * 1.25
                category='餐饮费',
                expense_date=date.today(),
                status='rejected',
                user_id=employee_user.id,
                approved_by=admin_user.id,
                approved_at=datetime.utcnow(),
                approval_comment='金额过高，需要提供更详细的说明'
            ),
            Expense(
                title='酒店住宿费',
                description='商务出差住宿费用',
                amount=15000,
                currency='JPY',
                exchange_rate=0.0067,  # JPY to USD 汇率 (1 JPY = 0.0067 USD) 
                usd_amount=100.50,  # 15000 * 0.0067
                category='差旅费',
                expense_date=date.today(),
                status='approved',
                user_id=employee_user.id,
                approved_by=admin_user.id,
                approved_at=datetime.utcnow(),
                approval_comment='差旅费用合理'
            )
        ]
        
        for expense in sample_expenses:
            db.session.add(expense)
        
        db.session.commit()
        
        # 创建示例附件（模拟数据）
        sample_files = [
            ExpenseFile(
                filename='sample_receipt_1.pdf',
                original_filename='商务午餐发票.pdf',
                file_path='uploads/sample_receipt_1.pdf',
                file_size=125000,
                file_type='pdf',
                expense_id=sample_expenses[0].id
            ),
            ExpenseFile(
                filename='sample_receipt_2.jpg',
                original_filename='出租车票据.jpg',
                file_path='uploads/sample_receipt_2.jpg',
                file_size=85000,
                file_type='jpg',
                expense_id=sample_expenses[1].id
            )
        ]
        
        for file_record in sample_files:
            db.session.add(file_record)
        
        db.session.commit()
        
        print("数据库初始化完成！")
        print("管理员账户: admin@company.com / admin123")
        print("员工账户: user@company.com / user123")

if __name__ == '__main__':
    init_database()