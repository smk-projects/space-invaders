from core.item.item_base import GameItemBase
from core.config.item_config import GameItemConfig
from core.item.enums import GameItemType
from core.settings.screen_setting import BRUSH_SIZE
from core.item.enums import GameItemState
from core.item.bullet.enemy_bullet import EnemyBullet
from core.item.bullet.player_bullet import PlayerBullet
from core.settings.game_setting import FRAME_RATE
from core.game_state import game_state
import time

class EnemyBase(GameItemBase):
    """
    敵方角色: 基底類別
    """
    def __init__(self):        
        self.config = GameItemConfig(
            brush_size=BRUSH_SIZE, 
            item_type=GameItemType.ENEMY
        )
        super().__init__(self.config)
        self.__last_fired_time = time.time()
        self.__fire_interval = 1.0  # 開火間隔時間
        self.__fired_bullets: list[EnemyBullet] = []
        self.__bullet_speed = 5 # 預設子彈移動速度
        self.__pause = False # 暫停狀態
        
        self.__enemy_life = 1
        self._remaining_life = self.__enemy_life
    
    @property
    def life(self):
        """
        生命值
        """
        return self._remaining_life
    
    def score(self):
        """
        取得分數
        """
        return 100 * self.__enemy_life
    
    def hit(self, target: GameItemBase):
        """
        被攻擊
        """
        if not super().hit(target):
            return False        
        if target.item_type == GameItemType.BUNKER:
            self.set_state(GameItemState.ALIVE) # 敵人撞擊碉堡沒事            
        return True
    
    def get_hit(self, player_bullet: PlayerBullet):
        """
        受到攻擊
        """
        if not super().get_hit(player_bullet):
            return False
        self._remaining_life -= 1
        
        if self._remaining_life == 1:
            self.set_brush_color((255, 255, 255))
        elif self._remaining_life == 2:
            self.set_brush_color((255, 255, 0))
        elif self._remaining_life >= 3:
            self.set_brush_color((255, 0, 0))
        
        self.draw()
        if self._remaining_life <= 0:
            game_state.player_score += self.score()
            self.set_state(GameItemState.DESTROY)
        else:
            self.set_state(GameItemState.ALIVE)
        return True
    
    def set_life(self, life: int):
        """
        設定生命值
        """
        self.__enemy_life = life
        self._remaining_life = life
    
    def set_bullet_speed(self, speed:float):
        """
        設定子彈速度
        """
        self.__bullet_speed = speed
    
    def can_fire(self):
        """
        判斷是否可以開火
        """
        # 得是活人才能開火
        if not self.item_state == GameItemState.ALIVE:
            return False
        # 一次只能發射一顆子彈
        if len(self.__fired_bullets) != 0:
            return False
        # 每次開火時間都需間隔指定的秒數
        if self.__last_fired_time + self.__fire_interval > time.time():
            return False
        return True
    
    def fire(self, bullet_spped: int):
        """
        開火
        """
        bullet = EnemyBullet()
        if not self.can_fire():
            return None
        
        bullet.set_pos(
            x=self.pos_x + (self.width - bullet.width) // 2,
            y=self.pos_y + self.height
        )
        bullet.set_speed(bullet_spped)
        bullet.draw()
        self.__last_fired_time = time.time()
        self.__fired_bullets.append(bullet)
        return bullet
    
    @property
    def fired_bullets(self):
        """
        取得已發射的子彈
        """
        return self.__fired_bullets
    
    def destroy_matrixs(self):
        """
        定義敵方物件的動畫矩陣
        """
        return [
            # First frame - small core
            [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],

            # Second frame - expanding with transparency
            [
            [0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 1, 1, 2, 0, 0, 0, 0],
            [0, 0, 0, 2, 1, 1, 1, 1, 2, 0, 0, 0],
            [0, 0, 2, 1, 1, 1, 1, 1, 1, 2, 0, 0],
            [0, 0, 2, 1, 1, 1, 1, 1, 1, 2, 0, 0],
            [0, 0, 2, 1, 1, 1, 1, 1, 1, 2, 0, 0],
            [0, 0, 2, 1, 1, 1, 1, 1, 1, 2, 0, 0],
            [0, 0, 0, 2, 1, 1, 1, 1, 2, 0, 0, 0],
            [0, 0, 0, 0, 2, 1, 1, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],

            # Third frame - larger explosion with fading
            [
            [0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0],
            [0, 0, 0, 3, 2, 2, 2, 2, 3, 0, 0, 0],
            [0, 0, 3, 2, 1, 1, 1, 1, 2, 3, 0, 0],
            [0, 3, 2, 1, 1, 1, 1, 1, 1, 2, 3, 0],
            [0, 3, 2, 1, 1, 1, 1, 1, 1, 2, 3, 0],
            [0, 3, 2, 1, 1, 1, 1, 1, 1, 2, 3, 0],
            [0, 3, 2, 1, 1, 1, 1, 1, 1, 2, 3, 0],
            [0, 0, 3, 2, 1, 1, 1, 1, 2, 3, 0, 0],
            [0, 0, 0, 3, 2, 2, 2, 2, 3, 0, 0, 0],
            [0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],

            # Fourth frame - fading out
            [
            [0, 0, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0],
            [0, 0, 4, 3, 3, 3, 3, 3, 3, 4, 0, 0],
            [0, 4, 3, 2, 2, 2, 2, 2, 2, 3, 4, 0],
            [4, 3, 2, 1, 1, 1, 1, 1, 1, 2, 3, 4],
            [4, 3, 2, 1, 1, 1, 1, 1, 1, 2, 3, 4],
            [4, 3, 2, 1, 1, 1, 1, 1, 1, 2, 3, 4],
            [4, 3, 2, 1, 1, 1, 1, 1, 1, 2, 3, 4],
            [0, 4, 3, 2, 2, 2, 2, 2, 2, 3, 4, 0],
            [0, 0, 4, 3, 3, 3, 3, 3, 3, 4, 0, 0],
            [0, 0, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            # Fifth frame - scattered dots
            [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],

            # Sixth frame - fewer scattered dots
            [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],

            # Seventh frame - even fewer scattered dots
            [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],

            # Eighth frame - almost gone
            [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        ]