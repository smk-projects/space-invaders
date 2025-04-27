import pygame
from pygame import Surface
from core.settings.screen_setting import WIDTH, HEIGHT
from core.screen.enums import ScreenState
from core.screen.base import ScreenBase
from abc import ABC, abstractmethod
from core.game_state import game_state
from core.settings.level_setting import level_count
from typing import Literal

# 遊戲螢幕基本類別
class ScreenManager:    
    __instance = None
    __cls_initialized = False
    
    def __init__(self):
        if not self.__cls_initialized:
            raise Exception(f"{self.__class__.__name__} is a singleton class, call {self.__class__.__name__}.instance() instead.")
        self.__parent_surface: pygame.surface = None
        self.__curent_screen: ScreenBase = None
        self.__surface: pygame.surface = None
        self.__clock: pygame.time.Clock = None
    
    def __init__instance(self):        
        self.__parent_surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.__surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption("Space Invaders")
        self.__clock = pygame.time.Clock()
    
    
    @classmethod
    def instance(cls):
        cls.__cls_initialized = True
        if not cls.__instance:
            cls.__instance = ScreenManager()
            cls.__instance.__init__instance()
        return cls.__instance

    def global_events(self, events: list[pygame.event.Event]) -> Literal['LVUP', 'LVDOWN', 'FULLSCREEN', 'RESET', 'QUIT'] | None :
        """
        全域事件判斷
        """
        for event in events:
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                # 檢測 Ctrl + 上鍵組合                
                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    if event.key == pygame.K_UP:
                        return 'LVUP'
                    elif event.key == pygame.K_DOWN:                        
                        return 'LVDOWN'
                
                # 全螢幕切換 (ALT+ENTER)
                if (keys[pygame.K_LALT] or keys[pygame.K_RALT]) and event.key == pygame.K_RETURN:
                    return 'FULLSCREEN'
                
                # 重置遊戲
                if keys[pygame.K_r]:
                    return 'RESET'
                
                # 按下 ESC 鍵 離開遊戲
                if keys[pygame.K_ESCAPE]:
                    return 'QUIT'
            

            # 檢測按鈕放開事件
            if event.type == pygame.KEYUP:
                
                # 重置遊戲
                if event.key == pygame.K_F11:
                    return 'FULLSCREEN'
            
            # 檢測離開遊戲事件
            if event.type == pygame.QUIT:
                return 'QUIT'
            
    def get_main_surface(self) -> pygame.surface:
        """
        取得主螢幕的 surface
        """
        return self.__surface
    
    def get_current_screen(self) -> ScreenBase:
        """
        取得當前螢幕
        """
        return self.__curent_screen
    
    # 顯示螢幕
    def display(self, screen: ScreenBase) -> ScreenState: 
        self.__curent_screen = screen
        
        self.__surface.fill((0, 0, 0))  # 清空畫面
        screen.initialize()  # 初始化畫面
        
        running = True
        
        pygame.key.stop_text_input()
        screen_state = ScreenState.STARTUP
        f11_pressed = False

        while running:
            screen.increment_ticks()
            events = pygame.event.get()
            
            event = self.global_events(events)
            if event == 'LVUP':
                if game_state.current_level < level_count():
                    game_state.current_level += 1
                return ScreenState.GAME_START
            elif event == 'LVDOWN':
                if (game_state.current_level > 1):
                    game_state.current_level -= 1            
                return ScreenState.GAME_START    
            elif event == 'FULLSCREEN':                
                pygame.display.toggle_fullscreen()
            elif event == 'RESET':
                return ScreenState.RESET
            elif event == 'QUIT':
                running = False
                return ScreenState.QUIT
            
            
            self.__surface.fill((0, 0, 0))
            screen_state = screen.next_frame(events)  # 顯示畫面
            
            # 螢幕置中
            display_info = pygame.display.Info()
            x_offset = (display_info.current_w - WIDTH) // 2
            y_offset = (display_info.current_h - HEIGHT) // 2
            self.__parent_surface.blit(self.__surface, (x_offset, y_offset))

            
            if screen_state is not None:
                running = False
            # 刷新螢幕
            pygame.display.flip()
            self.__clock.tick(60)
            
        return screen_state
        
    