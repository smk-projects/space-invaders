
from core.screen.screen_manager import ScreenManager
from core.config.item_config import GameItemConfig
from core.item.enums import GameItemState, MoveDirection
from abc import ABC, abstractmethod
import numpy as np
import pygame
import time

class GameItemBase: 
    """
    遊戲中物件基底類別
    """
    def __init__(self, config: GameItemConfig):
        self.brush_size = config.brush_size
        self.pos_x = config.init_x
        self.pos_y = config.init_y
        self.item_type = config.item_type
        self.frame = 0
        self.screen_surface = ScreenManager.instance().get_main_surface()
        self.item_state = GameItemState.ALIVE
        self.move_step = 0
        self.move_step_pixels = config.init_speed
        self.direction = MoveDirection.STOP
        self.__brush_color = (255, 255, 255)  # 預設畫筆顏色為白色        
        self.__background_color = (0, 0, 0, 0)  # 預設背景顏色為黑色
        self.item_martix = self.alive_martixs()[0]
        self.__item_surface = None
        self.__opacity = 255        
        self._last_move_time = time.time()
        
    def draw(self):
        self.__item_surface = {
            GameItemState.ALIVE: self.__martixs_to_surfaces(self.alive_martixs()),
            GameItemState.DESTROY: self.__martixs_to_surfaces(self.destroy_matrixs()),
            GameItemState.DESTROYED: self.__martixs_to_surfaces(self.destroyed_matrixs())
        }
        return self
    
    def set_canvas(self, canvas: pygame.Surface):
        """
        設定物件的畫布，若未設定，則直接畫在主螢幕上
        """
        self.screen_surface = canvas
    
    def set_brush_size(self, size: int):
        """
        設定畫筆的大小
        """
        self.brush_size = size
    
    def set_frame(self, frame):
        """
        設定物件的動畫幀數
        """
        self.frame = frame
        
    def set_state(self, state: GameItemState):
        """
        設定物件的狀態
        """
        # 狀態變更，新狀態的動畫要重畫，故 frame 歸零
        self.frame = 0
        self.item_state = state
    
    def set_opacity(self, opacity: float = 0.0):
        """
        設定物件的透明度
        """
        if opacity < 0.0:
            opacity = 0.0
        elif opacity > 1.0:
            opacity = 1.0
        self.__opacity = int(opacity * 255)
    
    @abstractmethod
    def alive_martixs(self):
        """
        定義一組物件動畫矩陣，每個動作由 12X12 的矩陣組成，1 代表畫筆，0 代表畫布
        同時定義一組動畫矩陣序列，每個序列代表一個動作
        """
        pass

    @abstractmethod
    def destroy_matrixs(self):
        """
        定義物件的消失動畫矩陣
        """
        pass
    
    def destroyed_matrixs(self):
        """
        定義物件的消失動畫矩陣
        """
        return [
            np.zeros((12, 12), dtype=int).tolist()
        ]

    def set_brush_color(self, color: tuple):
        """
        定義畫筆顏色，預設為白色
        """
        self.__brush_color = color
        
    def set_background_color(self, color: tuple):
        """
        定義背景顏色，預設為黑色
        """
        self.__background_color = color
            
    def set_speed(self, speed: int):
        """
        定義物件的移動速度，預設為 1，數字越大速度越快
        """
        self.move_step_pixels = speed

    def set_pos(self, x: int, y: int):
        """
        定義物件的初始位置
        """
        self.pos_x = x
        self.pos_y = y

    @property
    def width(self):
        """
        取得物件的寬度
        """
        return len(self.item_martix[0]) * self.brush_size
    
    @property
    def height(self):
        """
        取得物件的高度
        """
        return len(self.item_martix) * self.brush_size
    
    @property
    def state(self):
        """
        取得物件的狀態
        """
        return self.item_state
    
    @property
    def speed(self):
        """
        取得物件的速度
        """
        return self.move_step_pixels
    
    def __martixs_to_surfaces(self, martixs: list) -> list[pygame.Surface]:
        """
        將矩陣轉換為 surface 物件
        """
        if martixs is None:
            return []
        item_surfaces = []
        all_rects: list[pygame.Rect] = []
        for martix in martixs:
            item_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            item_surface.fill(self.__background_color)
            frame_rects = []
            top, left = 0, 0
            for row in martix:
                top += self.brush_size
                left = 0    
                for cell in row:
                    
                    cell_color = self.__background_color
                    if cell == 1: 
                        cell_color = self.__brush_color 
                    elif cell == 0: 
                        # cell_color = self.__background_color
                        cell_color = None
                    else:
                        cell_color = tuple(int(c * (1 - (cell / 10))) for c in self.__brush_color[:3])
    
                    left += self.brush_size
                    if cell_color is None:
                        continue
                    rect = pygame.Rect(left, top, self.brush_size, self.brush_size)
                    frame_rects.append(rect)
                    pygame.draw.rect(item_surface, cell_color, rect)                    
            item_surfaces.append(item_surface) 
        return item_surfaces
    
    def get_surface(self) -> pygame.surface:
        """
        取得物件的 surface
        """
        if self.item_state in self.__item_surface:
            return self.__item_surface[self.item_state][self.frame]
        return None
    
    # 由子類別定義擊中後的行為
    def hit(self, target: 'GameItemBase') -> bool:
        """        
        若擊中目標，則回傳 True，否則回傳 False
        """
        if self.state in [GameItemState.DESTROYED, GameItemState.DESTROY]:
            return False
        if target.get_hit(self):
            # 互相撞擊，所以撞擊的一方也毀掉
            self.set_state(GameItemState.DESTROY)
            return True
        return False
    
    def get_hit(self, who: 'GameItemBase' = None):
        """
        若判定被擊中，則回傳 True
        預設是若已經死亡狀態，則直接視為未擊中
        若仍是存活狀態被擊中，則設定為死亡狀態
        """
        # Create rects for self and the target who
        if self.state in [GameItemState.DESTROYED, GameItemState.DESTROY]:
            return False
            
        self_rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        who_rect = pygame.Rect(who.pos_x, who.pos_y, who.width, who.height)

        # Check if the rects collide
        if self_rect.colliderect(who_rect):
            self.set_state(GameItemState.DESTROY)
            return True
        return False

    def __move_surface(self):
        """
        移動物件的 surface
        """
        if self.item_state not in self.__item_surface:
            return
        surf = self.__item_surface[self.item_state][self.frame]
        if surf.get_alpha() != self.__opacity:
            surf.set_alpha(self.__opacity)
        self.screen_surface.blit(surf, (self.pos_x, self.pos_y))

    def move(self, direction: MoveDirection = MoveDirection.STOP, move_pixels: int = 0):
        """
        定義物件的移動方向
        """
        self.direction = direction
        if move_pixels <= 0:
            move_pixels = self.move_step_pixels
        
        match direction:
            case MoveDirection.LEFT:
                self.pos_x -= move_pixels
            case MoveDirection.RIGHT:
                self.pos_x += move_pixels
            case MoveDirection.UP:
                self.pos_y -= move_pixels
            case MoveDirection.DOWN:
                self.pos_y += move_pixels
            case MoveDirection.UP_LEFT:
                self.pos_x -= move_pixels
                self.pos_y -= move_pixels
            case MoveDirection.UP_RIGHT:
                self.pos_x += move_pixels
                self.pos_y -= move_pixels
            case MoveDirection.DOWN_LEFT:
                self.pos_x -= move_pixels
                self.pos_y += move_pixels
            case MoveDirection.DOWN_RIGHT:
                self.pos_x += move_pixels
                self.pos_y += move_pixels
            case MoveDirection.STOP:
                self.pos_x = self.pos_x
                self.pos_y = self.pos_y
        
        # 物件移動時，動畫偵數也要變化
        #if self.move_step < (self.move_step_pixels * (10 / self.move_step_pixels)):
        now = time.time()
        if now - self._last_move_time > (.1 / self.speed):
            self.frame += 1
            self._last_move_time = now

        if self.item_state in self.__item_surface:
            if self.frame >= len(self.__item_surface[self.item_state]):
                if self.item_state == GameItemState.DESTROY:
                    self.set_state(GameItemState.DESTROYED)
                else:
                    self.frame = 0
            
        self.__move_surface()