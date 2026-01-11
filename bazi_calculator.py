# -*- coding: utf-8 -*-
"""
八字计算模块
根据出生日期计算四柱八字和五行分析
"""

import datetime

class BaZiCalculator:
    """八字计算器"""
    
    # 天干表
    TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    
    # 地支表
    DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 地支藏干（简化版）
    DI_ZHI_CANG_GAN = {
        "子": ["癸"],
        "丑": ["己", "癸", "辛"],
        "寅": ["甲", "丙", "戊"],
        "卯": ["乙"],
        "辰": ["戊", "乙", "癸"],
        "巳": ["丙", "庚", "戊"],
        "午": ["丁", "己"],
        "未": ["己", "丁", "乙"],
        "申": ["庚", "壬", "戊"],
        "酉": ["辛"],
        "戌": ["戊", "辛", "丁"],
        "亥": ["壬", "甲"]
    }
    
    # 五行对应表
    WU_XING_MAP = {
        "甲": "木", "乙": "木",  # 甲乙为木
        "丙": "火", "丁": "火",  # 丙丁为火
        "戊": "土", "己": "土",  # 戊己为土
        "庚": "金", "辛": "金",  # 庚辛为金
        "壬": "水", "癸": "水",  # 壬癸为水
    }
    
    # 月支表（农历月份对应的地支）
    MONTH_ZHI = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]
    
    # 日柱计算基数表（简化版，实际需要更复杂的计算）
    DAY_BASE = {
        (1900, 1999): 0,
        (2000, 2099): 0,  # 简化处理
    }
    
    @classmethod
    def calculate_year_pillar(cls, year):
        """
        计算年柱
        :param year: 年份（如2024）
        :return: (年干, 年支)
        """
        # 简化计算：以1900年为基准
        base_year = 1900
        gan_index = (year - base_year) % 10
        zhi_index = (year - base_year) % 12
        
        return cls.TIAN_GAN[gan_index], cls.DI_ZHI[zhi_index]
    
    @classmethod
    def calculate_month_pillar(cls, year, month):
        """
        计算月柱
        :param year: 年份
        :param month: 月份（1-12）
        :return: (月干, 月支)
        """
        # 月支固定
        month_zhi = cls.MONTH_ZHI[month - 1]
        
        # 计算月干：根据年干和月份
        year_gan, _ = cls.calculate_year_pillar(year)
        year_gan_index = cls.TIAN_GAN.index(year_gan)
        
        # 月干计算公式：年干序号 * 2 + 月份
        month_gan_index = (year_gan_index * 2 + month) % 10
        month_gan = cls.TIAN_GAN[month_gan_index]
        
        return month_gan, month_zhi
    
    @classmethod
    def calculate_day_pillar(cls, year, month, day):
        """
        计算日柱（标准公式）
        参考：八字日柱计算公式
        :param year: 年份
        :param month: 月份
        :param day: 日期
        :return: (日干, 日支)
        """
        # 标准日柱计算公式
        # 1. 计算当年元旦干支基数
        # 公式：基数 = (年尾二位数+3)*5+55+(年尾二位数-1)/4
        
        year_tail = year % 100  # 年尾二位数
        
        # 计算基数（取整）
        base = (year_tail + 3) * 5 + 55 + (year_tail - 1) // 4
        
        # 2. 计算当年天数（从元旦到指定日期的天数）
        # 先计算当年是否是闰年
        is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        
        # 每月天数（平年）
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if is_leap_year:
            month_days[1] = 29  # 闰年2月29天
        
        # 计算当年天数
        days_of_year = sum(month_days[:month-1]) + day - 1  # -1因为从元旦开始
        
        # 3. 计算总基数
        total_base = base + days_of_year
        
        # 4. 对60取余得到干支序号（0-59）
        ganzhi_index = total_base % 60
        
        # 5. 转换为天干地支（0-9为天干，0-11为地支）
        gan_index = ganzhi_index % 10
        zhi_index = ganzhi_index % 12
        
        return cls.TIAN_GAN[gan_index], cls.DI_ZHI[zhi_index]
    
    @classmethod
    def calculate_hour_pillar(cls, day_gan, hour):
        """
        计算时柱
        :param day_gan: 日干
        :param hour: 小时（0-23）
        :return: (时干, 时支)
        """
        # 时支固定（每2小时一个地支）
        hour_zhi_index = (hour + 1) // 2 % 12
        hour_zhi = cls.DI_ZHI[hour_zhi_index]
        
        # 计算时干：根据日干和时支
        day_gan_index = cls.TIAN_GAN.index(day_gan)
        
        # 时干计算公式：日干序号 * 2 + 时支序号
        hour_gan_index = (day_gan_index * 2 + hour_zhi_index) % 10
        hour_gan = cls.TIAN_GAN[hour_gan_index]
        
        return hour_gan, hour_zhi
    
    @classmethod
    def calculate_bazi(cls, year, month, day, hour=12):
        """
        计算完整的八字
        :param year: 年份
        :param month: 月份
        :param day: 日期
        :param hour: 小时（默认中午12点）
        :return: 八字字典
        """
        year_gan, year_zhi = cls.calculate_year_pillar(year)
        month_gan, month_zhi = cls.calculate_month_pillar(year, month)
        day_gan, day_zhi = cls.calculate_day_pillar(year, month, day)
        hour_gan, hour_zhi = cls.calculate_hour_pillar(day_gan, hour)
        
        return {
            "年柱": f"{year_gan}{year_zhi}",
            "月柱": f"{month_gan}{month_zhi}",
            "日柱": f"{day_gan}{day_zhi}",
            "时柱": f"{hour_gan}{hour_zhi}",
            "年干": year_gan, "年支": year_zhi,
            "月干": month_gan, "月支": month_zhi,
            "日干": day_gan, "日支": day_zhi,
            "时干": hour_gan, "时支": hour_zhi
        }
    
    @classmethod
    def analyze_wuxing_strength(cls, bazi_dict):
        """
        分析八字中的五行强弱
        :param bazi_dict: 八字字典
        :return: 五行统计字典
        """
        wuxing_count = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        
        # 统计天干的五行
        for gan_key in ["年干", "月干", "日干", "时干"]:
            gan = bazi_dict[gan_key]
            wuxing = cls.WU_XING_MAP.get(gan, "")
            if wuxing:
                wuxing_count[wuxing] += 1
        
        # 统计地支的五行（包括藏干）
        for zhi_key in ["年支", "月支", "日支", "时支"]:
            zhi = bazi_dict[zhi_key]
            cang_gans = cls.DI_ZHI_CANG_GAN.get(zhi, [])
            for gan in cang_gans:
                wuxing = cls.WU_XING_MAP.get(gan, "")
                if wuxing:
                    wuxing_count[wuxing] += 0.5  # 藏干权重较低
        
        return wuxing_count
    
    @classmethod
    def recommend_xiyongshen(cls, wuxing_count):
        """
        推荐喜用神
        :param wuxing_count: 五行统计
        :return: 喜用神列表
        """
        # 找出最弱的五行（需要补充的）
        min_count = min(wuxing_count.values())
        weak_elements = [elem for elem, count in wuxing_count.items() 
                        if count == min_count]
        
        # 找出次弱的五行
        sorted_counts = sorted(set(wuxing_count.values()))
        if len(sorted_counts) > 1:
            second_min = sorted_counts[1]
            second_weak = [elem for elem, count in wuxing_count.items() 
                          if count == second_min]
            weak_elements.extend(second_weak)
        
        # 去重
        weak_elements = list(set(weak_elements))
        
        # 根据五行相生关系推荐
        recommended = []
        for elem in weak_elements:
            recommended.append(elem)
            # 如果弱的是木，可以补水（水生木）
            if elem == "木":
                recommended.append("水")
            # 如果弱的是火，可以补木（木生火）
            elif elem == "火":
                recommended.append("木")
            # 如果弱的是土，可以补火（火生土）
            elif elem == "土":
                recommended.append("火")
            # 如果弱的是金，可以补土（土生金）
            elif elem == "金":
                recommended.append("土")
            # 如果弱的是水，可以补金（金生水）
            elif elem == "水":
                recommended.append("金")
        
        # 去重并限制最多2个
        recommended = list(set(recommended))
        return recommended[:2]
    
    @classmethod
    def analyze_bazi(cls, year, month, day, hour=12):
        """
        完整的八字分析
        :param year: 年份
        :param month: 月份
        :param day: 日期
        :param hour: 小时
        :return: 分析结果字典
        """
        # 计算八字
        bazi = cls.calculate_bazi(year, month, day, hour)
        
        # 分析五行强弱
        wuxing_count = cls.analyze_wuxing_strength(bazi)
        
        # 推荐喜用神
        xiyongshen = cls.recommend_xiyongshen(wuxing_count)
        
        # 日主（日干）分析
        ri_zhu = bazi["日干"]
        ri_zhu_wuxing = cls.WU_XING_MAP.get(ri_zhu, "")
        
        return {
            "八字": bazi,
            "五行统计": wuxing_count,
            "日主": ri_zhu,
            "日主五行": ri_zhu_wuxing,
            "推荐喜用神": xiyongshen,
            "八字字符串": f"{bazi['年柱']} {bazi['月柱']} {bazi['日柱']} {bazi['时柱']}"
        }


def test_bazi():
    """测试八字计算"""
    print("=" * 60)
    print("八字计算测试")
    print("=" * 60)
    
    # 测试案例1：2024年1月15日
    print("\n测试案例1：2024年1月15日 12:00")
    result1 = BaZiCalculator.analyze_bazi(2024, 1, 15, 12)
    print(f"八字：{result1['八字字符串']}")
    print(f"日主：{result1['日主']}（{result1['日主五行']}）")
    print(f"五行统计：{result1['五行统计']}")
    print(f"推荐喜用神：{result1['推荐喜用神']}")
    
    # 测试案例2：2000年6月1日
    print("\n测试案例2：2000年6月1日 8:00")
    result2 = BaZiCalculator.analyze_bazi(2000, 6, 1, 8)
    print(f"八字：{result2['八字字符串']}")
    print(f"日主：{result2['日主']}（{result2['日主五行']}）")
    print(f"五行统计：{result2['五行统计']}")
    print(f"推荐喜用神：{result2['推荐喜用神']}")
    
    # 测试案例3：1990年10月10日
    print("\n测试案例3：1990年10月10日 16:00")
    result3 = BaZiCalculator.analyze_bazi(1990, 10, 10, 16)
    print(f"八字：{result3['八字字符串']}")
    print(f"日主：{result3['日主']}（{result3['日主五行']}）")
    print(f"五行统计：{result3['五行统计']}")
    print(f"推荐喜用神：{result3['推荐喜用神']}")


if __name__ == "__main__":
    test_bazi()
