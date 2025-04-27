from core.item.item_base import GameItemBase
from core.config.item_config import GameItemConfig
from core.item.enums import GameItemType
import random
from random import randint

class Star(GameItemBase):
    """
    繪製背景星星
    """
    def __init__(self):
        # 隨機設定星星大小
        star_level = randint(0, 2)        
        star_martixs_list = {
            0: self.general_star(),
            1: self.little_star(),
            2: self.micro_star()
        }
        self._star_martixs = star_martixs_list.get(star_level)
        self.set_speed(1) # 設定星星的閃爍速度
        
        # 隨機設定星星的動畫起始幀數
        super().set_frame(randint(0, len(self._star_martixs) - 1))  
        config = GameItemConfig(
            brush_size=1, 
            item_type=GameItemType.BACKGROUND
        )
        super().__init__(config)
        super().set_brush_color(random.choice(
            [
                (51, 51, 51),   
                (81, 81, 81),    
                (100, 100, 100),    
                (25, 25, 25),      
                (15, 15, 15)      
            ]
        ))  # 隨機設定畫筆顏色
    
    # 一般星星
    def general_star(self):
        return [
            [  # Frame 1 - 最亮
            [0, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 0],
            ],
            [  # Frame 1 - 最亮
            [0, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 0],
            ],
            [  # Frame 2 - 較暗
            [0, 0, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0],
            ],
            [  # Frame 2 - 較暗
            [0, 0, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0],
            ],
            [  # Frame 3 - 最暗
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            ],
            [  # Frame 3 - 最暗
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            ],
            [  # Frame 4 - 漸亮
            [0, 0, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0],
            ],
            [  # Frame 4 - 漸亮
            [0, 0, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0],
            ]
        ]
    
    # 小星星
    def little_star(self):
        return [
            [  # Frame 1 - 最亮
            [0, 1, 1, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 1, 1, 0],
            ],
            [  # Frame 2 - 較暗
            [0, 1, 1, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 1, 1, 0],
            ],
            [  # Frame 3 - 最暗
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            ],
            [  # Frame 4 - 漸亮
            [0, 1, 1, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 1, 1, 0],
            ]
        ]
    
    # 最小顆的星星
    def micro_star(self):
        return [
            [  # Frame 1 - 最亮
                [1, 1],
                [1, 1],
            ],
            [  # Frame 1 - 最亮
                [1, 1],
                [1, 1],
            ],
            [  # Frame 1 - 最亮
                [1, 1],
                [1, 1],
            ],
            [  # Frame 2 - 較暗
                [0, 0],
                [0, 0],
            ],
            [  # Frame 2 - 較暗
                [0, 0],
                [0, 0],
            ],
            [  # Frame 2 - 較暗
                [0, 0],
                [0, 0],
            ],
        ]
    
    # 顯示物品存在時的矩陣
    def alive_martixs(self):        
        return self._star_martixs