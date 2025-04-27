import core.settings.screen_setting as scrset
from core.views.enums import SurfaceAlign
from core.screen.screen_manager import ScreenManager
from .view_config import ViewConfig
import pygame

class ViewBase:
    """
    視圖基底類別: ViewBase
    """
    def __init__(self, config: ViewConfig = None):
        self.view_config = config        
        self._surface = pygame.Surface((config.width, config.height), pygame.SRCALPHA)
        self._surface.fill(config.background)
                
    def put_surface(self, item_surface: pygame.surface, align: SurfaceAlign):
        """
        將 surface 放置在指定位置
        """
        view_rect = self._surface.get_rect()
        item_rect = item_surface.get_rect()
        
        item_rect.center = (view_rect.width // 2, view_rect.height // 2)
        if align == SurfaceAlign.LEFT:
            item_rect.left = self.view_config.padding_left
        elif align == SurfaceAlign.RIGHT:
            item_rect.left = view_rect.width - item_rect.width - self.view_config.padding_right
        self._surface.blit(item_surface, item_rect)
        
    def draw(self):
        """
        畫出視圖
        """
        ScreenManager.instance().get_main_surface().blit(self._surface, (self.view_config.x, self.view_config.y))
        