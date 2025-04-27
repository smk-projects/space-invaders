from ..item_base import GameItemBase
from core.item.bullet.enemy_bullet import EnemyBullet
from core.item.bullet.player_bullet import PlayerBullet
from core.config.item_config import GameItemConfig
from ..enums import GameItemType, GameItemState, MoveDirection
from core.settings.screen_setting import BRUSH_SIZE
from core.screen.screen_manager import ScreenManager
import pygame, random, math

class Bunker(GameItemBase):
    """
    Bunker: 防禦堡壘
    """
    def __init__(self, brush_size=5, x=0, y=0):
        item_config = GameItemConfig(
            item_type=GameItemType.BUNKER,
            brush_size=2,                        
        )
        super().__init__(item_config)
        self.set_brush_color((0, 255, 100))  # 設定顏色為綠色
        

    def get_hit(self, who: GameItemBase):
        """
        複寫碉堡受到攻擊的效果
        """
        self.set_state(GameItemState.ALIVE) # 碉堡不會死
        bunker_rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        who_rect = pygame.Rect(who.pos_x, who.pos_y, who.width, who.height)
        
        if not bunker_rect.colliderect(who_rect):            
            return False        
        overlap_rect = bunker_rect.clip(who_rect)
        bunker_surf = self.get_surface()
        
        if who.item_type == GameItemType.ENEMY:
            surf_x = overlap_rect.x - self.pos_x
            surf_y = overlap_rect.y - self.pos_y
            bunker_surf.fill((0, 0, 0, 0), pygame.Rect(surf_x, surf_y, overlap_rect.width, overlap_rect.height))
            return True
        
        
        hit_radius = 6  
        fragment_size = 4  
        surf_x = overlap_rect.x - self.pos_x
        loop_range = range(self.pos_y + self.height - 1, self.pos_y - 1, -1)
        if who.direction == MoveDirection.DOWN:
            loop_range = range(self.pos_y, self.pos_y + self.height)
        
        for y in loop_range:
            px = surf_x + hit_radius  
            py = y - self.pos_y

            # 防止超過碉堡範圍
            if py < 0 or py >= self.height:
                continue
            if px < 0 or px >= self.width:
                continue

            color = bunker_surf.get_at((px, py))
            
            # 交疊的區域是非透明色表示擊中
            if color[3] != 0 or len(color) < 4:
                # Define the circular hit area centered at (px, py)
                for frag_x in range(px - hit_radius, px + hit_radius, fragment_size):
                    for frag_y in range(py - hit_radius, py + hit_radius, fragment_size):
                        if frag_x < 0 or frag_x >= self.width or frag_y < 0 or frag_y >= self.height:
                            continue
                        
                        frag_center_x = frag_x + fragment_size // 2
                        frag_center_y = frag_y + fragment_size // 2
                        distance = math.sqrt((frag_center_x - px) ** 2 + (frag_center_y - py) ** 2)
                        if distance <= hit_radius:
                            
                            if random.random() > 0.3: 
                                bunker_surf.fill((0, 0, 0, 0), pygame.Rect(frag_x, frag_y, fragment_size, fragment_size))
                self.move()
                return True
            
        # 命中區都是透明色，表示未命中
        return False
        
    def __bunker_matrixs(self): 
        """
        Bunker 的矩陣
        """
        # 0: empty, 1: full brush, 2-6: grayscale from dark to light
        return [[
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 1, 1, 1, 1, 1, 1],
            [1, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 4, 1, 1, 1, 1, 1],
            [5, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 4, 5, 1, 1, 1, 1],
            [5, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 4, 5, 1, 1, 1, 1],
            [6, 5, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 5, 6, 1, 1, 1, 1]
        ]]
    
    
    def alive_martixs(self):
        return self.__bunker_matrixs()