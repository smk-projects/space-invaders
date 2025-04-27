from core.screen.base import ScreenBase
from core.screen.enums import ScreenState
from core.screen.screen_manager import ScreenManager
import core.screen.game_play_constant as constant
from core.helper import Countdown
from core.item.item_base import GameItemBase
from core.item.actor import \
    EnemyBase, BasicEnemy, StrongEnemy, Bunker, \
    StrongerEnemy, Player, PlayerBullet, EnemyBullet
from core.item.actor.player import PlayerAbility
from core.item.background import Star, Planet

from core.views.game_status_view import GameStatusView
from core.views.score_view import ScoreView

from core.item.enums import MoveDirection, GameItemState
from core.game_state import game_state

import core.settings.screen_setting as scrset
from core.settings.level_setting import level_config, level_count
from core.settings.level_setting import level_config

import pygame
import random
import time
from collections import defaultdict
from typing import Literal

# 定義遊戲畫面
class GamePlayScreen(ScreenBase):        
    def __init__(self):
        super().__init__()
        self.__level = level_config(game_state.current_level)
        self.__enemies = []        
        self.__enemies_init_speed = self.__level.enemy_init_speed
        self.__enemies_speed = self.__enemies_init_speed
        self.__enemy_init_count = 0
        self.__stars = []
        self.__bunkers: list[Bunker] = []
        self.__player: Player = None      
        self.__enemy_bullets: list[EnemyBullet] = []  
        self.__enemy_move_direction = MoveDirection.RIGHT
        self.__enemy_move_down_interval = -1
        self.__last_enemy_fired_time = time.time()    
        self.__status_view = GameStatusView()
        self.__deadline = 0
        self.__pause = False
        

        self.__RESET_PLYR_TIMER = Countdown(1)
        self.__NEXT_LEVEL_TIMER = Countdown(3)
        self.__GAMEOVER_TIMER = Countdown(3)        
        self.__deadline_surf = pygame.Surface((scrset.WIDTH, scrset.HEIGHT - self.__deadline), pygame.SRCALPHA)
        
    # 初始化 (覆寫父類別的 initialize)
    def initialize(self):
        self.__enemies = self.__draw_enemies()
        self.__player = self.__draw_player()
        self.__stars = self.__drow_stars()
        self.__planets = self.__draw_planets()
        self.__bunkers = self.__draw_bunker()
        self.__deadline_surf.fill((255, 0, 0, 0)) # 初始化死亡線的透明度為0
        self.__deadline_alpha_adj = 1

    def __drow_stars(self):
        # 繪製背景星星
        # 隨機產生星星的數量
        star_count = random.randint(200, 400)

        stars = []
        for _ in range(star_count):
            # 建立一顆星星
            star = Star()
            
            # 隨機設定位置
            random_x = random.uniform(0, scrset.WIDTH)
            random_y = random.uniform(0, scrset.HEIGHT)
            
            star.set_pos(x=random_x, y=random_y)
            star.draw()
            stars.append(star)
        return stars
    
    def __draw_planets(self):
        planets = []
        planet_count = random.choice([0, 1, 2, 3, 4])  # 隨機產生行星的數量
        for _ in range(planet_count):        
            # 繪製行星
            max_attempts = 10  # 最大嘗試次數
            min_distance = 100  # 最小行星間距

            planet = Planet()
            
            # 嘗試找到合適的位置
            for _ in range(max_attempts):
                # Randomly choose one of the 4 corners and add some random offset
                corner = random.randint(0, 3)
                offset_x = random.randint(0, int(scrset.WIDTH * 1.2))
                offset_y = random.randint(0, int(scrset.HEIGHT * 1.2))
                
                if corner == 0:  # Top-left
                    pos_x = offset_x
                    pos_y = offset_y
                elif corner == 1:  # Top-right
                    pos_x = scrset.WIDTH - planet.width - offset_x
                    pos_y = offset_y
                elif corner == 2:  # Bottom-left
                    pos_x = offset_x
                    pos_y = scrset.HEIGHT - planet.height - offset_y
                else:  # Bottom-right
                    pos_x = scrset.WIDTH - planet.width - offset_x
                    pos_y = scrset.HEIGHT - planet.height - offset_y

                # 檢查是否與其他行星距離太近
                too_close = False
                for existing_planet in planets:
                    dx = pos_x - existing_planet.pos_x
                    dy = pos_y - existing_planet.pos_y
                    distance = (dx * dx + dy * dy) ** 0.5
                    if distance < min_distance:
                        too_close = True
                        break
                
                if not too_close:
                    planet.set_pos(x=pos_x, y=pos_y)
                    planet.draw()
                    planet.move()
                    planets.append(planet)
                    break
        
        return planets
    
    def set_puase(self, pause: bool):
        """
        設定遊戲是否暫停
        """
        self.__pause = pause
    
    def __update_enemies_speed(self):
        """
        更新敵人的速度
        """
        alive_enemies = self.__get_enemies_by_status('ALIVE')
        if len(alive_enemies) > 1:
            enemies_speed = self.__enemies_init_speed + ((1 - len(alive_enemies) / self.__enemy_init_count) * 1.5)
        else:
            enemies_speed = self.__enemies_init_speed + ((1 - len(alive_enemies) / self.__enemy_init_count) * 5)
        self.__enemies_speed = enemies_speed
        for enemy in self.__enemies:
            if enemy.speed != self.__enemies_speed:
                enemy.set_speed(self.__enemies_speed)    
            
    # 繪製敵人
    def __draw_enemies(self):
        """
        繪製敵人
        """
        init_pos_x, init_pos_y = constant.EDGE_START, constant.EDGE_TOP        
        pos_x, pos_y = init_pos_x, init_pos_y
        init_speed = self.__enemies_init_speed
        gap = BasicEnemy().width // 1.8
        enemys = []        

        # 敵人數量佔螢幕寬度的比例        
        enemy_width_ratio = self.__level.screen_enemy_rate[0]
        # 敵人數量佔螢幕高度的比例
        enemy_height_ratio = self.__level.screen_enemy_rate[1]
        
        while pos_y < (scrset.HEIGHT * enemy_height_ratio):     
            pos_x = init_pos_x       
            while pos_x < (constant.EDGE_END * enemy_width_ratio):
                enemy = self.__generate_enemy()
                enemy.set_speed(init_speed)
                enemy.set_pos(x=pos_x, y=pos_y)
                enemy.draw()
                enemys.append(enemy)
                pos_x += enemy.width + gap
            pos_y += enemy.height + gap
    
        self.__enemy_init_count = len(enemys)
        return enemys
    
    def __draw_bunker(self):
        """
        繪製防護罩
        """
        bunker = Bunker()
        bunkers: list[Bunker] = []
        bunker_count = 4
        moveable_area = scrset.WIDTH - constant.EDGE_START - (scrset.WIDTH - constant.EDGE_END)
        bunker_gap = (moveable_area - (bunker.width * bunker_count )) // (bunker_count + 1) # 防護罩間隔，包含與左右的邊界
        bunker_y = int((scrset.HEIGHT - (scrset.HEIGHT - constant.EDGE_BOTTOM) - constant.EDGE_TOP) * (9/10))
        bunker_x = bunker_gap + constant.EDGE_START
        for _ in range(0, bunker_count):            
            bunker = Bunker()
            bunker.set_pos(x=bunker_x, y=bunker_y)
            bunker.draw()
            bunker_x += (bunker.width + bunker_gap)
            bunkers.append(bunker)
        return bunkers
        
    def __generate_enemy(self):
        """
        依關卡設定的敵人強度機率建立敵人
        """
        level_config = self.__level
        enemy_type_probs = {
            'strong_enemy': level_config.strong_enemy_rate,
            'stronger_enemy': level_config.stronger_enemy_rate
        }


        # Sort the dictionary by values in descending order
        sorted_enemy_types = sorted(enemy_type_probs.items(), key=lambda x: x[1])
        rnd = random.random()
        genrated_enemy = None
        for tp, enemy_prob in sorted_enemy_types:
            if rnd <= enemy_prob:
                if tp == 'strong_enemy':
                    genrated_enemy = StrongEnemy()
                elif tp == 'stronger_enemy':
                    genrated_enemy = StrongerEnemy()
                break
        if genrated_enemy is None:
            genrated_enemy = BasicEnemy()                
        return genrated_enemy

    # 繪製玩家
    def __draw_player(self):
        init_pos_x = scrset.WIDTH - constant.EDGE_START - scrset.BRUSH_SIZE * 2
        init_pos_y = constant.EDGE_BOTTOM
        player = Player(brush_size=scrset.BRUSH_SIZE, x=init_pos_x, y=init_pos_y)
        
        player_x, player_y = (scrset.WIDTH - player.width) / 2, constant.EDGE_BOTTOM - (player.height) - 10 # 不要黏著邊界
        
        player.set_pos(x=player_x, y=player_y) # 不要黏著邊界
        player.set_speed(3)
        player.draw()
        
        self.__deadline = player_y
        return player
    
    def __draw_background(self):
        for star in self.__stars:
            star.move()        
        for planet in self.__planets:
            planet.move()  
    
    # 控制敵人的移動
    def __enemies_action(self):
        if not self.begin_event_detect:
            return
        
        self.__enemies = [enemy for enemy in self.__enemies if enemy.item_state != GameItemState.DESTROYED]

        if len(self.__enemies) == 0:
            return

        enemies: list[EnemyBase] = self.__enemies
        alive_enemies = self.__get_enemies_by_status('ALIVE')
        
        if self.__pause or self.__player.get_ability(PlayerAbility.FREEZE):
            for enemy in alive_enemies:
                enemy.move()
            return

        self.__update_enemies_speed()
        
        grouped_pos_x: dict[int, list[EnemyBase]] = defaultdict(list)
        for enemy in alive_enemies:
            grouped_pos_x[enemy.pos_x].append(enemy)
        
        all_bottom_enemies: list[EnemyBase] = [
            enemy 
            for _, grouped_enemies in grouped_pos_x.items()
            for enemy in grouped_enemies
            if enemy.pos_y == max(
                em.pos_y for em in grouped_enemies
            )
        ] 

        # 控制敵人發射子彈
        if time.time() - self.__last_enemy_fired_time >= 1 :
            self.__last_enemy_fired_time = time.time()
        for enemy in all_bottom_enemies:
            fire_prob = random.random()
            if fire_prob > (self.__level.enemy_fire_prob * .01):
                continue
            bullet = enemy.fire(self.__level.enemy_bullet_speed)
            if bullet:
                bullet.move(direction=MoveDirection.DOWN)
                self.__enemy_bullets.append(bullet)
    
        touch_edge = False 
        rightmost_enemy = max(enemies, key=lambda e: e.pos_x + e.width)
        leftmost_enemy = min(enemies, key=lambda e: e.pos_x)

        if leftmost_enemy.pos_x <= constant.EDGE_START:
            self.__enemy_move_direction = MoveDirection.RIGHT
            touch_edge = True
            
        # 偵測最右側敵人是否已經靠近到右邊界
        # 若已碰到右邊界，則所有敵人改往左邊移動
        if rightmost_enemy.pos_x + rightmost_enemy.width >= constant.EDGE_END:
            self.__enemy_move_direction = MoveDirection.LEFT
            touch_edge = True
        
        # 當敵方觸碰到邊緣時往下移動
        if not (enemies[0].pos_x == constant.EDGE_START and enemies[0].pos_y == constant.EDGE_TOP):
            if touch_edge and self.__enemy_move_down_interval < 0:
                self.__enemy_move_down_interval = 0

        if self.__enemy_move_down_interval >= 0:
            for enemy in enemies:                
                enemy.move(direction=MoveDirection.DOWN)
            self.__enemy_move_down_interval += enemies[0].speed
            if self.__enemy_move_down_interval >= enemies[0].height // 2:
                self.__enemy_move_down_interval = -1
                
        if self.__enemy_move_down_interval < 0:
            for enemy in enemies:
                enemy.move(self.__enemy_move_direction)
    
    def __display_bunker(self):
        for bunker in self.__bunkers:
            bunker.move()

    
    def __get_enemies_by_status(self, status: Literal['ALIVE', 'FIRED']) -> list[EnemyBase]:
        """
        依狀態取得符合條件的敵人
        - ALIVE: 取得存活的敵人
        - FIRED: 取得發射子彈的敵人
        """
        if status == 'ALIVE':
            return [enemy for enemy in self.__enemies if enemy.item_state == GameItemState.ALIVE]
        elif status == 'FIRED':
            return [
                enemy 
                for enemy in self.__enemies
                if len(enemy.fired_bullets) > 0
            ]
        else:
            return self.__enemies
    
    # 處理玩家的動作
    def __player_action(self):
        if not self.begin_event_detect:
            return
        
        player_state = self.__player.item_state
        if player_state != GameItemState.ALIVE:
            if player_state == GameItemState.DESTROY:
                self.__player.move()
                return
            return
        
        player:Player = self.__player
        
        keys = pygame.key.get_pressed()
        # 玩家的移動
        if keys[pygame.K_LEFT]:
            if player.pos_x > constant.EDGE_START:
                player.move(direction=MoveDirection.LEFT)
        elif keys[pygame.K_RIGHT]:
            if player.pos_x + player.width < constant.EDGE_END:
                player.move(direction=MoveDirection.RIGHT)
        player.move()
        
        # 玩家發射子彈
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:            
            bullet = player.fire()
            if bullet:                    
                bullet.move(direction=MoveDirection.UP)

    # 控制子彈的移動
    def __move_bullets(self):
        player_bullets: list[PlayerBullet] = self.__player.fired_bullets
        
        # 玩家子彈
        if len(player_bullets) > 0:
            for bullet in player_bullets[:]:
                bullet.move(direction=MoveDirection.UP)
                if bullet.pos_y + bullet.height < constant.EDGE_TOP:
                    player_bullets.remove(bullet)

            # 挑出已經摧毀的子彈並從陣列中移除
            for bullet in player_bullets[:]:
                if bullet.item_state == GameItemState.DESTROYED:
                    player_bullets.remove(bullet)
                    
        # 敵人子彈
        fired_enemies = self.__get_enemies_by_status('FIRED')
        
        for fired_enemy in fired_enemies:
            for bullet in fired_enemy.fired_bullets[:]:
                bullet.move(                    
                    direction=MoveDirection.DOWN 
                    if self.__pause or self.__player.get_ability(PlayerAbility.FREEZE) is None else MoveDirection.STOP
                )
                if bullet.pos_y > scrset.HEIGHT:
                    fired_enemy.fired_bullets.remove(bullet)
        
    def __show_deadline(self):
        if not self.__player.state == GameItemState.ALIVE:
            return
        
        show_deadline = any(enemy.pos_y + enemy.height + int(enemy.height * 1.5) >= self.__deadline for enemy in self.__enemies)
        if not show_deadline:
            return
        
        dl_surf_bg = self.__deadline_surf.get_at((0, 0))
        alpha = dl_surf_bg[3]
        
        if alpha >= 48 and self.__deadline_alpha_adj > 0:
            self.__deadline_alpha_adj = -1 
        elif alpha <= 12 and self.__deadline_alpha_adj < 0:   
            self.__deadline_alpha_adj = 1           
        
        self.__deadline_surf.fill((255, 0, 0, alpha + self.__deadline_alpha_adj))
        ScreenManager.instance().get_main_surface().blit(self.__deadline_surf, (0, self.__deadline))
        
    def __detect_bullet_collision(self):
        """
        偵測子彈的碰撞
        """
        
        # 偵測玩家子彈與敵人之間的碰撞
        player_bullets: list[PlayerBullet] = self.__player.fired_bullets
        enemy_bullets: list[EnemyBullet] = self.__enemy_bullets
        enemies: list[EnemyBase] = self.__enemies
        alive_enemies: list[EnemyBase] = self.__get_enemies_by_status('ALIVE')
        
        for bunker in self.__bunkers:
            for bullet in player_bullets[:]:
                if bullet.hit(bunker):
                    self.__player_bullet_hit(bullet, bunker)
                    return
                    
            for bullet in enemy_bullets[:]:
                if bullet.hit(bunker):
                    enemy_bullets.remove(bullet)
                    return
            
            for enemy in alive_enemies[:]:
                enemy.hit(bunker)                
            
        for bullet in player_bullets[:]:
            for enemy in enemies[:]:
                if bullet.hit(enemy):
                    self.__player_bullet_hit(bullet, enemy)
                    game_state.player_score += enemy.score()
                    break
        
        # 偵測敵人子彈與玩家之間的碰撞
        for fired_enemy in self.__get_enemies_by_status('ALIVE'):
            for bullet in fired_enemy.fired_bullets[:]:
                if bullet.hit(self.__player):                
                    fired_enemy.fired_bullets.remove(bullet)
                    break
    
    def __next_player(self) -> bool:
        """
        重置玩家狀態
        
        - Return True: 仍有殘機，重置玩家狀態
        - Return False: 已無殘跡可重置狀態
        """
        if self.__player.state == GameItemState.ALIVE:
            return True
        
        if game_state.player_life <= 0:
            return False
        
        if not self.__RESET_PLYR_TIMER.is_running():
            self.__RESET_PLYR_TIMER.start()
            
        if self.__RESET_PLYR_TIMER.remaining_seconds > 0:
            return True
        
        game_state.player_life -= 1        
        self.__player.set_pos(
            x=(scrset.WIDTH - self.__player.width) / 2,
            y=constant.EDGE_BOTTOM - (self.__player.height) - 10
        )
        self.__player.set_state(GameItemState.ALIVE)
        self.__player.set_invincible(invincible_sec=5)
        self.__player.remove_all_abilities()
        self.__player.draw()
        return True

    def __put_status_view(self):
        """
        放置玩家狀態視圖
        """
        activate_ability = None
        activate_abilities: dict[PlayerAbility, object] = self.__player.get_abilities()
        for (abtype, abeffect) in activate_abilities.items():
            if abeffect is not None and abeffect.cooldown_remaining > 0:
                activate_ability = abeffect
                break;
        
        status_view = self.__status_view
        if activate_ability is not None:
            status_view.ability_active(activate_ability)
        else:
            status_view.ability_active(None)
        status_view.draw()
        
    def __put_score_view(self):
        score_view = ScoreView()
        score_view.draw()

    def __player_bullet_hit(self, bullet: PlayerBullet, target: GameItemBase) -> bool:
        """
        處理玩家子彈擊中目標的動作
        """
        hit_target = bullet.hit(target)
        # 判斷子彈還有殘餘威力，且敵人仍存活
        while hit_target and bullet.power > 0 and target.state == GameItemState.ALIVE:
            hit_target = bullet.hit(target) 
        # 若子彈殘餘威利用盡，則移除子彈，否則讓他繼續往下打
        if bullet.power <= 0:
            self.__player.fired_bullets.remove(bullet)
            
    def __upgrade_clicked(self, events: list[pygame.event.Event]) -> bool:
        """
        偵測升級物品是否被點擊
        """        
        if self.__player.state != GameItemState.ALIVE:
            return False
        
        # 必須所有能力的冷卻時間都結束，才能進行升級
        abilities = self.__player.get_abilities()
        if any(ability.cooldown_remaining > 0 for ability in abilities.values()):
            return False
        
        for event in events:
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_1: # 觸發雙子彈
                    self.__player.upgrade(ability=PlayerAbility.DOULBLE)
                    return True
                elif event.key == pygame.K_2:
                    self.__player.upgrade(ability=PlayerAbility.SHIELD)
                    return True
                elif event.key == pygame.K_3:
                    self.__player.upgrade(ability=PlayerAbility.FREEZE)
                    return True
        return False
    
    def __detect_bunker_collision(self):
        """
        偵測防護罩的碰撞
        """
        player_bullets: list[PlayerBullet] = self.__player.fired_bullets
        enemy_bullets: list[EnemyBullet] = self.__enemy_bullets
        
        for bunker in self.__bunkers:
            for bullet in player_bullets[:]:
                if bullet.hit(bunker):
                    while bullet.power > 0 and bunker.state == GameItemState.ALIVE:
                        bullet.hit(bunker)                        
                    if bullet.power <= 0:
                        player_bullets.remove(bullet)
                    break

    def __is_enemy_over_deadline(self):
        """
        偵測敵人是否已經過了死亡線
        """
        for enemy in self.__enemies:
            if enemy.pos_y + enemy.height >= self.__deadline:
                return True
        return False
    
    def __is_stage_pass(self) -> bool:
        if all(enemy.item_state == GameItemState.DESTROYED for enemy in self.__enemies):
            if not self.__NEXT_LEVEL_TIMER.is_running():
                self.__NEXT_LEVEL_TIMER.start()
            else:
                if self.__NEXT_LEVEL_TIMER.remaining_seconds <= 0:            
                    return True
        return False

    # 實作父類別的 next_frame
    def next_frame(self, events: list[pygame.event.Event]) -> ScreenState:
        # 繪製背景
        self.__draw_background()        
        self.__enemies_action()
        self.__player_action()
        self.__display_bunker()
        self.__move_bullets()
        
        self.__show_deadline()
        self.__detect_bullet_collision()
        self.__put_status_view()
        self.__put_score_view()
        self.__upgrade_clicked(events) 
        
        game_over = False
        if self.__player.state == GameItemState.DESTROYED and not self.__next_player():
            game_over = True
        
        if self.__is_enemy_over_deadline():
            self.__player.set_state(GameItemState.DESTROY)            
            game_over = True
        
        if game_over:
            self.__player.remove_all_abilities()
            self.set_puase(True)
            if not self.__GAMEOVER_TIMER.is_running():
                self.__GAMEOVER_TIMER.start()
            else:
                if self.__GAMEOVER_TIMER.remaining_seconds <= 0:
                    return ScreenState.GAME_OVER
        
        if self.__is_stage_pass():
            return ScreenState.GAME_PASS
        
        

        