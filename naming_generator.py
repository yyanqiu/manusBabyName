# -*- coding: utf-8 -*-
"""
取名生成器主程序 (V3.2 八字增强版)
根据姓氏、性别、出生日期生成推荐名字，集成八字自动计算和喜用神推荐
"""

import datetime
import random
from wuge_calculator import WuGeCalculator
from sancai_analyzer import SanCaiAnalyzer
from data_81_numbers import get_number_luck, get_number_meaning
from data_characters import get_character_info, CHARACTERS
from ai_analyzer import AIAnalyzer
from bazi_calculator import BaZiCalculator  # 新增：导入八字计算模块


class Config:
    """配置常量"""
    SCORE_THRESHOLD_NO_XIYONGSHEN = 75
    SCORE_THRESHOLD_WITH_XIYONGSHEN = 70
    MAX_CANDIDATES = 200
    MAX_XIYONGSHEN = 2
    MIN_COMMON_USAGE = 3  # 最小常用度
    MAX_NAME_COUNT = 10   # 默认生成名字数量
    
    # 搜索限制
    MAX_SEARCH_PREFERRED = 5000   # 优先搜索最大次数
    MAX_SEARCH_OTHER = 10000      # 其他搜索最大次数
    
    # 评分相关
    MAX_MEANING_SOUND_SCORE = 20  # 字义音韵最大得分
    WUGE_SCORE_PER_GOOD = 8       # 五格每吉得分
    BAXI_SCORE_BASE = 5           # 八字基础得分
    BAXI_SCORE_ONE_MATCH = 5      # 八字一个匹配得分
    BAXI_SCORE_TWO_MATCH = 10     # 八字两个匹配得分


class NamingGenerator:
    """取名生成器"""
    
    def __init__(self, surname, gender, birthdate=None, xiyongshen=None, bazi_analysis=None):
        """
        初始化
        :param surname: 姓氏
        :param gender: 性别（"男"/"女"）
        :param birthdate: 出生日期（可选，用于八字分析）
        :param xiyongshen: 喜用神列表（可选，如 ["金", "水"]）
        :param bazi_analysis: 八字分析结果（可选）
        """
        self.surname = surname
        self.gender = gender
        self.birthdate = birthdate
        self.xiyongshen = xiyongshen if xiyongshen else []
        self.bazi_analysis = bazi_analysis
        self.ai_analyzer = AIAnalyzer()
        
        # 获取姓氏笔画
        surname_info = get_character_info(surname[0]) if len(surname) > 0 else None
        self.surname_stroke = surname_info["笔画"] if surname_info else None
        
        # 如果提供了出生日期但没有喜用神，自动计算八字和喜用神
        if birthdate and not xiyongshen:
            self._auto_calculate_xiyongshen()
    
    def _auto_calculate_xiyongshen(self):
        """自动计算八字和喜用神"""
        try:
            if isinstance(self.birthdate, str):
                # 解析日期字符串
                try:
                    year, month, day = map(int, self.birthdate.split('-'))
                except ValueError as e:
                    print(f"日期格式错误：{e}")
                    print("请使用YYYY-MM-DD格式，例如：2024-01-15")
                    print("将使用默认设置（不限制五行）")
                    return
            elif isinstance(self.birthdate, datetime.date):
                # 已经是date对象
                year, month, day = self.birthdate.year, self.birthdate.month, self.birthdate.day
            else:
                print("无效的出生日期格式")
                return
            
            # 验证日期范围
            if year < 1900 or year > 2100:
                print(f"年份{year}超出计算范围（1900-2100）")
                print("将使用默认设置（不限制五行）")
                return
            
            if month < 1 or month > 12:
                print(f"月份{month}无效")
                print("将使用默认设置（不限制五行）")
                return
            
            # 计算当月最大天数
            import calendar
            max_day = calendar.monthrange(year, month)[1]
            if day < 1 or day > max_day:
                print(f"日期{day}无效，{year}年{month}月最多有{max_day}天")
                print("将使用默认设置（不限制五行）")
                return
            
            # 计算八字
            self.bazi_analysis = BaZiCalculator.analyze_bazi(year, month, day)
            
            # 使用推荐的喜用神
            if self.bazi_analysis and "推荐喜用神" in self.bazi_analysis:
                self.xiyongshen = self.bazi_analysis["推荐喜用神"]
                print(f"根据八字分析，自动推荐喜用神：{', '.join(self.xiyongshen)}")
                
        except ImportError as e:
            print(f"八字计算模块导入失败：{e}")
            print("请确保bazi_calculator.py文件存在且可导入")
            print("将使用默认设置（不限制五行）")
        except AttributeError as e:
            print(f"八字计算模块方法调用失败：{e}")
            print("请检查bazi_calculator.py中的BaZiCalculator类定义")
            print("将使用默认设置（不限制五行）")
        except Exception as e:
            print(f"八字计算发生未知错误：{e}")
            print("将使用默认设置（不限制五行）")
    
    def generate_names(self, count=Config.MAX_NAME_COUNT):
        """
        生成推荐名字列表（优化版）
        :param count: 生成数量
        :return: 名字列表（已评分排序）
        """
        # 预筛选符合条件的字
        filtered_chars = []
        for char, info in CHARACTERS.items():
            if (self.gender in info["性别"] and 
                info["常用度"] >= Config.MIN_COMMON_USAGE):
                filtered_chars.append((char, info))
        
        if not filtered_chars:
            print("没有找到符合条件的字")
            return []
        
        # 根据喜用神分组（优化筛选）
        preferred_chars = []
        other_chars = []
        
        for char, info in filtered_chars:
            if self.xiyongshen and info["五行"] in self.xiyongshen:
                preferred_chars.append((char, info))
            else:
                other_chars.append((char, info))
        
        # 增加随机性
        random.shuffle(preferred_chars)
        random.shuffle(other_chars)
        
        # 限制搜索范围，提高性能
        max_search = min(100, len(filtered_chars))
        preferred_chars = preferred_chars[:max_search]
        other_chars = other_chars[:max_search]
        
        candidates = []
        search_count = 0
        
        # 优先使用喜用神匹配的字
        for char1, info1 in preferred_chars:
            for char2, info2 in filtered_chars:
                if char1 == char2:
                    continue
                    
                # 检查第二个字是否适合该性别和常用度
                if (self.gender not in info2["性别"] or 
                    info2["常用度"] < Config.MIN_COMMON_USAGE):
                    continue
                
                # 喜用神匹配检查
                if self.xiyongshen:
                    if len(self.xiyongshen) == 2:
                        match1 = info1["五行"] in self.xiyongshen
                        match2 = info2["五行"] in self.xiyongshen
                        if not (match1 or match2):
                            continue
                    else:
                        if (info1["五行"] not in self.xiyongshen and 
                            info2["五行"] not in self.xiyongshen):
                            continue
                
                # 生成完整姓名
                full_name = self.surname + char1 + char2
                
                # 计算评分
                score_result = self.evaluate_name(full_name)
                
                # 使用配置常量
                threshold = (Config.SCORE_THRESHOLD_WITH_XIYONGSHEN 
                           if self.xiyongshen else Config.SCORE_THRESHOLD_NO_XIYONGSHEN)
                
                if score_result["总分"] >= threshold:
                    candidates.append({
                        "姓名": full_name,
                        "名字": char1 + char2,
                        "评分": score_result
                    })
                
                search_count += 1
                if (len(candidates) >= Config.MAX_CANDIDATES or 
                    search_count >= Config.MAX_SEARCH_PREFERRED):  # 限制总搜索次数
                    break
            
            if (len(candidates) >= Config.MAX_CANDIDATES or 
                search_count >= Config.MAX_SEARCH_PREFERRED):
                break
        
        # 如果喜用神匹配的字不够，再搜索其他字
        if len(candidates) < count * 2 and search_count < Config.MAX_SEARCH_PREFERRED:
            for char1, info1 in other_chars:
                for char2, info2 in filtered_chars:
                    if char1 == char2:
                        continue
                        
                    if (self.gender not in info2["性别"] or 
                        info2["常用度"] < Config.MIN_COMMON_USAGE):
                        continue
                    
                    # 喜用神匹配检查
                    if self.xiyongshen:
                        if len(self.xiyongshen) == 2:
                            match1 = info1["五行"] in self.xiyongshen
                            match2 = info2["五行"] in self.xiyongshen
                            if not (match1 or match2):
                                continue
                        else:
                            if (info1["五行"] not in self.xiyongshen and 
                                info2["五行"] not in self.xiyongshen):
                                continue
                    
                    full_name = self.surname + char1 + char2
                    score_result = self.evaluate_name(full_name)
                    
                    threshold = (Config.SCORE_THRESHOLD_WITH_XIYONGSHEN 
                               if self.xiyongshen else Config.SCORE_THRESHOLD_NO_XIYONGSHEN)
                    
                    if score_result["总分"] >= threshold:
                        candidates.append({
                            "姓名": full_name,
                            "名字": char1 + char2,
                            "评分": score_result
                        })
                    
                    search_count += 1
                    if (len(candidates) >= Config.MAX_CANDIDATES or 
                        search_count >= Config.MAX_SEARCH_OTHER):
                        break
                
                if (len(candidates) >= Config.MAX_CANDIDATES or 
                    search_count >= Config.MAX_SEARCH_OTHER):
                    break
        
        # 按总分排序
        candidates.sort(key=lambda x: x["评分"]["总分"], reverse=True)
        
        # 只取前 count 个进行文化分析
        final_results = candidates[:count]
        
        if final_results:
            print(f"正在进行文化深度解析（共 {len(final_results)} 个名字）...")
            for item in final_results:
                item["文化解析"] = self.ai_analyzer.analyze_name(
                    self.surname, item["名字"], self.gender
                )
        
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
                wuge_score += Config.WUGE_SCORE_PER_GOOD
        
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
                    score += 5  # 音韵差异加分，这个值较小且固定，不需要配置常量
        return min(score, Config.MAX_MEANING_SOUND_SCORE)
    
    def _calculate_bazi_score(self, name):
        """计算八字匹配得分"""
        if not self.xiyongshen:
            return Config.BAXI_SCORE_BASE
        
        wuxing_list = []
        for char in name:
            char_info = get_character_info(char)
            if char_info:
                wuxing_list.append(char_info["五行"])
        
        if not wuxing_list: return 0
        
        if len(self.xiyongshen) == 2:
            match_count = sum(1 for wx in wuxing_list if wx in self.xiyongshen)
            unique_matches = len(set(wx for wx in wuxing_list if wx in self.xiyongshen))
            if unique_matches == 2: return Config.BAXI_SCORE_TWO_MATCH
            if match_count >= 1: return Config.BAXI_SCORE_ONE_MATCH
        else:
            match_count = sum(1 for wx in wuxing_list if wx in self.xiyongshen)
            if match_count == 2: return Config.BAXI_SCORE_TWO_MATCH
            if match_count == 1: return Config.BAXI_SCORE_ONE_MATCH
            
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
        
        # 显示八字信息（如果有）
        if self.bazi_analysis:
            output.append(f"【八字信息】{self.bazi_analysis['八字字符串']}")
            output.append(f"【日主五行】{self.bazi_analysis['日主']}（{self.bazi_analysis['日主五行']}）")
            output.append(f"【喜用神】{', '.join(self.xiyongshen) if self.xiyongshen else '未指定'}")
        
        output.append("\n【五格分析】得分：{}".format(score_data["五格得分"]))
        wuge_details = score_data["五格详情"]
        for ge_name in ["天格", "人格", "地格", "总格", "外格"]:
            ge_info = wuge_details[ge_name]
            luck_symbol = "✓" if ge_info["吉凶"] == "吉" else "✗"
            output.append(f"  {ge_name}：{ge_info['数值']}（{ge_info['五行']}）- {ge_info['吉凶']} {luck_symbol}")
        
        output.append("\n【三才配置】得分：{}".format(score_data["三才得分"]))
        sancai_info = score_data["三才详情"]
        output.append(f"  {sancai_info['三才']} - {sancai_info['评价']}")
        
        output.append("\n【八字匹配】得分：{}".format(score_data["八字得分"]))
        if self.xiyongshen:
            output.append(f"  喜用神匹配度：{score_data['八字得分']}/10分")
        
        output.append("\n【文化深度解析】")
        output.append(culture_analysis)
        
        return "\n".join(output)


def _get_xiyongshen_input(birthdate):
    """
    获取喜用神输入（提取重复逻辑）
    :param birthdate: 出生日期对象或None
    :return: 喜用神列表
    """
    xiyongshen = []
    
    if birthdate:
        use_auto = input("是否根据八字自动计算喜用神？(y/n，默认y)：").strip().lower()
        if use_auto != 'n':
            # 自动计算，返回空列表，让NamingGenerator自动计算
            return []
        else:
            # 手动输入
            print("\n提示：支持五行（金、木、水、火、土），最多输入2个，空格分隔。")
            xiyongshen_str = input("请输入喜用神（可选）：").strip()
            xiyongshen = xiyongshen_str.split() if xiyongshen_str else []
    else:
        print("\n提示：支持五行（金、木、水、火、土），最多输入2个，空格分隔。")
        xiyongshen_str = input("请输入喜用神（可选）：").strip()
        xiyongshen = xiyongshen_str.split() if xiyongshen_str else []
    
    return xiyongshen


def main():
    print("=" * 60)
    print("三才五格智能取名系统 V3.2 (八字增强版)")
    print("=" * 60)
    
    surname = input("\n请输入姓氏：").strip()
    if not surname: return
    
    gender = input("请输入性别（男/女）：").strip()
    if gender not in ["男", "女"]: return
    
    # 新增：输入出生日期
    birthdate_str = input("\n请输入出生日期（YYYY-MM-DD，可选）：").strip()
    birthdate = None
    if birthdate_str:
        try:
            year, month, day = map(int, birthdate_str.split('-'))
            birthdate = datetime.date(year, month, day)
        except:
            print("日期格式错误，将跳过八字分析")
    
    # 使用提取的函数获取喜用神输入
    xiyongshen = _get_xiyongshen_input(birthdate)
    
    count = input("\n请输入生成名字数量（默认 5）：").strip()
    count = int(count) if count.isdigit() else 5
    
    generator = NamingGenerator(surname, gender, birthdate=birthdate, xiyongshen=xiyongshen)
    results = generator.generate_names(count)
    
    if not results:
        print("\n抱歉，未能生成符合条件的名字。")
        print("建议：1. 降低分数要求 2. 减少喜用神限制 3. 扩充字库")
        return
    
    for i, name_data in enumerate(results, 1):
        print(generator.format_result(name_data, i))
    
    save_option = input("\n\n是否保存结果到文件？(y/n): ").strip().lower()
    if save_option == 'y':
        filename = f"取名结果_{surname}{gender}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"三才五格智能取名系统 V3.2 八字增强版报告\n")
            f.write(f"姓氏：{surname} 性别：{gender}\n")
            if birthdate:
                f.write(f"出生日期：{birthdate_str}\n")
            if generator.bazi_analysis:
                f.write(f"八字：{generator.bazi_analysis['八字字符串']}\n")
                f.write(f"日主：{generator.bazi_analysis['日主']}（{generator.bazi_analysis['日主五行']}）\n")
                f.write(f"喜用神：{', '.join(generator.xiyongshen) if generator.xiyongshen else '未指定'}\n")
            f.write("\n")
            for i, name_data in enumerate(results, 1):
                f.write(generator.format_result(name_data, i) + "\n")
        print(f"\n结果已保存到：{filename}")


if __name__ == "__main__":
    main()
