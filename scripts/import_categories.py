#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报销类型快速导入脚本
用于将预定义的报销类型批量导入到数据库中

使用方法:
1. 确保Flask应用已启动
2. 运行: python import_expense_categories.py
3. 或在Flask应用中调用: from import_expense_categories import import_categories; import_categories()
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app, db, Category

# 预定义的报销类型数据 - 包含详细描述
EXPENSE_CATEGORIES = [
    {
        "name": "过桥费停车费",
        "description": "车辆通行过桥费、隧道费、停车费等交通相关费用。包括高速公路过路费、市内停车场费用、临时停车费等。"
    },
    {
        "name": "维修费", 
        "description": "设备、车辆、办公设施等的维护和修理费用。包括预防性维护、故障修复、零部件更换、保养服务等。"
    },
    {
        "name": "办公费",
        "description": "日常办公用品和办公设备的采购费用。包括文具用品、纸张、墨盒、办公设备小件、办公软件等。"
    },
    {
        "name": "油费",
        "description": "车辆燃油费用，包括汽油、柴油等。用于公务用车、出差车辆的加油费用报销。"
    },
    {
        "name": "生活补助",
        "description": "员工生活相关的补助费用。包括餐补、交通补助、通讯补助、节日补助等福利性支出。"
    },
    {
        "name": "水电费",
        "description": "办公场所的水费、电费、燃气费等基础设施费用。包括月度账单、临时用水用电费用。"
    },
    {
        "name": "住宿费",
        "description": "出差期间的酒店住宿费用。包括标准间、商务间等符合公司差旅标准的住宿开支。"
    },
    {
        "name": "福利费",
        "description": "员工福利相关支出。包括节日慰问、生日福利、团建活动、员工体检、培训等福利性费用。"
    },
    {
        "name": "招待费",
        "description": "业务招待和客户接待费用。包括商务用餐、客户接待、会议餐费等合理的业务招待支出。"
    },
    {
        "name": "广告费",
        "description": "市场推广和广告宣传费用。包括线上广告投放、宣传物料制作、展会参展、品牌推广等营销支出。"
    },
    {
        "name": "运输费",
        "description": "货物运输和物流费用。包括快递费、物流配送费、货运费、仓储费等运输相关支出。"
    },
    {
        "name": "手续费",
        "description": "各类金融和行政手续费用。包括银行手续费、汇款费、认证费、审批费、服务费等。"
    },
    {
        "name": "营业外支出",
        "description": "非日常经营活动产生的支出。包括捐赠支出、罚款支出、资产处置损失等特殊项目支出。"
    },
    {
        "name": "工资",
        "description": "员工薪酬支出。包括基本工资、奖金、津贴、补贴等人力成本相关的工资性支出。"
    },
    {
        "name": "租赁费",
        "description": "租赁相关费用。包括办公场所租金、设备租赁费、车辆租赁费等各类租赁合同项下的支出。"
    },
    {
        "name": "其他应收",
        "description": "其他类型的应收款项和杂项支出。包括临时性支出、预付款项、保证金等暂时无法归类的费用。"
    }
]

def import_categories():
    """导入报销类型到数据库"""
    from app.main import User  # 导入User模型
    
    with app.app_context():
        try:
            print("🚀 开始导入报销类型...")
            
            # 获取系统管理员用户作为创建者
            admin_user = User.query.filter_by(role='admin').first()
            if not admin_user:
                print("❌ 未找到管理员用户，请先创建管理员账户")
                return {'success': False, 'error': '未找到管理员用户'}
            
            # 统计信息
            imported_count = 0
            updated_count = 0
            skipped_count = 0
            
            for category_data in EXPENSE_CATEGORIES:
                name = category_data["name"]
                description = category_data["description"]
                
                # 检查是否已存在
                existing_category = Category.query.filter_by(name=name).first()
                
                if existing_category:
                    # 更新描述
                    if existing_category.description != description:
                        existing_category.description = description
                        updated_count += 1
                        print(f"✅ 更新类型: {name}")
                    else:
                        skipped_count += 1
                        print(f"⏭️  跳过类型: {name} (已存在且无变化)")
                else:
                    # 创建新类型
                    new_category = Category(
                        name=name,
                        description=description,
                        created_by=admin_user.id
                    )
                    db.session.add(new_category)
                    imported_count += 1
                    print(f"✨ 新增类型: {name}")
            
            # 提交事务
            db.session.commit()
            
            # 打印统计结果
            print("\n" + "="*60)
            print("📊 导入完成统计:")
            print(f"   📝 新增类型: {imported_count} 个")
            print(f"   🔄 更新类型: {updated_count} 个") 
            print(f"   ⏭️  跳过类型: {skipped_count} 个")
            print(f"   📋 总计处理: {len(EXPENSE_CATEGORIES)} 个")
            print("="*60)
            
            # 验证导入结果
            total_categories = Category.query.count()
            print(f"🗂️  数据库中总类型数: {total_categories} 个")
            
            return {
                'success': True,
                'imported': imported_count,
                'updated': updated_count,
                'skipped': skipped_count,
                'total': len(EXPENSE_CATEGORIES)
            }
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ 导入失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

def list_all_categories():
    """列出所有报销类型"""
    with app.app_context():
        categories = Category.query.all()
        print("\n📋 当前数据库中的所有报销类型:")
        print("="*80)
        for i, category in enumerate(categories, 1):
            print(f"{i:2d}. {category.name}")
            if category.description:
                # 描述文字换行处理
                desc_lines = [category.description[i:i+60] for i in range(0, len(category.description), 60)]
                for line in desc_lines:
                    print(f"     {line}")
            print("-" * 80)
        print(f"\n总计: {len(categories)} 个报销类型")

def delete_category(category_name):
    """删除指定的报销类型（谨慎使用）"""
    with app.app_context():
        try:
            category = Category.query.filter_by(name=category_name).first()
            if category:
                db.session.delete(category)
                db.session.commit()
                print(f"✅ 已删除类型: {category_name}")
                return True
            else:
                print(f"❌ 未找到类型: {category_name}")
                return False
        except Exception as e:
            db.session.rollback()
            print(f"❌ 删除失败: {str(e)}")
            return False

def clear_all_categories():
    """清空所有报销类型（危险操作）"""
    with app.app_context():
        try:
            count = Category.query.count()
            confirmation = input(f"⚠️  确认要删除所有 {count} 个报销类型吗？(输入 'YES' 确认): ")
            if confirmation == 'YES':
                Category.query.delete()
                db.session.commit()
                print(f"🗑️  已清空所有报销类型 ({count} 个)")
                return True
            else:
                print("❌ 操作已取消")
                return False
        except Exception as e:
            db.session.rollback()
            print(f"❌ 清空失败: {str(e)}")
            return False

def main():
    """主函数 - 命令行执行"""
    import argparse
    
    parser = argparse.ArgumentParser(description='报销类型管理工具')
    parser.add_argument('--action', choices=['import', 'list', 'delete', 'clear'], 
                       default='import', help='执行的操作')
    parser.add_argument('--name', help='类型名称（用于删除操作）')
    
    args = parser.parse_args()
    
    if args.action == 'import':
        print("🎯 执行导入操作...")
        result = import_categories()
        if result['success']:
            print("🎉 导入操作成功完成！")
        else:
            print("💥 导入操作失败！")
            sys.exit(1)
            
    elif args.action == 'list':
        list_all_categories()
        
    elif args.action == 'delete':
        if not args.name:
            print("❌ 请指定要删除的类型名称: --name '类型名称'")
            sys.exit(1)
        delete_category(args.name)
        
    elif args.action == 'clear':
        clear_all_categories()

if __name__ == '__main__':
    main()
