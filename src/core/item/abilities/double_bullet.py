from core.item.item_base import GameItemBase
from core.item.enums import GameItemType
from core.config.item_config import GameItemConfig
from core.settings.screen_setting import BRUSH_SIZE

class DoubleBullet(GameItemBase):
    """
    雙子彈: DoubleBullet
    """
    def __init__(self, brush_size: int = BRUSH_SIZE):
        config = GameItemConfig(
            brush_size=brush_size,
            item_type=GameItemType.UPGRADE
        )
        super().__init__(config)
        
    def alive_martixs(self):
        return [[
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 0],
            [0, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 0],
            [0, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 0],
            [0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]]