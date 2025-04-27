from .ability_base import AbilityBase

class DoubleBullet(AbilityBase):
    """
    雙子彈升級
    """
    def __init__(self, keep_sec: int = 10, colldown_sec: int = 25):
        super().__init__(keep_sec, colldown_sec)      