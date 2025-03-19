import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #管理子弹发射的类
    def __init__(self,ai_game):
        #在飞船当前位置创建一个子弹对象
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/basketball.png')
        self.image = pygame.transform.scale(self.image,(25,25))
        # 设置初始位置（从飞船中心发射）
        self.rect = self.image.get_rect()
        self.rect.center = ai_game.ship.rect.center

        # 精确浮点坐标
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)


    def update(self):
        #向上移动子弹/更新子弹的准确位置
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        #屏幕上绘制子弹
        self.screen.blit(self.image,self.rect)

