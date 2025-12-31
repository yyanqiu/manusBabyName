# -*- coding: utf-8 -*-
"""
取名生成器主程序 (V3.1 离线增强版)
根据姓氏、性别、出生日期生成推荐名字，并集成离线文化深度解析
"""

import datetime
import random
from wuge_calculator import WuGeCalculator
from sancai_analyzer import SanCaiAnalyzer
from data_81_numbers import get_number_luck, get_number_meaning
from data_characters import get_character_info, CHARACTERS
from ai_analyzer import AIAnalyzer


class NamingGenerator:
    """取名生成器"""
    
    def __init__(self, surname, gender, birthdate=None, xiyongshen=None):
        """
        初始化
        :param surname: 姓氏
        :param gender: 性别（"男"/"女"）
        :param birthdate: 出生日期（可选，用于八字分析）
        :param xiyongshen: 喜用神列表（可选，如 ["金", "水"]）
        """
        self.surname = surname
        self.gender = gender
        self.birthdate = birthdate
        self.xiyongshen = xiyongshen if xiyongshen else []
        self.ai_analyzer = AIAnalyzer()
        
        # 获取姓氏笔画
        surname_info = get_character_info(surname[0]) if len(surname) > 0 else None
        self.surname_stroke = surname_info["笔画"] if surname_info else None
        
    def generate_names(self, count=10):
        """
        生成推荐名字列表
        :param count: 生成数量
        :return: 名字列表（已评分排序）
        """
        candidates = []
        all_chars = list(CHARACTERS.keys())
        
        # 增加随机性，避免每次生成都一样
        random.shuffle(all_chars)
        
        # 遍历所有可能的双名组合
        for char1 in all_chars:
            char1_info = CHARACTERS[char1]
            
            # 检查第一个字是否适合该性别
            if self.gender not in char1_info["性别"]:
                continue
            
            # 常用度筛选（至少3分）
            if char1_info["常用度"] < 3:
                continue
            
            # 喜用神筛选：第一个字尽量在喜用神中
            if self.xiyongshen and char1_info["五行"] not in self.xiyongshen:
                # 如果指定了喜用神但第一个字不匹配，降低其被选中的概率
                if random.random() > 0.2:
                    continue
                
            for char2 in all_chars:
                char2_info = CHARACTERS[char2]
                
                # 检查第二个字是否适合该性别
                if self.gender not in char2_info["性别"]:
                    continue
                
                # 常用度筛选
                if char2_info["常用度"] < 3:
                    continue
                
                # 避免重复字
                if char1 == char2:
                    continue
                
                # 喜用神筛选
                if self.xiyongshen:
                    # 如果指定了2个喜用神，尽量让两个字分别对应
                    if len(self.xiyongshen) == 2:
                        match1 = char1_info["五行"] in self.xiyongshen
                        match2 = char2_info["五行"] in self.xiyongshen
                        if not (match1 or match2):
                            continue
                    else:
                        if char1_info["五行"] not in self.xiyongshen and char2_info["五行"] not in self.xiyongshen:
                            continue
                
                # 生成完整姓名
                full_name = self.surname + char1 + char2
                
                # 计算评分
                score_result = self.evaluate_name(full_name)
                
                # 评分阈值
                threshold = 75 if not self.xiyongshen else 70
                
                if score_result["总分"] >= threshold:
                    candidates.append({
                        "姓名": full_name,
                        "名字": char1 + char2,
                        "评分": score_result
                    })
                    
                # 限制候选池大小，防止计算过久
                if len(candidates) > 200:
                    break
            if len(candidates) > 200:
                break
        
        # 按总分排序
        candidates.sort(key=lambda x: x["评分"]["总分"], reverse=True)
        
        # 只取前 count 个进行文化分析
        final_results = candidates[:count]
        
        print(f"正在进行文化深度解析（共 {len(final_results)} 个名字）...")
        for item in final_results:
            item["文化解析"] = self.ai_analyzer.analyze_name(self.surname, item["名字"], self.gender)
            
        return final_results
    
    def evaluate_name(self, full_name):
        """评估名字得分"""
        surname = self.surname
        name = full_name[len(surname):]
        
        calc = WuGeCalculator(surname, name)
        wuge_result = calc.calculate_all()
        
        wuge_score = 0
        wuge_details = {}
        
        for ge_name, ge_info in wuge_result.items():
            num = ge_info["数值"]
            luck = get_number_luck(num)
            wuge_details[ge_name] = {
                "数值": num,
                "五行": ge_info["五行"],
                "吉凶": luck
            }
            if luck == "吉":
                wuge_score += 8
        
        sancai_result = SanCaiAnalyzer.analyze_sancai(
            wuge_result["天格"]["五行"],
            wuge_result["人格"]["五行"],
            wuge_result["地格"]["五行"]
        )
        sancai_score = sancai_result["得分"]
        
        ziyi_score = self._evaluate_meaning_and_sound(name)
        bazi_score = self._calculate_bazi_score(name)
        
        total_score = wuge_score + sancai_score + ziyi_score + bazi_score
        
        return {
            "总分": total_score,
            "五格得分": wuge_score,
            "三才得分": sancai_score,
            "字义得分": ziyi_score,
            "八字得分": bazi_score,
            "五格详情": wuge_details,
            "三才详情": sancai_result,
            "三才配置": calc.get_sancai()
        }
    
    def _evaluate_meaning_and_sound(self, name):
        """评估字义和音韵"""
        score = 0
        for char in name:
            char_info = get_character_info(char)
            if char_info:
                score += char_info["常用度"]
        
        if len(name) == 2:
            char1_info = get_character_info(name[0])
            char2_info = get_character_info(name[1])
            if char1_info and char2_info:
                if char1_info["拼音"][0] != char2_info["拼音"][0]:
                    score += 5
        return min(score, 20)
    
    def _calculate_bazi_score(self, name):
        """计算八字匹配得分"""
        if not self.xiyongshen:
            return 5
        
        wuxing_list = []
        for char in name:
            char_info = get_character_info(char)
            if char_info:
                wuxing_list.append(char_info["五行"])
        
        if not wuxing_list: return 0
        
        if len(self.xiyongshen) == 2:
            match_count = sum(1 for wx in wuxing_list if wx in self.xiyongshen)
            unique_matches = len(set(wx for wx in wuxing_list if wx in self.xiyongshen))
            if unique_matches == 2: return 10
            if match_count >= 1: return 5
        else:
            match_count = sum(1 for wx in wuxing_list if wx in self.xiyongshen)
            if match_count == 2: return 10
            if match_count == 1: return 5
            
        return 0
    
    def format_result(self, name_data, rank):
        """格式化输出"""
        full_name = name_data["姓名"]
        name_only = name_data["名字"]
        score_data = name_data["评分"]
        culture_analysis = name_data.get("文化解析", "暂无文化解析。")
        
        output = []
        output.append(f"\n{'='*60}")
        output.append(f"推荐名字 {rank}：{full_name}（综合评分：{score_data['总分']}分）")
        output.append(f"{'='*60}")
        
        output.append("\n【五格分析】得分：{}".format(score_data["五格得分"]))
        wuge_details = score_data["五格详情"]
        for ge_name in ["天格", "人格", "地格", "总格", "外格"]:
            ge_info = wuge_details[ge_name]
            luck_symbol = "✓" if ge_info["吉凶"] == "吉" else "✗"
            output.append(f"  {ge_name}：{ge_info['数值']}（{ge_info['五行']}）- {ge_info['吉凶']} {luck_symbol}")
        
        output.append("\n【三才配置】得分：{}".format(score_data["三才得分"]))
        sancai_info = score_data["三才详情"]
        output.append(f"  {sancai_info['三才']} - {sancai_info['评价']}")
        
        output.append("\n【文化深度解析】")
        output.append(culture_analysis)
        
        return "\n".join(output)


def main():
    print("=" * 60)
    print("三才五格智能取名系统 V3.1 (离线增强版)")
    print("=" * 60)
    
    surname = input("\n请输入姓氏：").strip()
    if not surname: return
    
    gender = input("请输入性别（男/女）：").strip()
    if gender not in ["男", "女"]: return
    
    print("\n提示：支持五行（金、木、水、火、土），最多输入2个，空格分隔。")
    xiyongshen_str = input("请输入喜用神（可选）：").strip()
    xiyongshen = xiyongshen_str.split() if xiyongshen_str else []
    
    count = input("请输入生成名字数量（默认 5）：").strip()
    count = int(count) if count.isdigit() else 5
    
    generator = NamingGenerator(surname, gender, xiyongshen=xiyongshen)
    results = generator.generate_names(count)
    
    if not results:
        print("\n抱歉，未能生成符合条件的名字。")
        return
    
    for i, name_data in enumerate(results, 1):
        print(generator.format_result(name_data, i))
    
    save_option = input("\n\n是否保存结果到文件？(y/n): ").strip().lower()
    if save_option == 'y':
        filename = f"取名结果_{surname}{gender}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"三才五格智能取名系统 V3.1 报告\n姓氏：{surname} 性别：{gender}\n")
            for i, name_data in enumerate(results, 1):
                f.write(generator.format_result(name_data, i) + "\n")
        print(f"\n结果已保存到：{filename}")


if __name__ == "__main__":
    main()
