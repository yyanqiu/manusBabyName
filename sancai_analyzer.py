# -*- coding: utf-8 -*-
"""
三才五行分析模块
分析五行相生相克关系
"""


class SanCaiAnalyzer:
    """三才五行分析器"""
    
    # 五行相生关系
    SHENG_MAP = {
        "木": "火",  # 木生火
        "火": "土",  # 火生土
        "土": "金",  # 土生金
        "金": "水",  # 金生水
        "水": "木"   # 水生木
    }
    
    # 五行相克关系
    KE_MAP = {
        "木": "土",  # 木克土
        "火": "金",  # 火克金
        "土": "水",  # 土克水
        "金": "木",  # 金克木
        "水": "火"   # 水克火
    }
    
    @classmethod
    def is_sheng(cls, element1, element2):
        """
        判断element1是否生element2
        :param element1: 五行1
        :param element2: 五行2
        :return: True/False
        """
        return cls.SHENG_MAP.get(element1) == element2
    
    @classmethod
    def is_ke(cls, element1, element2):
        """
        判断element1是否克element2
        :param element1: 五行1
        :param element2: 五行2
        :return: True/False
        """
        return cls.KE_MAP.get(element1) == element2
    
    @classmethod
    def analyze_sancai(cls, tiange_wuxing, renge_wuxing, dige_wuxing):
        """
        分析三才配置
        :param tiange_wuxing: 天格五行
        :param renge_wuxing: 人格五行
        :param dige_wuxing: 地格五行
        :return: 分析结果字典
        """
        if not all([tiange_wuxing, renge_wuxing, dige_wuxing]):
            return {
                "三才": "未知",
                "评价": "无法分析",
                "详情": "五行信息不完整",
                "得分": 0
            }
        
        sancai = f"{tiange_wuxing}{renge_wuxing}{dige_wuxing}"
        
        # 分析天格与人格的关系
        tian_ren_relation = cls._get_relation(tiange_wuxing, renge_wuxing)
        
        # 分析人格与地格的关系
        ren_di_relation = cls._get_relation(renge_wuxing, dige_wuxing)
        
        # 综合评价
        score = 0
        evaluation = []
        
        # 天格生人格（成功运）
        if tian_ren_relation == "生":
            score += 15
            evaluation.append("天格生人格，成功运佳")
        elif tian_ren_relation == "克":
            evaluation.append("天格克人格，成功运受阻")
        elif tian_ren_relation == "被生":
            score += 5
            evaluation.append("人格泄天格，成功运一般")
        elif tian_ren_relation == "被克":
            evaluation.append("人格克天格，成功运不顺")
        else:
            score += 10
            evaluation.append("天格与人格关系平和")
        
        # 人格生地格（基础运）
        if ren_di_relation == "生":
            score += 15
            evaluation.append("人格生地格，基础运稳固")
        elif ren_di_relation == "克":
            evaluation.append("人格克地格，基础运不稳")
        elif ren_di_relation == "被生":
            score += 5
            evaluation.append("地格泄人格，基础运一般")
        elif ren_di_relation == "被克":
            evaluation.append("地格克人格，基础运受损")
        else:
            score += 10
            evaluation.append("人格与地格关系平和")
        
        # 整体评价
        if score >= 25:
            overall = "大吉"
        elif score >= 20:
            overall = "吉"
        elif score >= 15:
            overall = "中吉"
        elif score >= 10:
            overall = "平"
        else:
            overall = "凶"
        
        return {
            "三才": sancai,
            "评价": overall,
            "详情": "；".join(evaluation),
            "得分": score,
            "天人关系": tian_ren_relation,
            "人地关系": ren_di_relation
        }
    
    @classmethod
    def _get_relation(cls, element1, element2):
        """
        获取两个五行之间的关系
        :param element1: 五行1
        :param element2: 五行2
        :return: "生"/"克"/"被生"/"被克"/"平"
        """
        if cls.is_sheng(element1, element2):
            return "生"
        elif cls.is_ke(element1, element2):
            return "克"
        elif cls.is_sheng(element2, element1):
            return "被生"
        elif cls.is_ke(element2, element1):
            return "被克"
        else:
            return "平"
    
    @classmethod
    def get_best_sancai_combinations(cls):
        """
        获取最佳三才配置组合
        :return: 最佳三才配置列表
        """
        elements = ["木", "火", "土", "金", "水"]
        best_combinations = []
        
        for tian in elements:
            for ren in elements:
                for di in elements:
                    result = cls.analyze_sancai(tian, ren, di)
                    if result["得分"] >= 25:
                        best_combinations.append({
                            "三才": result["三才"],
                            "得分": result["得分"],
                            "评价": result["评价"]
                        })
        
        # 按得分排序
        best_combinations.sort(key=lambda x: x["得分"], reverse=True)
        return best_combinations


def test_sancai():
    """测试三才分析"""
    test_cases = [
        ("金", "木", "水"),  # 李世民的三才
        ("木", "火", "土"),  # 相生配置
        ("金", "金", "金"),  # 同五行
        ("木", "土", "水"),  # 相克配置
    ]
    
    for tian, ren, di in test_cases:
        result = SanCaiAnalyzer.analyze_sancai(tian, ren, di)
        print(f"三才：{result['三才']}")
        print(f"评价：{result['评价']}")
        print(f"详情：{result['详情']}")
        print(f"得分：{result['得分']}/30")
        print("=" * 50)
        print()


if __name__ == "__main__":
    test_sancai()
    
    print("\n最佳三才配置（前10名）：")
    print("=" * 50)
    best = SanCaiAnalyzer.get_best_sancai_combinations()[:10]
    for i, combo in enumerate(best, 1):
        print(f"{i}. {combo['三才']} - {combo['评价']}（{combo['得分']}分）")
