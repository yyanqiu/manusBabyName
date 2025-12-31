# -*- coding: utf-8 -*-
"""
五格计算模块
实现天格、人格、地格、总格、外格的计算
"""

from data_characters import get_character_info


class WuGeCalculator:
    """五格计算器"""
    
    def __init__(self, surname, name):
        """
        初始化
        :param surname: 姓氏（单姓或复姓）
        :param name: 名字（单名或双名）
        """
        self.surname = surname
        self.name = name
        self.surname_strokes = self._get_strokes(surname)
        self.name_strokes = self._get_strokes(name)
        
    def _get_strokes(self, text):
        """
        获取文字的笔画数列表
        :param text: 文字字符串
        :return: 笔画数列表
        """
        strokes = []
        for char in text:
            info = get_character_info(char)
            if info:
                strokes.append(info["笔画"])
            else:
                # 如果字库中没有，使用一个默认值或简单提示
                # 在实际应用中，建议扩充字库或集成笔画查询API
                # 这里为了保证程序不崩溃，返回一个默认笔画（如6画）
                strokes.append(6) 
        return strokes
    
    def calculate_tiange(self):
        """
        计算天格
        单姓：姓氏笔画 + 1
        复姓：两个姓氏笔画相加
        :return: 天格数值
        """
        if not self.surname_strokes:
            return None
            
        if len(self.surname) == 1:
            # 单姓
            return self.surname_strokes[0] + 1
        else:
            # 复姓
            return sum(self.surname_strokes)
    
    def calculate_renge(self):
        """
        计算人格
        单姓单名：姓 + 名
        单姓双名：姓 + 名第一字
        复姓单名：姓第二字 + 名
        复姓双名：姓第二字 + 名第一字
        :return: 人格数值
        """
        if not self.surname_strokes or not self.name_strokes:
            return None
            
        if len(self.surname) == 1:
            # 单姓
            return self.surname_strokes[0] + self.name_strokes[0]
        else:
            # 复姓
            return self.surname_strokes[-1] + self.name_strokes[0]
    
    def calculate_dige(self):
        """
        计算地格
        单名：名字笔画 + 1
        双名：两个名字笔画相加
        :return: 地格数值
        """
        if not self.name_strokes:
            return None
            
        if len(self.name) == 1:
            # 单名
            return self.name_strokes[0] + 1
        else:
            # 双名
            return sum(self.name_strokes)
    
    def calculate_zongge(self):
        """
        计算总格
        姓名所有笔画相加
        :return: 总格数值
        """
        if not self.surname_strokes or not self.name_strokes:
            return None
            
        return sum(self.surname_strokes) + sum(self.name_strokes)
    
    def calculate_waige(self):
        """
        计算外格
        单姓单名：2
        单姓双名：总格 - 人格 + 1
        复姓单名：总格 - 人格 + 1
        复姓双名:总格 - 人格
        :return: 外格数值
        """
        if not self.surname_strokes or not self.name_strokes:
            return None
            
        zongge = self.calculate_zongge()
        renge = self.calculate_renge()
        
        if len(self.surname) == 1 and len(self.name) == 1:
            # 单姓单名
            return 2
        elif len(self.surname) == 2 and len(self.name) == 2:
            # 复姓双名
            return zongge - renge
        else:
            # 其他情况
            return zongge - renge + 1
    
    def get_wuxing(self, number):
        """
        根据数字获取五行属性
        1-2: 木, 3-4: 火, 5-6: 土, 7-8: 金, 9-10: 水
        :param number: 数字
        :return: 五行属性
        """
        if number is None:
            return None
            
        # 只看个位数
        last_digit = number % 10
        if last_digit == 0:
            last_digit = 10
            
        wuxing_map = {
            1: "木", 2: "木",
            3: "火", 4: "火",
            5: "土", 6: "土",
            7: "金", 8: "金",
            9: "水", 10: "水"
        }
        
        return wuxing_map.get(last_digit, None)
    
    def calculate_all(self):
        """
        计算所有五格
        :return: 字典，包含天格、人格、地格、总格、外格及其五行属性
        """
        tiange = self.calculate_tiange()
        renge = self.calculate_renge()
        dige = self.calculate_dige()
        zongge = self.calculate_zongge()
        waige = self.calculate_waige()
        
        return {
            "天格": {
                "数值": tiange,
                "五行": self.get_wuxing(tiange)
            },
            "人格": {
                "数值": renge,
                "五行": self.get_wuxing(renge)
            },
            "地格": {
                "数值": dige,
                "五行": self.get_wuxing(dige)
            },
            "总格": {
                "数值": zongge,
                "五行": self.get_wuxing(zongge)
            },
            "外格": {
                "数值": waige,
                "五行": self.get_wuxing(waige)
            }
        }
    
    def get_sancai(self):
        """
        获取三才配置（天格、人格、地格的五行）
        :return: 三才配置字符串，如"金木水"
        """
        tiange = self.calculate_tiange()
        renge = self.calculate_renge()
        dige = self.calculate_dige()
        
        return f"{self.get_wuxing(tiange)}{self.get_wuxing(renge)}{self.get_wuxing(dige)}"


def test_wuge():
    """测试五格计算"""
    # 测试案例：李世民
    calc = WuGeCalculator("李", "世民")
    result = calc.calculate_all()
    
    print("姓名：李世民")
    print("=" * 50)
    for ge_name, ge_info in result.items():
        print(f"{ge_name}：{ge_info['数值']}（{ge_info['五行']}）")
    print(f"三才：{calc.get_sancai()}")
    print()
    
    # 测试案例：司马懿
    calc2 = WuGeCalculator("司马", "懿")
    result2 = calc2.calculate_all()
    
    print("姓名：司马懿")
    print("=" * 50)
    for ge_name, ge_info in result2.items():
        print(f"{ge_name}：{ge_info['数值']}（{ge_info['五行']}）")
    print(f"三才：{calc2.get_sancai()}")


if __name__ == "__main__":
    test_wuge()
