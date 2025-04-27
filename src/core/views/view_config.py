from dataclasses import dataclass, field

@dataclass
class ViewConfig:
    width: int = 0
    height: int = 0
    padding_left: int = 0
    padding_right: int = 0
    padding_bottom: int = 0
    padding_top: int = 0
    background: tuple = (0, 0, 0)
    x: int = 0
    y: int = 0
    