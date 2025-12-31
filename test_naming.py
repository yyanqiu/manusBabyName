# -*- coding: utf-8 -*-
"""
自动化测试脚本
"""

from naming_generator import NamingGenerator

def test_naming():
    """测试取名功能"""
    print("=" * 60)
    print("测试取名系统")
    print("=" * 60)
    
    # 测试案例1：李姓男孩
    print("\n测试案例1：李姓男孩")
    print("-" * 60)
    generator1 = NamingGenerator("李", "男")
    results1 = generator1.generate_names(5)
    
    if results1:
        print(f"成功生成 {len(results1)} 个名字")
        for i, name_data in enumerate(results1[:3], 1):
            print(f"{i}. {name_data['姓名']} - {name_data['评分']['总分']}分")
    else:
        print("未能生成名字")
    
    # 测试案例2：王姓女孩
    print("\n测试案例2：王姓女孩")
    print("-" * 60)
    generator2 = NamingGenerator("王", "女")
    results2 = generator2.generate_names(5)
    
    if results2:
        print(f"成功生成 {len(results2)} 个名字")
        for i, name_data in enumerate(results2[:3], 1):
            print(f"{i}. {name_data['姓名']} - {name_data['评分']['总分']}分")
    else:
        print("未能生成名字")
    
    # 测试案例3：张姓男孩
    print("\n测试案例3：张姓男孩")
    print("-" * 60)
    generator3 = NamingGenerator("张", "男")
    results3 = generator3.generate_names(5)
    
    if results3:
        print(f"成功生成 {len(results3)} 个名字")
        for i, name_data in enumerate(results3[:3], 1):
            print(f"{i}. {name_data['姓名']} - {name_data['评分']['总分']}分")
    else:
        print("未能生成名字")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_naming()
