from dataclasses import dataclass, field

@dataclass
class LevelConfig:
    enemy_init_speed: int = .5 # 敵人初始速度
    enemy_bullet_speed: int = 1 # 敵人子彈速度
    enemy_fire_prob: float = .1 # 敵人發射子彈的機率
    screen_enemy_rate: tuple[float, float] = field(default_factory=lambda: [.7, .2]) # 畫面上敵人數量佔螢幕長寬的比率
    strong_enemy_rate: float = 0.0 # 強化敵人的比率
    stronger_enemy_rate: float = 0.0 # 更強化敵人的比率

