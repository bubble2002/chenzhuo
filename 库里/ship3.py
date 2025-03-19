import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_game):
        #初始化飞船并设置初始位置
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船图像并获取外界图形
        self.image = pygame.image.load('images/curry.png')

        self.image = pygame.transform.scale(self.image,(80,58))
        self.rect = self.image.get_rect()

        #新飞船放置在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom
        #飞船属性x中存储一个浮点数
        self.x = float(self.rect.x)
        # 移动标志(初始状态静止）
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # 根据移动标志调整飞船位置
        #更新飞船属性x，而非其外接矩形的属性x的值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        #根据self.x更新rect对象
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        #指定位置绘制飞船
        self.screen.blit(self.image,self.rect)