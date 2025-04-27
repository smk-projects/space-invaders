from core.screen.base import ScreenBase
from core.screen.enums import ScreenState
from core.screen.screen_manager import ScreenManager
from core.helper.countdown import Countdown
from core.game_state import reset_player_life 
import pygame

class GameOverScreen(ScreenBase):
    def __init__(self):
        super().__init__()
        self.continue_counter = 10
        self.__overlay_countdown: Countdown = None
        self.__continue_countdown: Countdown = None
        self.__overlay_surf = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.__deside_state: ScreenState = None
        
    def initialize(self):
        super().initialize()
        self.__overlay_countdown = Countdown(3)
        self.__continue_countdown = Countdown(10)
        self.__continue_countdown.start()
    
    def detect_continue(self, events):
        """
        偵測玩家是否想要接關
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self.__continue_countdown.stop()
                    reset_player_life()
                    return ScreenState.GAME_START
                elif event.key == pygame.K_n:
                    return ScreenState.STARTUP
        return None
    
    def __overlay_fully_shown(self) -> bool:
        """
        繪製遊戲結束的覆蓋層
        """
        if not self.__overlay_countdown.is_running():
            return False
        remaining = self.__overlay_countdown.remaining_seconds
        wait_seconds = self.__overlay_countdown.seconds
        opacity = 255 - int(255 * (remaining / wait_seconds))
        screen_rect: pygame.Rect = ScreenManager.instance().get_main_surface().get_rect()
        self.__overlay_surf = pygame.Surface((screen_rect.width, screen_rect.height), pygame.SRCALPHA)
        self.__overlay_surf.fill((0, 0, 0, opacity))
        ScreenManager.instance().get_main_surface().blit(self.__overlay_surf, (0, 0))
        if remaining <= 0:
            return True
        return False
    
    def next_frame(self, events):
        screen_rect: pygame.Rect = ScreenManager.instance().get_main_surface().get_rect()
        
        gameover_text = pygame.font.Font(None, 74).render("Game Over", True, (255, 0, 0))
        gameover_text_rect = gameover_text.get_rect()
        
        continue_text = pygame.font.Font(None, 36).render(f"Continue ? (Y/n) ({int(self.__continue_countdown.remaining_seconds)})", True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect()
        
        msg_surf = pygame.Surface((screen_rect.width // 2, screen_rect.height // 3), pygame.SRCALPHA)
        msg_surf.fill((0, 0, 0))  # Semi-transparent black background
        msg_surf_rect = msg_surf.get_rect()
        msg_surf_rect.center = (screen_rect.width // 2, screen_rect.height // 2)
        msg_border = pygame.Rect(0, 0, msg_surf_rect.width - 2, msg_surf_rect.height - 2)
        msg_border.center = (msg_surf_rect.centerx, msg_surf_rect.centery)
        pygame.draw.rect(
            msg_surf, 
            (255, 255, 255), 
            msg_border, 
            1
        )
        
        gameover_text_rect.center = (msg_surf_rect.width // 2, msg_surf_rect.height // 2 - 50)
        continue_text_rect.center = (msg_surf_rect.width // 2, msg_surf_rect.height // 2 + 50)
        
        msg_surf.blit(gameover_text, gameover_text_rect)
        msg_surf.blit(continue_text, continue_text_rect)
        
        ScreenManager.instance().get_main_surface().blit(msg_surf, msg_surf_rect)
        
        if self.__deside_state is None:
            self.__deside_state = self.detect_continue(events)
        
        if self.__deside_state is not None and not self.__overlay_countdown.is_running():
            self.__overlay_countdown.start()
            self.__continue_countdown.stop()
        
        if self.__deside_state is not None and self.__overlay_fully_shown():
            return self.__deside_state
        
        
        if self.__continue_countdown.remaining_seconds <= 0:
            return ScreenState.STARTUP
        
        
        
        