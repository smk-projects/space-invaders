from core.item.bullet.bullet_base import BulletBase
from core.item.item_base import GameItemBase
from core.item.enums import GameItemType, GameItemState
import pygame

class EnemyBullet(BulletBase):
    """
    敵人子彈: Bullet
    """
    def __init__(self):        
        super().__init__()

    def alive_martixs(self):
        """
        定義子彈的動畫矩陣
        """
        return [[
            [0, 0, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0],
        ]]
