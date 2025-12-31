# -*- coding: utf-8 -*-
"""
喜用神功能测试脚本
"""

from naming_generator import NamingGenerator
from data_characters import get_character_info

def test_xiyongshen():
    """测试喜用神功能"""
    print("=" * 60)
    print("喜用神功能测试")
    print("=" * 60)
    
    # 测试案例1：双喜用神（金、水）
    print("\n【测试1】双喜用神：金、水")
    print("-" * 60)
    generator1 = NamingGenerator("李", "男", xiyongshen=["金", "水"])
    results1 = generator1.generate_names(5)
    
    if results1:
        print(f"成功生成 {len(results1)} 个名字")
        for i, name_data in enumerate(results1[:3], 1):
            name = name_data['名字']
            char1_info = get_character_info(name[0])
            char2_info = get_character_info(name[1])
            wuxing1 = char1_info['五行'] if char1_info else '?'
            wuxing2 = char2_info['五行'] if char2_info else '?'
            print(f"{i}. {name_data['姓名']} - {name_data['评分']['总分']}分 (五行：{wuxing1}、{wuxing2})")
            print(f"   八字得分：{name_data['评分']['八字得分']}分")
    else:
        print("未能生成名字")
    
    # 测试案例2：单喜用神（木）
    print("\n【测试2】单喜用神：木")
    print("-" * 60)
    generator2 = NamingGenerator("王", "女", xiyongshen=["木"])
    results2 = generator2.generate_names(5)
    
    if results2:
        print(f"成功生成 {len(results2)} 个名字")
        for i, name_data in enumerate(results2[:3], 1):
            name = name_data['名字']
            char1_info = get_character_info(name[0])
            char2_info = get_character_info(name[1])
            wuxing1 = char1_info['五行'] if char1_info else '?'
            wuxing2 = char2_info['五行'] if char2_info else '?'
            print(f"{i}. {name_data['姓名']} - {name_data['评分']['总分']}分 (五行：{wuxing1}、{wuxing2})")
            print(f"   八字得分：{name_data['评分']['八字得分']}分")
    else:
        print("未能生成名字")
    
    # 测试案例3：双喜用神（火、土）
    print("\n【测试3】双喜用神：火、土")
    print("-" * 60)
    generator3 = NamingGenerator("张", "男", xiyongshen=["火", "土"])
    results3 = generator3.generate_names(5)
    
    if results3:
        print(f"成功生成 {len(results3)} 个名字")
        for i, name_data in enumerate(results3[:3], 1):
            name = name_data['名字']
            char1_info = get_character_info(name[0])
            char2_info = get_character_info(name[1])
            wuxing1 = char1_info['五行'] if char1_info else '?'
            wuxing2 = char2_info['五行'] if char2_info else '?'
            print(f"{i}. {name_data['姓名']} - {name_data['评分']['总分']}分 (五行：{wuxing1}、{wuxing2})")
            print(f"   八字得分：{name_data['评分']['八字得分']}分")
    else:
        print("未能生成名字")
    
    # 测试案例4：不指定喜用神
    print("\n【测试4】不指定喜用神")
    print("-" * 60)
    generator4 = NamingGenerator("刘", "女", xiyongshen=[])
    results4 = generator4.generate_names(3)
    
    if results4:
        print(f"成功生成 {len(results4)} 个名字")
        for i, name_data in enumerate(results4[:3], 1):
            name = name_data['名字']
            char1_info = get_character_info(name[0])
            char2_info = get_character_info(name[1])
            wuxing1 = char1_info['五行'] if char1_info else '?'
            wuxing2 = char2_info['五行'] if char2_info else '?'
            print(f"{i}. {name_data['姓名']} - {name_data['评分']['总分']}分 (五行：{wuxing1}、{wuxing2})")
            print(f"   八字得分：{name_data['评分']['八字得分']}分")
    else:
        print("未能生成名字")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_xiyongshen()
