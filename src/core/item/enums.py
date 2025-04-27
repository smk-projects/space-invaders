
from enum import Enum

class GameItemType(Enum):
    """
    描述物件的類型
    """
    ENEMY = 1 # 敵人
    PLAYER = 2 # 玩家
    BULLET = 3, # 子彈
    BACKGROUND = 4, # 背景物件
    BUNKER = 5, # 防禦堡壘
    UPGRADE  = 6, # 升級物件

class GameItemState(Enum):
    """
    描述物件的狀態
    """
    ALIVE = 1
    DESTROY = 2
    EXPLOSION = 3
    DESTROYED = 4
    
class MoveDirection(Enum):
    """
    描述物件的移動方向
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP_LEFT = 6
    UP_RIGHT = 7
    DOWN_LEFT = 8
    DOWN_RIGHT = 9
    STOP = 5
