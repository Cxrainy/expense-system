#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速导入报销类型 - 简化版本
适用于快速批量导入或系统初始化
"""

import os
import sys

# 确保能找到app模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def quick_import():
    """快速导入函数 - 可在其他脚本中调用"""
    try:
        from app import app, db, Category
        
        # 简化的类型数据
        categories = [
            "过桥费停车费", "维修费", "办公费", "油费", "生活补助", 
            "水电费", "住宿费", "福利费", "招待费", "广告费",
            "运输费", "手续费", "营业外支出", "工资", "租赁费", "其他应收"
        ]
        
        with app.app_context():
            imported = 0
            for name in categories:
                if not Category.query.filter_by(name=name).first():
                    category = Category(name=name, description=f"{name}相关支出")
                    db.session.add(category)
                    imported += 1
            
            db.session.commit()
            print(f"✅ 快速导入完成: {imported} 个新类型")
            return imported
            
    except Exception as e:
        print(f"❌ 快速导入失败: {e}")
        return 0

if __name__ == '__main__':
    quick_import()
