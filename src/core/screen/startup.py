from core.screen.base import ScreenBase
from core.screen.enums import ScreenState
from core.item.background.star import Star
from core.item.background.planet import Planet
from core.item.assets.game_title import GameTitle
import core.settings.screen_setting as scrset
from core.screen.screen_manager import ScreenManager

import pygame
from random import randint

class StartupScreen(ScreenBase):
    """
    啟動畫面: Startup Screen
    """
    def __init__(self):
        super().__init__()
        self.__text_opacity = 255
        self.__text_opacity_step = -10
        self.__opacity_interval = 0
        self.__background_stars: list[Star] = []
        self.__background_planets: list[Planet] = []
        self.__game_title: pygame.surface = None
        self.__game_title_pos_y: int = None
        self.__game_title_move_y_interval: int = 0
        self.__game_title = None
        
    def initialize(self):
        self.__draw_background()
        self.__game_title = GameTitle()
        self.__game_title.set_pos(x=(scrset.WIDTH - self.__game_title.width) // 2, y=scrset.HEIGHT // 4)
        self.__game_title.draw()        
    
    def __draw_background(self):
        # 繪製行星
        plant = Planet(size=512)
        plant.set_pos(
            x=self.width - (plant.width // 2),
            y=self.height - (plant.height // 2)
            
        )
        self.__background_planets.append(plant.draw())
        
        for _ in range(2):
            plant = Planet()
            plant.set_pos(
                x=randint(0, scrset.WIDTH),
                y=randint(0, scrset.HEIGHT)
            )
            self.__background_planets.append(plant.draw())
        
        # 繪製星星
        start_count = randint(100, 255)
        for _ in range(start_count):
            # 隨機產生星星的數量
            random_x = randint(0, scrset.WIDTH)
            random_y = randint(0, scrset.HEIGHT)
            
            star = Star()
            star.set_pos(x=random_x, y=random_y)
            self.__background_stars.append(star.draw())

    def next_frame(self, events: list[pygame.event.Event]) -> ScreenState:
        for star in self.__background_stars:
            star.move()
        for plant in self.__background_planets:
            plant.move()
            
        self.__game_title.move()        
        self.__opacity_interval += 1
        min_opacity, max_opacity = 96, 255

        if (self.__opacity_interval >= 5):
            self.__opacity_interval = 0
            
            self.__text_opacity += self.__text_opacity_step                
            # 避免透明度爆掉
            if (self.__text_opacity < min_opacity):
                self.__text_opacity = min_opacity
            elif (self.__text_opacity > max_opacity):
                self.__text_opacity = max_opacity
            
            if self.__text_opacity <= min_opacity or self.__text_opacity >= max_opacity:                
                self.__text_opacity_step *= -1  # 反轉透明度變化方向
        else:
            self.__opacity_interval += 1
        
        font = pygame.font.Font(None, 36)  
        text = font.render("press [SPACE] to start", True, (255, 255, 255))  
        text.set_alpha(self.__text_opacity)

        # Position text at the bottom 1/3 of the screen
        text_rect = text.get_rect(
            center=(scrset.WIDTH // 2, 
            scrset.HEIGHT - int(scrset.HEIGHT // 3))
        )

        # Draw the text on the screen
        
        ScreenManager.instance().get_main_surface().blit(text, text_rect)
        
        if (self.begin_event_detect):
            for event in events:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    return ScreenState.GAME_START