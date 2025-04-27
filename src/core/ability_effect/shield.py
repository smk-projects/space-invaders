from core.screen.screen_manager import ScreenManager
from .ability_base import AbilityBase
import pygame

class Shield(AbilityBase):
    """
    防護罩: Shield
    """
    def __init__(self, keep_sec: int = 20, colldown_sec: int = 20, power: int = 3):
        super().__init__(keep_sec, colldown_sec)
        self.__power = power
        self.__power_init = power
        self.__shield_radius = 5
        self.__surface: pygame.surfae = None
    
    @property
    def power(self):
        """
        取得防護罩的能量
        """
        return self.__power
    
    def update(self, around_rect: pygame.Rect = None):
        """
        更新防護罩
        """
        shield_power = self.__power
        w, h = around_rect.width * 1.2, around_rect.height * 1.2
        radius = int(((w ** 2 + h ** 2) ** 0.5) / 2)
        self.__shield_radius = radius
        shield_opacity = 64
        shield_opacity = int(shield_opacity * (shield_power / self.__power_init))
        shield_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(shield_surface, (0, 255, 0, shield_opacity), (radius, radius), radius, around_rect.width)
        self.__surface = shield_surface
    
    def shield_surface(self, around_rect: pygame.Rect = None) -> pygame.Surface:
        """
        取得防護罩的 surface
        """
        if self.__surface is None:
            self.update(around_rect)
        return self.__surface
    
    def reset(self):
        """
        重置防護罩的能量
        """
        self.__power = self.__power_init
        super().reset()
        
    def decrease_power(self, amount: int = 1):
        """
        降低防護罩的能量
        """
        self.__power = max(0, self.__power - amount)
        if self.__power <= 0:
            self.disable()
    
    def show(self, around_rect: pygame.Rect = None):
        """
        顯示防護罩
        - around_rect: 防護罩包住的矩形範圍
        """
        if self.__power <= 0:
            return
        shield_surface = self.shield_surface(around_rect=around_rect)        
        center = around_rect.center
        ScreenManager.instance().get_main_surface() \
            .blit(shield_surface, (center[0] - self.__shield_radius, center[1] - self.__shield_radius))