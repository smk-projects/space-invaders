from core.item.item_base import GameItemBase
from core.config.item_config import GameItemConfig
from core.item.enums import GameItemType
import random
import numpy as np

class Planet(GameItemBase):
    def __init__(self, brush_size=5, x=0, y=0):
        self.config = GameItemConfig(
            brush_size=1, 
            item_type=GameItemType.BACKGROUND
        )
        self._planet = None
        super().__init__(self.config)   
        
        planet_colors = [
            (200, 160, 120),  # Warm sandy
            (140, 180, 200),  # Cool blue-gray
            (180, 140, 100),  # Terra cotta
            (120, 120, 160),  # Purple-gray
            (200, 140, 140),  # Pink-red
            (130, 180, 130),  # Sage green
            (160, 120, 180),   # Purple
            (220, 130, 90),   # Rust orange
            (100, 170, 160),  # Teal
            (190, 180, 120),  # Pale gold
            (150, 150, 120),  # Olive gray
            (100, 140, 170),  # Steel blue
            (170, 110, 90),   # Rusty brown
            (90, 150, 110),   # Forest green
            (210, 180, 140),  # Tan
            (130, 100, 80),   # Dark brown
            (180, 190, 200)   # Silver gray
        ]
        adj_ratio = 0.2
        planet_colors = [(int(r * adj_ratio), int(g * adj_ratio), int(b * adj_ratio)) for r,g,b in planet_colors]
        
        planet_color = random.choice(planet_colors)  
        super().set_background_color((0, 0, 0, 0))  # 背景顏色為透明色
        super().set_brush_color(planet_color)  # 隨機設定畫筆顏色
        
    # 隨機建立行星
    def alive_martixs(self):
        if self._planet is not None:
            return self._planet
        
        size = random.randint(64, 256)
        matrix = np.zeros((size, size), dtype=int)

        # 基本設定
        cx, cy = size // 2, size // 2
        radius = size // 2 - 4

        # 畫出完整圓形行星
        for y in range(size):
            for x in range(size):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                    matrix[y][x] = 1

        num_craters = random.randint(60, 100)
        for _ in range(num_craters):
            crater_radius = random.randint(size // 60, size // 20)
            angle = random.uniform(0, 2 * np.pi)
            r = random.uniform(0, radius - crater_radius - 1)

            crater_cx = int(cx + r * np.cos(angle))
            crater_cy = int(cy + r * np.sin(angle))
            crater_depth = random.choice([2, 3])

            for y in range(crater_cy - crater_radius, crater_cy + crater_radius + 1):
                for x in range(crater_cx - crater_radius, crater_cx + crater_radius + 1):
                    if 0 <= x < size and 0 <= y < size:
                        if (x - crater_cx)**2 + (y - crater_cy)**2 <= crater_radius**2:
                            if (x - cx)**2 + (y - cy)**2 <= radius**2:  # 必須在行星圓形內
                                matrix[y][x] = crater_depth

        shadow_redux_period = int(size * 0.2)
        decreasing_unit = int(size * .04)
        shadow_len = int((size // 2) * random.choice([1, 1.2, 1.4, 1.6, .6, .5, .8, .4])) 

        for y in range(size):
            if y % shadow_redux_period == 0:
                shadow_len = shadow_len - decreasing_unit
                
            if y > radius and decreasing_unit > 0:
                decreasing_unit = 0 - decreasing_unit

            if (shadow_len == 0):
                continue
            
            for x in range(shadow_len):                
                if matrix[y][x] == 0: 
                    continue
                
                if matrix[y][x] == 1:
                    matrix[y][x] = 10 - int(10 * (x / shadow_len))      
                else:
                    crater_shadow = matrix[y][x] + 1
                    if (shadow > 10):
                        shadow = 10
                    matrix[y][x] = shadow
                    
        self._planet = [matrix]
        return self._planet
