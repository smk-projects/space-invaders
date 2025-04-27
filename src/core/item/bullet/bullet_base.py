from core.item.item_base import GameItemBase
from core.config.item_config import GameItemConfig
from core.item.enums import GameItemType, GameItemState
import core.settings.screen_setting as scrset
import pygame

class BulletBase(GameItemBase):
    """
    玩家子彈基底類別
    """
    def __init__(self):
        
        self.config = GameItemConfig(
            brush_size=scrset.BRUSH_SIZE,             
            item_type=GameItemType.BULLET
        )
        super().__init__(self.config)
        
    def is_collision(self, target: GameItemBase) -> bool:
        """
        判斷子彈是否與其他物件相撞
        """
        if target.item_state != GameItemState.ALIVE:
            return False
        bullet_rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        target_cw = target.width * 0.6
        target_ch = target.height * 0.6
        target_cx = target.pos_x + (target.width - target_cw) / 2
        target_cy = target.pos_y + (target.height - target_ch) / 2
        center_rect = pygame.Rect(target_cx, target_cy, target_cw, target_ch)
        
        if bullet_rect.colliderect(center_rect):
            return True        
        return False