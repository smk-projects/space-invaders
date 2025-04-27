from core.item.item_base import GameItemBase
from core.config.item_config import GameItemConfig
from core.item.enums import GameItemType
from core.ability_effect import AbilityBase, Shield, Freeze, DoubleBullet
from core.item.bullet.player_bullet import PlayerBullet, PlayerBulletType
import core.settings.game_setting as game_constant
from core.item.enums import GameItemState, MoveDirection
from core.helper import Countdown
import time, pygame
from enum import Enum

class PlayerAbility(Enum):
    """
    玩家持有能力: PlayerAbility
    """
    NORMAL: int = 0
    SHIELD: int = 3  # 防護罩啟用
    FREEZE: int = 4  # 凍結敵人
    DOULBLE: int = 5  # 雙倍傷害
    

class PlayerStatus(Enum):
    """
    玩家狀態: PlayerStatus
    """
    NORMAL: int = 0
    INVINCIBLE: int = 1  # 無敵狀態

class Player(GameItemBase):
    # 子彈冷卻時間 (以幀數為單位)

    """
    玩家角色: 玩家
    """
    def __init__(self, brush_size=5, x=0, y=0):
        self.config = GameItemConfig(
            brush_size=brush_size, 
            init_x=x, 
            init_y=y, 
            item_type=GameItemType.PLAYER
        )
        # 子彈冷卻時間 (秒)
        self.bullet_cooldown = .5
        self.__player_status = PlayerStatus.NORMAL  # 玩家狀態
        self.__fired_bullets = []  # 儲存已發射的子彈        
        self.__player_abilities: dict[PlayerAbility, AbilityBase] = {}  # 升級物品
        self.set_brush_color((255, 255, 255))        
        self.__INVINCIBLE_TIMER = Countdown(5)
        
        
        super().__init__(self.config)

    @property
    def fired_bullets(self):
        """
        取得已發射的子彈
        """
        return self.__fired_bullets
    
    def get_hit(self, who: GameItemBase) -> bool:
        if super().get_hit(who):        
            if self.__player_status == PlayerStatus.INVINCIBLE:
                self.set_state(GameItemState.ALIVE)  # 無敵狀態不會被擊中
            
            shield = self.get_ability(PlayerAbility.SHIELD)
            if shield is not None and shield.power > 0:
                self.set_state(GameItemState.ALIVE) # 有護盾的保護下不會死
                shield.decrease_power()
                if shield.power <= 0:
                    self.remove_upgrade_item(PlayerAbility.SHIELD)
            return True
        return False

    def upgrade(self, ability: PlayerAbility):
        """
        升級玩家
        - ability: 升級類型
        - effect_sec: 升級效果時間
        """
        if self.__player_abilities.get(ability) is not None:
            self.__player_abilities[ability].enable()
            return 
        
        if ability == PlayerAbility.SHIELD:
            self.__player_abilities[ability] = Shield()
        elif ability == PlayerAbility.DOULBLE:
            self.__player_abilities[ability] = DoubleBullet()
        elif ability == PlayerAbility.FREEZE:
            self.__player_abilities[ability] = Freeze()
        
        self.__player_abilities[ability].enable()
        
    def __refresh_abilities_status(self):
        """
        刷新升級物品狀態
        """
        del_keys: list[PlayerAbility] = []
        for key, item in self.__player_abilities.items():
            if item.cooldown_remaining <= 0:
                del_keys.append(key)
                
        for key in del_keys:
            self.remove_upgrade_item(key)                
    
    def get_ability(self, ability_type: PlayerAbility) -> AbilityBase:
        """
        取得升級物品
        """
        if ability_type in self.__player_abilities:
            if self.__player_abilities[ability_type].effect_remaining > 0:                
                return self.__player_abilities[ability_type]            
        return None
    
    def get_abilities(self):
        """
        取得所有升級物品
        """
        return self.__player_abilities
    
    def remove_all_abilities(self):
        """
        移除所有升級物品
        """
        self.__player_abilities.clear()
        
    def remove_upgrade_item(self, upgrade_tpye: PlayerAbility):
        """
        移除升級物品
        """
        if upgrade_tpye in self.__player_abilities:
            self.__player_abilities[upgrade_tpye] = None
            del self.__player_abilities[upgrade_tpye]
    
    def show_shield(self):
        """
        顯示防護罩
        """
        shield = self.get_ability(PlayerAbility.SHIELD)
        if shield is None:
            return
        
        player_rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        shield.show(around_rect=player_rect)
        
        
    def set_invincible(self, invincible_sec: int = 5):
        """time.
        設定無敵狀態
        """
        self.__INVINCIBLE_TIMER = Countdown(invincible_sec)
        self.__INVINCIBLE_TIMER.start()        
        self.__player_status = PlayerStatus.INVINCIBLE                
    
    def move(self, direction: MoveDirection = MoveDirection.STOP, move_pixels: int = 0):
        if self.__player_status == PlayerStatus.INVINCIBLE:
            if self.__INVINCIBLE_TIMER.remaining_seconds <= 0:
                self.__player_status = PlayerStatus.NORMAL
                self.set_opacity(1)  # 恢復正常狀態
            else:
                self.set_opacity(1 if time.time() % 2  == 0 else .2)
        
        self.__refresh_abilities_status()
        super().move(direction, move_pixels)
        self.show_shield()
    
    def fire(self):
        """
        發射子彈
        """
        # 紀錄當前時間
        if self.item_state != GameItemState.ALIVE:
            return None
        
        current_time = time.time()

        # 如果尚未定義上次發射時間，則初始化為 0
        if not hasattr(self, 'last_fire_time'):
            self.last_fire_time = 0

        # 計算時間差
        time_since_last_fire = current_time - self.last_fire_time

        # 如果時間差小於冷卻時間，則不發射子彈
        if time_since_last_fire < self.bullet_cooldown:
            return None
        
        if len(self.__fired_bullets) >= game_constant.MAX_BULLETS:
            return None

        double_bullet = self.get_ability(PlayerAbility.DOULBLE)
        # 更新上次發射時間
        self.last_fire_time = current_time        
        bullet = PlayerBullet(PlayerBulletType.DEFAULT if double_bullet is None else PlayerBulletType.DOUBLE)
        bullet.set_pos(x=self.pos_x, y=self.pos_y - bullet.height)        
        bullet.draw()
        self.__fired_bullets.append(bullet)  # 儲存已發射的子彈
        
        return bullet
    
    def alive_martixs(self):
        """
        定義玩家物件的動畫矩陣
        """
        return [
            [
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 4, 4, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 4, 1, 4, 4, 1, 1, 0, 0],
            [0, 2, 1, 1, 4, 4, 4, 4, 1, 1, 2, 0],
            [3, 2, 1, 1, 4, 4, 4, 4, 1, 1, 2, 3],
            [3, 2, 1, 1, 1, 4, 4, 1, 1, 1, 2, 3],
            [3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3],
            [3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3],
            [3, 2, 1, 0, 0, 0, 0, 0, 0, 1, 2, 3],
            [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3]
            ]
        ]
        
    def destroy_matrixs(self):
        """
        定義玩家物件的動畫矩陣
        """
        return [
            [
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 2, 2, 1, 1, 0, 0, 0],
                [0, 0, 1, 2, 2, 3, 3, 2, 2, 1, 0, 0],
                [0, 1, 2, 3, 3, 4, 4, 3, 3, 2, 1, 0],
                [1, 2, 3, 4, 4, 5, 5, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 5, 0, 0, 5, 4, 3, 2, 1],
                [1, 2, 3, 4, 5, 0, 0, 5, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 5, 5, 4, 4, 3, 2, 1],
                [0, 1, 2, 3, 3, 4, 4, 3, 3, 2, 1, 0],
                [0, 0, 1, 2, 2, 3, 3, 2, 2, 1, 0, 0],
                [0, 0, 0, 1, 1, 2, 2, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
            ],
            [
                [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
                [0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0],
                [1, 2, 3, 3, 2, 1, 1, 2, 3, 3, 2, 1],
                [1, 2, 3, 4, 3, 2, 2, 3, 4, 3, 2, 1],
                [0, 1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 0],
                [0, 0, 1, 2, 5, 0, 0, 5, 2, 1, 0, 0],
                [0, 0, 1, 2, 5, 0, 0, 5, 2, 1, 0, 0],
                [0, 1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 0],
                [1, 2, 3, 4, 3, 2, 2, 3, 4, 3, 2, 1],
                [1, 2, 3, 3, 2, 1, 1, 2, 3, 3, 2, 1],
                [0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0],
                [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0]
            ],
            [
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
                [0, 0, 1, 0, 1, 2, 2, 1, 0, 1, 0, 0],
                [0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0],
                [0, 0, 1, 2, 3, 4, 4, 3, 2, 1, 0, 0],
                [0, 1, 2, 3, 4, 0, 0, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 0, 0, 4, 3, 2, 1, 0],
                [0, 0, 1, 2, 3, 4, 4, 3, 2, 1, 0, 0],
                [0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0],
                [0, 0, 1, 0, 1, 2, 2, 1, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 0],
                [0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0],
                [0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0],
                [0, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 0],
                [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        ]
    
        