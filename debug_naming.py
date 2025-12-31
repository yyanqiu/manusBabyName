# -*- coding: utf-8 -*-
from naming_generator import NamingGenerator
from data_characters import CHARACTERS

def debug_generation(surname, gender, xiyongshen=None):
    print(f"\n--- 调试开始：姓={surname}, 性别={gender}, 喜用神={xiyongshen} ---")
    
    # 1. 检查字库中符合性别的字
    suitable_gender = [c for c, info in CHARACTERS.items() if gender in info["性别"]]
    print(f"1. 符合性别({gender})的字数: {len(suitable_gender)}")
    
    # 2. 检查符合常用度的字
    suitable_common = [c for c in suitable_gender if CHARACTERS[c]["常用度"] >= 3]
    print(f"2. 符合常用度(>=3)的字数: {len(suitable_common)}")
    
    # 3. 检查符合喜用神的字
    if xiyongshen:
        suitable_xiyong = [c for c in suitable_common if CHARACTERS[c]["五行"] in xiyongshen]
        print(f"3. 符合喜用神({xiyongshen})的字数: {len(suitable_xiyong)}")
        
        # 分五行统计
        for wx in xiyongshen:
            count = len([c for c in suitable_common if CHARACTERS[c]["五行"] == wx])
            print(f"   - 五行[{wx}]的字数: {count}")
    
    # 4. 尝试生成
    generator = NamingGenerator(surname, gender, xiyongshen=xiyongshen)
    results = generator.generate_names(10)
    print(f"4. 最终生成名字数: {len(results)}")
    
    if not results:
        print("!!! 生成失败，尝试降低分数阈值测试...")
        # 临时修改阈值进行测试
        all_candidates = []
        for char1 in CHARACTERS.keys():
            char1_info = CHARACTERS[char1]
            if gender not in char1_info["性别"] or char1_info["常用度"] < 3: continue
            if xiyongshen and char1_info["五行"] not in xiyongshen: continue
            
            for char2 in CHARACTERS.keys():
                char2_info = CHARACTERS[char2]
                if gender not in char2_info["性别"] or char2_info["常用度"] < 3: continue
                if char1 == char2: continue
                if xiyongshen:
                    if char2_info["五行"] not in xiyongshen: continue
                    if len(xiyongshen) == 2 and char1_info["五行"] == char2_info["五行"]: continue
                
                full_name = surname + char1 + char2
                score = generator.evaluate_name(full_name)["总分"]
                all_candidates.append((full_name, score))
        
        if all_candidates:
            all_candidates.sort(key=lambda x: x[1], reverse=True)
            print(f"   找到候选组合数: {len(all_candidates)}")
            print(f"   最高分: {all_candidates[0][1]}")
            print(f"   最低分: {all_candidates[-1][1]}")
        else:
            print("   完全没有符合五行/性别限制的组合！")

if __name__ == "__main__":
    # 测试几种常见组合
    debug_generation("李", "男", ["金", "水"])
    debug_generation("王", "女", ["木", "火"])
    debug_generation("张", "男", ["土"])
    debug_generation("赵", "女", ["金", "木"])
