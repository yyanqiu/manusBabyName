# -*- coding: utf-8 -*-
"""
自动化测试脚本 (V3.2 八字增强版)
"""

from naming_generator import NamingGenerator
import datetime

def test_naming():
    """测试取名功能"""
    print("=" * 60)
    print("测试取名系统 V3.2 (八字增强版)")
    print("=" * 60)
    
    # 测试案例1：李姓男孩（无八字）
    print("\n测试案例1：李姓男孩（无八字）")
    print("-" * 60)
    generator1 = NamingGenerator("李", "男")
    results1 = generator1.generate_names(3)
    
    if results1:
        print(f"成功生成 {len(results1)} 个名字")
        for i, name_data in enumerate(results1[:3], 1):
            print(f"{i}. {name_data['姓名']} - {name_data['评分']['总分']}分")
    else:
        print("未能生成名字")
    
    # 测试案例2：王姓女孩（带八字自动计算）
    print("\n测试案例2：王姓女孩（带八字自动计算）")
    print("-" * 60)
    birthdate2 = datetime.date(2024, 1, 15)
    generator2 = NamingGenerator("王", "女", birthdate=birthdate2)
    results2 = generator2.generate_names(3)
    
    if results2:
        print(f"成功生成 {len(results2)} 个名字")
        if generator2.bazi_analysis:
            print(f"八字：{generator2.bazi_analysis['八字字符串']}")
            print(f"喜用神：{', '.join(generator2.xiyongshen)}")
        for i, name_data in enumerate(results2[:3], 1):
            print(f"{i}. {name_data['姓名']} - {name_data['评分']['总分']}分")
    else:
        print("未能生成名字")
    
    # 测试案例3：张姓男孩（手动指定喜用神）
    print("\n测试案例3：张姓男孩（手动指定喜用神）")
    print("-" * 60)
    generator3 = NamingGenerator("张", "男", xiyongshen=["金", "水"])
    results3 = generator3.generate_names(3)
    
    if results3:
        print(f"成功生成 {len(results3)} 个名字")
        for i, name_data in enumerate(results3[:3], 1):
            print(f"{i}. {name_data['姓名']} - {name_data['评分']['总分']}分")
    else:
        print("未能生成名字")
    
    # 测试案例4：测试八字计算模块
    print("\n测试案例4：八字计算模块测试")
    print("-" * 60)
    from bazi_calculator import BaZiCalculator
    
    test_dates = [
        (2024, 1, 15, 12),  # 2024年1月15日
        (2000, 6, 1, 8),    # 2000年6月1日
        (1990, 10, 10, 16), # 1990年10月10日
    ]
    
    for year, month, day, hour in test_dates:
        result = BaZiCalculator.analyze_bazi(year, month, day, hour)
        print(f"{year}-{month:02d}-{day:02d} {hour:02d}:00:")
        print(f"  八字：{result['八字字符串']}")
        print(f"  日主：{result['日主']}（{result['日主五行']}）")
        print(f"  喜用神：{', '.join(result['推荐喜用神'])}")
        print()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_naming()
