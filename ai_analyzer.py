# -*- coding: utf-8 -*-
"""
离线文化解析模块 (V3.1)
无需 API Key，内置文化数据库提供名字深度寓意分析
"""

import random

class AIAnalyzer:
    """智能文化寓意分析器 (离线版)"""
    
    def __init__(self):
        # 内置诗词库
        self.poems = {
            "木": [
                "“青青子衿，悠悠我心。”——《诗经》",
                "“宁可食无肉，不可居无竹。”——苏轼",
                "“林深时见鹿，溪午不闻钟。”——李白",
                "“芳林新叶催陈叶，流水前波让后波。”——刘禹锡"
            ],
            "火": [
                "“日出江花红胜火，春来江水绿如蓝。”——白居易",
                "“大漠孤烟直，长河落日圆。”——王维",
                "“星垂平野阔，月涌大江流。”——杜甫",
                "“光明磊落，志在四方。”"
            ],
            "土": [
                "“地势坤，君子以厚德载物。”——《易经》",
                "“安得广厦千万间，大庇天下寒士俱欢颜。”——杜甫",
                "“稳如泰山，志存高远。”",
                "“广袤大地，孕育万物。”"
            ],
            "金": [
                "“金就砺则利，君子博学而日参省乎己。”——《荀子》",
                "“大浪淘沙始见金。”——刘禹锡",
                "“锐意进取，无坚不摧。”",
                "“锦绣前程，光辉灿烂。”"
            ],
            "水": [
                "“上善若水，水善利万物而不争。”——《老子》",
                "“海纳百川，有容乃大。”——林则徐",
                "“清泉石上流。”——王维",
                "“浩渺烟波，志向远大。”"
            ]
        }
        
        # 意境模板
        self.templates = [
            "名字“{full_name}”蕴含着深厚的文化底蕴。{char1_desc}，{char2_desc}。二字结合，意境如{mood}，象征着孩子将来{future}。",
            "“{full_name}”一名，既有古典之雅，又不失现代之风。{char1_desc}体现了{char1_virtue}，而{char2_desc}则寓意着{char2_virtue}。整体给人以{feeling}的感觉。",
            "取名“{full_name}”，寄托了父母对孩子{hope}的期许。{char1_desc}与{char2_desc}相得益彰，正如诗云：{poem}。这是一个富有{style}的名字。"
        ]

    def analyze_name(self, surname, name, gender):
        """
        离线分析名字寓意
        """
        from data_characters import get_character_info
        
        full_name = surname + name
        char1 = name[0]
        char2 = name[1] if len(name) > 1 else ""
        
        info1 = get_character_info(char1)
        info2 = get_character_info(char2) if char2 else None
        
        # 提取特征
        wuxing1 = info1["五行"] if info1 else "木"
        wuxing2 = info2["五行"] if info2 else wuxing1
        
        char1_desc = f"“{char1}”字寓意{info1['字义']}" if info1 else f"“{char1}”字象征美好"
        char2_desc = f"“{char2}”字寓意{info2['字义']}" if info2 else ""
        
        char1_virtue = "高尚的品德" if wuxing1 in ["木", "土"] else "卓越的才华"
        char2_virtue = "广阔的胸怀" if wuxing2 in ["水", "火"] else "坚定的意志"
        
        moods = ["清风拂面", "高山流水", "旭日东升", "星光璀璨", "春意盎然"]
        futures = ["前程似锦", "志向远大", "德才兼备", "平安喜乐", "成就非凡"]
        feelings = ["儒雅", "大气", "灵动", "稳重", "清新"]
        hopes = ["聪明伶俐", "健康成长", "事业有成", "品行端正"]
        styles = ["书卷气", "英雄气", "艺术感", "自然美"]
        
        poem = random.choice(self.poems.get(wuxing1, self.poems["木"]))
        
        # 随机选择模板并填充
        template = random.choice(self.templates)
        analysis = template.format(
            full_name=full_name,
            char1_desc=char1_desc,
            char2_desc=char2_desc,
            char1_virtue=char1_virtue,
            char2_virtue=char2_virtue,
            mood=random.choice(moods),
            future=random.choice(futures),
            feeling=random.choice(feelings),
            hope=random.choice(hopes),
            style=random.choice(styles),
            poem=poem
        )
        
        return analysis

if __name__ == "__main__":
    # 简单测试
    analyzer = AIAnalyzer()
    print(analyzer.analyze_name("李", "沐书", "男"))
