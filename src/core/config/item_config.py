from core.item.enums import GameItemType

class GameItemConfig:
    """
    遊戲物件的設定
    """
    def __init__(self, brush_size=5, init_x=0, init_y=0, init_speed=3, item_type: GameItemType = GameItemType.ENEMY):
        self.brush_size = brush_size
        self.item_type = item_type
        self.init_x = init_x
        self.init_y = init_y
        self.init_speed = init_speed

