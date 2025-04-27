from core.item.bullet.bullet_base import BulletBase
from core.item.item_base import GameItemBase
from core.item.enums import GameItemType, GameItemState
from enum import Enum
from dataclasses import dataclass

class PlayerBulletType(Enum):
    """
    玩家子彈類型
    """
    DEFAULT = 0
    DOUBLE = 1,
    LASER = 2 # 程式測試用的強力武器

@dataclass 
class PlayerBulletConfig:
    """
    玩家子彈配置
    """
    bullet_type: PlayerBulletType = PlayerBulletType.DEFAULT
    bullet_speed: float = 10.0
    bullet_amount: int = 1
    power: int = 1
    matrixs: list[list[list[int]]] = None

class PlayerBullet(BulletBase):
    """
    玩家子彈: Bullet
    """
    def __init__(self, bullet_type: PlayerBulletType = PlayerBulletType.DEFAULT):        
        self.__bullet_matrixs = self.default_bullet_matrix()
        super().__init__()
        self.__power = 1
        self.__bullet_config: dict[PlayerBulletType, PlayerBulletConfig] = {
            PlayerBulletType.DEFAULT: PlayerBulletConfig(
                bullet_type=PlayerBulletType.DEFAULT,
                bullet_speed=10.0,
                bullet_amount=1,
                power=1,
                matrixs=self.default_bullet_matrix()
            ),
            PlayerBulletType.DOUBLE: PlayerBulletConfig(
                bullet_type=PlayerBulletType.DOUBLE,
                bullet_speed=20.0,
                bullet_amount=1,
                power=2,
                matrixs=self.double_bullet_matrix()
            ),
            PlayerBulletType.LASER: PlayerBulletConfig(
                bullet_type=PlayerBulletType.LASER,
                bullet_speed=40.0,
                bullet_amount=1,
                power=10,
                matrixs=self.laser_bullet_matrix()
            )
        }
        self.__bullet_type = bullet_type
        self.set_bullet(self.__bullet_type)

    @property
    def bullet_amount(self):
        return self.__bullet_config.bullet_amount

    @property
    def power(self):  
        """
        取得子彈威力
        """
        return self.__power
    
    def decrease_power(self, amount: int = 1):
        """
        減少子彈威力
        
        Args:
            amount: 要減少的威力值，預設為1
        """
        self.__power -= amount
        
        # 如果是雙子彈且威力減為1，切換回預設子彈矩陣
        if self.__power == 1 and self.__bullet_type == PlayerBulletType.DOUBLE:
            self.__bullet_matrixs = self.default_bullet_matrix()
    
    def hit(self, enemy: GameItemBase):
        """
        打到敵人
        """
        if not super().hit(enemy):
            return False
        
        self.__power -= 1
        self.set_state(GameItemState.ALIVE)
        if self.__power <= 0:
            self.set_state(GameItemState.DESTROY)
        return True
        
    def set_bullet(self, bullet_type: PlayerBulletType):
        self.__bullet_type = bullet_type
        self.set_speed(self.__bullet_config[bullet_type].bullet_speed)
        self.__power = self.__bullet_config[bullet_type].power
        self.__bullet_matrixs = self.__bullet_config[bullet_type].matrixs
        if (bullet_type == PlayerBulletType.LASER):
            self.set_brush_size(5)
        self.draw()

    def default_bullet_matrix(self):
        """
        定義玩家子彈的動畫矩陣
        """
        return [[
            [0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]]
    
    def double_bullet_matrix(self):
        """
        定義玩家雙子彈的動畫矩陣
        """
        return [[
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],            
        ]]

    def laser_bullet_matrix(self):
        """
        定義玩家激光的動畫矩陣
        """
        laser_matrix = []        
        for _ in range(60):
            laser_matrix.append([1, 1,])
        return [laser_matrix]
        
    def alive_martixs(self):
        """
        定義玩家子彈的動畫矩陣
        """
        return self.__bullet_matrixs