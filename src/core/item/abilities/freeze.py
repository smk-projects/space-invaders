from ..item_base import GameItemBase
from core.config.item_config import GameItemConfig
from core.item.enums import GameItemType
from core.settings.screen_setting import BRUSH_SIZE

class Freeze(GameItemBase):
    """
    防護罩圖示: Shield
    """
    def __init__(self, brush_size: int = BRUSH_SIZE):
        config = GameItemConfig(
            brush_size=brush_size,
            item_type = GameItemType.UPGRADE,
        )
        super().__init__(config)
        
    def alive_martixs(self):
        return [[
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0],
            [1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1],
            [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
            [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
            [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
            [1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1],
            [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        ]]