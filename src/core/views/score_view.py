from .view_base import ViewBase
from core.screen.screen_manager import ScreenManager
from .view_config import ViewConfig
from core.settings.screen_setting import WIDTH, HEIGHT
from core.screen.game_play_constant import EDGE_TOP
from core.game_state import game_state
from core.views.enums import SurfaceAlign
import pygame

class ScoreView(ViewBase):
    """
    分數顯示: 顯示玩家的分數
    """
    def __init__(self, score: int = 0):
        padding = 10
        view_config = ViewConfig(
            width=WIDTH,
            height=EDGE_TOP,
            x = 0,
            y = 0,
            padding_left=padding,
            padding_bottom=padding,
            padding_right=padding,
            padding_top=padding,
            background=(0, 0, 0)
        )
        
        super().__init__(view_config)
        self.update()
        

    def update(self):
        """
        取得分數的 surface
        """
        score_str = f"{game_state.player_score:08d}"
        font = pygame.font.Font(None, int(EDGE_TOP // 1.5))
        text_surface = font.render(f"SCORE: {score_str}", True, (255, 255, 255))
        
        high_score = 0
        high_score_str = f"{high_score:08d}" 
        high_score_surf = font.render(f"HIGH SCORE: {high_score_str}", True, (255, 255, 255))
        
        current_level_str = f"- LEVEL {game_state.current_level:02d} -"
        current_level_surf = font.render(current_level_str, True, (255, 255, 255))
        
        score_surf = pygame.Surface((self._surface.get_width(), self._surface.get_height()), pygame.SRCALPHA)
        score_surf.fill((0, 0, 0))
        
        self.put_surface(text_surface, SurfaceAlign.LEFT)
        self.put_surface(current_level_surf, SurfaceAlign.CENTER)
        self.put_surface(high_score_surf, SurfaceAlign.RIGHT)
        
        pygame.draw.line(
            self._surface,
            (255, 255, 255), 
            (0, EDGE_TOP - 1),  
            (self._surface.get_rect().width, EDGE_TOP - 1), 
            1
        )
        
        