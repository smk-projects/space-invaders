from core.screen.screen_manager import ScreenManager
from core.item.item_base import GameItemBase
from .ability_base import AbilityBase

class Freeze(AbilityBase):
    """
    凍結敵人
    """
    def __init__(self, keep_sec: int = 3, colldown_sec: int = 15):
        super().__init__(keep_sec, colldown_sec)