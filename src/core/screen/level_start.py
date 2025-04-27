from core.screen.base import ScreenBase
from core.item.actor.player import Player
from core.screen.enums import ScreenState
import pygame
from core.game_state import game_state
from core.screen.screen_manager import ScreenManager

class LevelStartScreen(ScreenBase):
    """
    遊戲開始畫面
    """
    def __init__(self):        
        super().__init__()
        self.__player_obj = None
        self.__level_surface = None
        self.__player_life_surface = None


    """
    初始化畫面上需要的物件
    """
    def __init_screen_items(self):
        surface = ScreenManager.instance().get_main_surface()
        # 繪製文字
        font = pygame.font.Font(None, 36)  # 使用默認字體，大小為36

        # 目前關卡文字
        self.__level_surface = font.render(f"Level {game_state.current_level}", True, (255, 255, 255)) 

        # 繪製玩家物件，用來計算隻數
        self.__player_obj = Player(brush_size=1)        
        self.__player_obj.draw()
        
        # 目前玩家生命數文字，除了殘機以外，還要加上1隻目前存活的戰機
        self.__player_life_surface = pygame.font.Font(None, 28).render(f" x {game_state.player_life + 1}", True, (255, 255, 255)) 
    
    """
    畫面初始化的時候的設定
    """
    def initialize(self):
        self.__init_screen_items()
    

    """
    畫面更新時的處理
    """
    def next_frame(self, events):
        # 貼上目前關卡的文字
        surface = ScreenManager.instance().get_main_surface()
        level_text_rect = self.__level_surface.get_rect()
        level_text_rect.center = surface.get_rect().center
        level_text_rect.y -= 25
        surface.blit(self.__level_surface, level_text_rect)
        
        # 貼上玩家生命數的資訊        
        life_text_rect = self.__player_life_surface.get_rect()

        player_life_width = self.__player_obj.width + life_text_rect.width        
        self.__player_obj.set_pos(
            x=self.width // 2 - player_life_width // 2,
            y=self.height // 2 - self.__player_obj.height // 2 + 25
        )
        self.__player_obj.move()
        life_text_rect.center = surface.get_rect().center
        life_text_rect.y += 25
        life_text_rect.x = self.__player_obj.pos_x + self.__player_obj.width
        
        surface.blit(self.__player_life_surface, life_text_rect)
        
        # 超過５秒自動進入下一頁
        if self.elapse_seconds > 5:
            return ScreenState.GAME_RUNNING
        
        # 判斷是否有任何按鍵按下
        if self.begin_event_detect:
            for event in events:
                if event.type == pygame.KEYUP:
                    return ScreenState.GAME_RUNNING
        
        
        
    
    