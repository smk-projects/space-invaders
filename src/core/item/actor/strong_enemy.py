from core.item.item_base import GameItemBase
from core.item.enums import GameItemState
from core.config.item_config import GameItemConfig
from core.item.actor.enemy_base import EnemyBase
from core.item.bullet.player_bullet import PlayerBullet

from core.item.enums import GameItemType

class StrongEnemy(EnemyBase):
    """
    敵方角色: 特殊敵人
    """
    def __init__(self):
        super().__init__()
        self.set_life(2)
        self.set_brush_color((255, 255, 0))  # 設定畫筆顏色為紅色

    def alive_martixs(self):
        """
        定義敵方物件的動畫矩陣
        """
        return [
            [
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0],
                [0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0],
                [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            [
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
                [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        ]
        