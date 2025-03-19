import sys
from time import sleep
import pygame
from game_stats6 import GameStats
from settings2 import Settings
from ship3 import Ship
from bullet4 import Bullet
from alien5 import Alien
from button7 import Button
from score8 import Scoreboard
import json
from pathlib import Path



class AlienInvasion:
    #管理游戏资源和行为的类
    def __init__(self):
        #初始化创建资源
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.init()
        pygame.mixer.music.load('bgm_max1.wav')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        self.swish1 = pygame.mixer.Sound('swish1.wav')
        self.swish1.set_volume(0.1)
        self.ball = pygame.mixer.Sound('basketball.wav')
        self.ball.set_volume(1)
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.background =pygame.image.load('images/court.png')
        self.background = pygame.transform.scale(self.background,(1200,1100))
        pygame.display.set_caption("Aline Invasion")
        #创建一个用于储存游戏统计信息的实例,并创建记分牌
        self.stats = GameStats(self)
        self.sb =Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        #游戏启动后处于活动状态
        self.game_active = True
        #切换背景颜色
        self.bg_color = (230,230,230)
        self.game_active = False
        self.play_button = Button(self,'Go Warriors : I can do all things!' )

    def draw_background(self):
        self.screen.blit(self.background,(0,0))

    def run_game(self):
        #开始游戏主循环
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)
    def _check_events(self):
        # 侦听鼠标和键盘事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        #玩家单击play按钮时才开始游戏
     button_clicked = self.play_button.rect.collidepoint(mouse_pos)
     if button_clicked and not self.game_active:
         #还原游戏设置
         self.settings.initialize_dynamic_settings()
         #重置游戏的统计信息
         self.stats.reset_stats()
         self.sb.prep_score()
         self.sb.prep_level()
         self.sb.prep_ships()
         self.game_active = True
         #清空敌人列表和子弹列表
         self.bullets.empty()
         self.aliens.empty()
         #创建一个新的舰队，并且将飞船放在底部中央屏幕
         self._create_fleet()
         self.ship.center_ship()
         pygame.mouse.set_visible(False)



    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._close_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        #创建一个子弹，将其加入编组bullets
        new_bullet = Bullet(self)
        if pygame.mixer.get_busy()<2:
            self.ball.play()
        self.bullets.add(new_bullet)

    def _update_screen(self):
        # 每次循环重新绘制屏幕
        self.screen.fill(self.settings.bg_color)
        self.draw_background()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        #显示得分
        self.sb.show_score()
        #当游戏处于非活跃状态，就绘制play按钮
        if not self.game_active:
            self.play_button.draw_button()
        # 最近绘制的屏幕可视化
        pygame.display.flip()

    def _update_bullets(self):
        #更新子弹位置
        # 删除已经消失的子弹
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_aline_collisions()

    def _check_bullet_aline_collisions(self):
        # 检查是否有子弹击中敌人，如果有就删除相应的子弹和敌人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens , True, True)
        if collisions:
            for aliens in collisions.values():
             self.stats.score += self.settings.aline_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            if pygame.mixer.get_busy()<2:
                self.swish1.play()


        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #提高等级
            self.stats.level +=1
            self.sb.prep_level()

    def _create_fleet(self):
        #创建舰队/创建敌人
        #敌人间距为宽度和高度
        alien =Alien(self)
        alien_width,alien_height = alien.rect.size

        current_x, current_y = alien_width,alien_height
        while current_y <(self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width
            #添加一行敌人后，重置x值并递增y值

            current_x = alien_width
            current_y += 2*alien_height

    def _create_alien(self,x_position,y_position):
        #将一个敌人放入当前行中
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        #更新外星人中所有敌人的位置,并检查是否在其边缘
        self._check_fleet_edges()
        self.aliens.update()
        #检测敌人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #检查是否有外星人到达屏幕底部
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        #当外星人到达边缘时采取相应措施4
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        #将整个外星舰队向下移动，并且改变它们的方向
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        #响应飞船和外星人碰撞
        # 将ships_left 减1
        if self.stats.ships_left >0:
            #将飞船减1并且更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()
        #清空外星人和子弹列表
            self.bullets.empty()
            self.aliens.empty()

        #创建新队，并且将其放在底部中央
            self._create_fleet()
            self.ship.center_ship()
        #暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        #检查是否到达屏幕底部
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #被撞一样
                self._ship_hit()
                break

    def _close_game(self):
        """保存这个比分并且退出我的游戏"""
        saved_high_score = self.stats.get_saved_high_score()
        if self.stats.high_score > saved_high_score:
            path = Path('high_score.json')
            contents = json.dumps(self.stats.high_score)
            path.write_text(contents)

        sys.exit()

if __name__ == '__main__':
    # 创建游戏实例并运行我的游戏！！！
    ai = AlienInvasion()
    ai.run_game()