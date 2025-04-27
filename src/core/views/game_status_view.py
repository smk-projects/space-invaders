from .view_base import ViewBase
from .view_config import ViewConfig
from core.item.item_base import GameItemBase
from core.screen.game_play_constant import EDGE_TOP, EDGE_BOTTOM
from core.game_state import game_state
from core.item.actor import Player
import core.item.abilities as ability_icons
import core.ability_effect as ability_effect
from core.views.enums import SurfaceAlign
from core.screen.screen_manager import ScreenManager
from core.ability_effect import AbilityBase
import pygame

class GameStatusView(ViewBase):
    """
    遊戲狀態視圖: GameStatusView
    """
    def __init__(self):
        scrmgr = ScreenManager.instance()
        scr_rect = scrmgr.get_main_surface().get_rect()
        padding = 10
        view_config = ViewConfig(
            width=scr_rect.width,
            height=scr_rect.height - EDGE_BOTTOM,
            padding_left=padding,
            padding_right=padding,
            padding_top=padding,
            padding_bottom=padding,
            background=(0, 0, 0),
            x=0,
            y=EDGE_BOTTOM
        )
        super().__init__(view_config)
        self.__active_ability: AbilityBase = None  # 當前啟用的能力
        self.update()
    
    def ability_active(self, ability: AbilityBase) -> None:
        """
        啟用能力的狀態
        """
        if ability is None:
            self.__active_ability = None
            return
        if ability.cooldown_remaining <= 0:
            self.__active_ability = None
        else: 
            self.__active_ability = ability
        
    
    def ability_active_surf(self) -> None:        
        # 設定為同時只能啟用一種能力
        if self.__active_ability is None:
            return None
        
        if self.__active_ability.cooldown_remaining <= 0:
            return None
        
        ability_icon: GameItemBase = None
        if isinstance(self.__active_ability, ability_effect.Shield):
            ability_icon = ability_icons.Shield(brush_size=2)
        elif isinstance(self.__active_ability, ability_effect.DoubleBullet):
            ability_icon = ability_icons.DoubleBullet(brush_size=2)
        elif isinstance(self.__active_ability, ability_effect.Freeze):
            ability_icon = ability_icons.Freeze(brush_size=2)

        view_surf = self._surface
        
        # 進度條的矩形
        progress_bar_rect = pygame.Rect(0, 0,  view_surf.get_rect().width // 6, view_surf.get_rect().height * .8)
        
        # 效果持續剩餘時間
        effect_remaining_rect = pygame.Rect(
            0, 0,  
            int(progress_bar_rect.width * (self.__active_ability.effect_remaining / self.__active_ability.effect_seconds)), 
            progress_bar_rect.height
        )
        
        # 能量冷卻剩餘時間
        cooldown_remaining_rect = pygame.Rect(
            0, 0,  
            int(progress_bar_rect.width * (self.__active_ability.cooldown_remaining / self.__active_ability.cooldown_seconds)), 
            progress_bar_rect.height
        )        
        padding = int(ability_icon.width * .5)
        
        progress_surf = pygame.Surface((
            ability_icon.width + progress_bar_rect.width + padding, 
            progress_bar_rect.height
        ), pygame.SRCALPHA)

        # 繪製進度條
        for index, rect in enumerate([progress_bar_rect, progress_bar_rect, cooldown_remaining_rect, effect_remaining_rect]):
            rect = rect.copy()
            rect.center = progress_surf.get_rect().center
            # rect.centerx += ability_icon.width + padding
            rect.x = ability_icon.width + padding            
            if index != 1: # 扣除邊框
                rect.width -= 2
                rect.height -= 2
                rect.x += 1
                rect.y += 1
            
            background = (0, 0, 0, 0)  # Transparent background
            if index == 1: # 繪製白色邊框
                background = (255, 255, 255)
            if index == 2:
                background = (255, 0, 0, 64)
            elif index == 3:
                background = (0, 255, 0, 64)
            
            pygame.draw.rect(
                progress_surf,
                background,  # White color for the progress bar border
                rect,
                1 if index == 1 else 0  # Border thickness
            )

        # 繪製能力的 ICON
        ability_icon.set_canvas(progress_surf)
        ability_icon.set_pos(
            x=0,
            y=(progress_surf.get_rect().height - ability_icon.height) // 2
        )
        ability_icon.draw()
        ability_icon.move()
        
        return progress_surf

    def upgrade_items_surf(self) -> pygame.surface:
        """
        畫出升級物品
        """
        font = pygame.font.Font(None, 18)
        upgrade_items: GameItemBase = [
            ability_icons.DoubleBullet(brush_size=1),
            ability_icons.Shield(brush_size=1),
            ability_icons.Freeze(brush_size=1)
        ]
        
        hotkey_gap = upgrade_items[0].width * 0.5
        item_gap = upgrade_items[0].width
        
        
        upgrade_labels: pygame.surface = []
        for i, item in enumerate(upgrade_items):
            upgrade_labels.append(
                font.render(f"{i+1}:", True, (255, 255, 255))
            )
            
        upgrade_surf = pygame.Surface((
                (upgrade_items[0].width + upgrade_labels[0].get_rect().width + hotkey_gap + item_gap) * len(upgrade_items), 
                upgrade_items[0].height
            ), 
            pygame.SRCALPHA
        )
        
        x = 0
        for i, item in enumerate(upgrade_items):
            upgrade_surf.blit(
                upgrade_labels[i],
                (x, 0)
            )
            x += upgrade_labels[i].get_rect().width
            
            item.set_canvas(upgrade_surf)
            item.set_pos(
                x=x,
                y=0
            ) 
            x += item.width + item_gap
            item.draw()
            item.move()
            
        return upgrade_surf
    
    def player_life_surf(self) -> pygame.surface:
        player = Player(brush_size=1)
        gap = player.width * 1.5
        plyr_surf_w = (player.width + gap) * game_state.player_life
        if plyr_surf_w <= 0:
            plyr_surf_w = player.width
        plyr_surf_h = player.height
        plyr_surf = pygame.Surface((plyr_surf_w, plyr_surf_h), pygame.SRCALPHA)
        
        # 繪製玩家的生命數，最多繪製9機
        for _ in range(0, min(game_state.player_life, 10)):
            # 畫出玩家的生命
            player = Player(brush_size=1)            
            player.set_canvas(plyr_surf)
            player.set_pos(
                x=gap * _,
                y=0
            )
            player.draw()            
            player.move()
        return plyr_surf  
    
    def update(self):
        """
        更新遊戲狀態視圖
        """
        self._surface.fill((0, 0, 0))  # Clear the surface with a transparent background
        pygame.draw.line(
            self._surface,
            (255, 255, 255),  
            (0, 0),  
            (self._surface.get_rect().width, 0), 
            1
        )
        plyr_surf = self.player_life_surf()
        
        ability_surf = self.ability_active_surf()
        if (ability_surf is None):
            ability_surf = self.upgrade_items_surf()
            
        self.put_surface(plyr_surf, align=SurfaceAlign.LEFT)
        self.put_surface(ability_surf, align=SurfaceAlign.CENTER)
        
    def draw(self):
        """
        因為需依升級狀態顯示內容，所以要覆寫 draw() 方法
        """
        self.update()
        super().draw()