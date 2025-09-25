"""
修复汇率逻辑脚本
将数据库中的汇率从旧逻辑（1单位货币=多少美元）转换为新逻辑（多少单位货币=1美元）
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(__file__))

from decimal import Decimal
from app import app, db, Currency, Expense

def fix_exchange_rates():
    """修复数据库中的汇率值"""
    with app.app_context():
        print("开始修复汇率逻辑...")
        
        # 汇率映射：旧汇率 -> 新汇率（多少单位货币=1美元）
        rate_conversions = {
            'USD': Decimal('1.0000'),      # 美元基准
            'CNY': Decimal('7.2500'),      # 人民币：约7.25人民币=1美元
            'EUR': Decimal('0.9091'),      # 欧元：约0.91欧元=1美元  
            'GBP': Decimal('0.8000'),      # 英镑：约0.8英镑=1美元
            'JPY': Decimal('149.25'),      # 日元：约149日元=1美元
            'KRW': Decimal('1428.57'),     # 韩元：约1429韩元=1美元
            'HKD': Decimal('7.8000'),      # 港元：约7.8港元=1美元
            'SGD': Decimal('1.3514'),      # 新加坡元：约1.35新元=1美元
            'AUD': Decimal('1.4925'),      # 澳元：约1.49澳元=1美元
            'CAD': Decimal('1.3514'),      # 加元：约1.35加元=1美元
        }
        
        # 修复Currency表中的汇率
        print("修复货币表中的汇率...")
        for currency in Currency.query.all():
            if currency.code in rate_conversions:
                old_rate = currency.exchange_rate
                new_rate = rate_conversions[currency.code]
                currency.exchange_rate = new_rate
                print(f"货币 {currency.code}: {old_rate} -> {new_rate}")
        
        # 修复Expense表中的汇率和美元金额
        print("修复报销记录中的汇率和美元金额...")
        for expense in Expense.query.all():
            if expense.currency in rate_conversions:
                old_rate = expense.exchange_rate
                new_rate = rate_conversions[expense.currency]
                
                # 重新计算美元金额：新逻辑是 usd_amount = amount / exchange_rate
                if expense.currency == 'USD':
                    new_usd_amount = expense.amount
                else:
                    new_usd_amount = expense.amount / new_rate
                
                # 更新记录
                expense.exchange_rate = new_rate
                expense.usd_amount = new_usd_amount
                print(f"报销记录 {expense.id} ({expense.currency}): 汇率 {old_rate} -> {new_rate}, 美元金额 -> {new_usd_amount:.2f}")
        
        # 提交更改
        db.session.commit()
        print("汇率修复完成！")

if __name__ == '__main__':
    fix_exchange_rates()