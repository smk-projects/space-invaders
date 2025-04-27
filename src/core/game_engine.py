import pygame
from core.screen.screen_manager import ScreenManager
from core.screen.game_play import GamePlayScreen
from core.screen.startup import StartupScreen
from core.screen.game_over import GameOverScreen
from core.screen.enums import ScreenState
from core.screen.level_start import LevelStartScreen
from core.game_state import game_state, reset_state
from core.settings.level_setting import level_count

class GameEngine:
    """
    遊戲主程式
    """
    def __init__(self):
        pass

    def start(self):
        pygame.init()
        pygame.display.set_caption("Space Invaders")        
        
        scrmgr = ScreenManager.instance()        
        state = ScreenState.STARTUP
        
        game_state.current_level = 1
        
        while state != ScreenState.QUIT:
            if state == ScreenState.STARTUP or state == ScreenState.RESET: # 遊戲重置
                reset_state()
                state = scrmgr.display(StartupScreen())
            
            elif state == ScreenState.GAME_START: # 遊戲開始
                state = scrmgr.display(LevelStartScreen())
            
            elif state == ScreenState.GAME_PASS: # 遊戲過關
                if game_state.current_level < level_count():
                    game_state.current_level += 1
                else:
                    game_state.current_level = 1
                state = scrmgr.display(LevelStartScreen())
                
            elif state == ScreenState.GAME_OVER:
                state = scrmgr.display(GameOverScreen())
            
            elif state == ScreenState.GAME_RUNNING: # 遊戲執行中
                state = scrmgr.display(GamePlayScreen())

        pygame.quit() 
