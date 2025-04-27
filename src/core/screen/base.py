import pygame
from core.settings.screen_setting import *
from core.screen.enums import ScreenState
from abc import ABC, abstractmethod
import core.settings.game_setting as game_setting

# 遊戲螢幕基本類別
class ScreenBase:    
    def __init__(self):
        self.__elapse_seconds = 0.0
        self.__frame_rate = game_setting.FRAME_RATE
        pass    
    
    """
    設定已經過的時間
    """
    def increment_ticks(self):
        self.__elapse_seconds += (1/game_setting.FRAME_RATE)
        
    @property
    def elapse_seconds(self):
        return self.__elapse_seconds        
    
    """
    判斷目前是否可開始偵測事件
    """
    @property
    def begin_event_detect(self) -> bool:
        return self.__elapse_seconds >= 0.5
    
    # 畫面初始化動作
    @abstractmethod
    def initialize(self):
        pass

    # 繪製畫面
    @abstractmethod
    def next_frame(self, events: list[pygame.event.Event]) -> ScreenState:
        pass

    # 螢幕寬度
    @property
    def width(self):        
        return WIDTH
    
    # 螢幕高度
    @property
    def height(self):        
        return HEIGHT
    
    # 畫筆大小
    @property
    def bursh_size(self):        
        return BRUSH_SIZE
    
    
    
    
    