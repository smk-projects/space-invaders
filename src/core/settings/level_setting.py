from core.config.level_config import LevelConfig

__all_level_configurations = \
    [
        # Level 1
        LevelConfig(
            enemy_init_speed=0.5, # 敵人初始速度
            enemy_bullet_speed=5, # 敵人子彈速度
            enemy_fire_prob=0.2, # 敵人開火機率
            screen_enemy_rate=(0.7, 0.2),  # 螢幕敵人比例   
        ),
        # Level 2
        LevelConfig(
            enemy_init_speed=0.5,
            enemy_bullet_speed=5,
            enemy_fire_prob=0.3,
            screen_enemy_rate=(0.7, 0.2),
        ),
        # Level 3
        LevelConfig(
            enemy_init_speed=0.5,
            enemy_bullet_speed=6,
            enemy_fire_prob=0.3,
            screen_enemy_rate=(0.8, 0.2),
            strong_enemy_rate=0.05
        ),
        # Level 4 
        LevelConfig(
            enemy_init_speed=0.6,
            enemy_bullet_speed=6,
            enemy_fire_prob=0.4,
            screen_enemy_rate=(0.8, 0.3),
            strong_enemy_rate=0.05
        ),
        # Level 5
        LevelConfig(
            enemy_init_speed=0.6,
            enemy_bullet_speed=6,
            enemy_fire_prob=0.4,
            screen_enemy_rate=(0.8, 0.3),
            strong_enemy_rate=0.1,
            stronger_enemy_rate=0.05
        ),
        # Level 6   
        LevelConfig(
            enemy_init_speed=0.7,
            enemy_bullet_speed=7,
            enemy_fire_prob=0.5,
            screen_enemy_rate=(0.8, 0.3),
            strong_enemy_rate=0.2,
            stronger_enemy_rate=0.05
        ),
        # Level 7  
        LevelConfig(
            enemy_init_speed=0.7,
            enemy_bullet_speed=8,
            enemy_fire_prob=0.5,
            screen_enemy_rate=(0.8, 0.3),
            strong_enemy_rate=0.3,
            stronger_enemy_rate=0.1
        ),
        # Level 8
        LevelConfig(
            enemy_init_speed=0.7,
            enemy_bullet_speed=9,
            enemy_fire_prob=0.6,
            screen_enemy_rate=(0.9, 0.3),
            strong_enemy_rate=0.3,
            stronger_enemy_rate=0.2
        ),
        # Level 9
        LevelConfig(
            enemy_init_speed=0.7,
            enemy_bullet_speed=10,
            enemy_fire_prob=0.6,
            screen_enemy_rate=(0.9, 0.3),
            strong_enemy_rate=0.3,
            stronger_enemy_rate=0.3
        ),
        # Level 10
        LevelConfig(
            enemy_init_speed=0.7,
            enemy_bullet_speed=12,
            enemy_fire_prob=0.6,
            screen_enemy_rate=(0.9, 0.3),
            strong_enemy_rate=0.3,
            stronger_enemy_rate=0.5
        ),
    ]

def level_config(level: int) -> LevelConfig:     
    level_configurations = __all_level_configurations
    if level < 1:
        return level_configurations[0]
    elif level > len(level_configurations):
        return level_configurations[-1]
    else:
        return level_configurations[level - 1]
    
def level_count() -> int:
    """
    取得關卡數量
    """
    return len(__all_level_configurations)