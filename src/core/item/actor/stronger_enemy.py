from core.item.item_base import GameItemBase
from core.config.item_config import GameItemConfig
from core.item.actor.enemy_base import EnemyBase
from core.item.bullet.player_bullet import PlayerBullet

from core.item.enums import GameItemType, GameItemState

class StrongerEnemy(EnemyBase):
    """
    敵方角色: 特殊敵人
    """
    def __init__(self):
        super().__init__()
        self.set_life(3)
        self.set_brush_color((255, 0, 0))  # 設定畫筆顏色為紅色

    def alive_martixs(self):
        """
        定義敵方物件的動畫矩陣
        """
        return [
            [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 2, 3, 3, 2, 2, 0, 0, 0],
            [0, 0, 2, 3, 3, 2, 2, 3, 3, 2, 0, 0],
            [0, 2, 3, 4, 4, 3, 3, 4, 4, 1, 2, 0],
            [0, 2, 3, 0, 4, 4, 4, 4, 0, 3, 2, 0],
            [0, 0, 2, 0, 0, 4, 4, 0, 0, 2, 0, 0],
            [0, 0, 0, 2, 3, 3, 3, 3, 2, 0, 0, 0],
            [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 2, 3, 3, 2, 2, 0, 0, 0],
            [0, 0, 2, 3, 3, 2, 2, 3, 3, 2, 0, 0],
            [0, 2, 3, 4, 4, 3, 3, 4, 4, 3, 2, 0],
            [0, 2, 3, 0, 4, 4, 4, 4, 0, 3, 2, 0],
            [0, 0, 2, 0, 0, 4, 4, 0, 0, 2, 0, 0],
            [0, 0, 0, 2, 3, 3, 3, 3, 2, 0, 0, 0],
            [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        ]
        