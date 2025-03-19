class Settings:
    #储存游戏中所有设置的类
    def __init__(self):
        #初始化游戏静态设置//屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color =(222,184,135)

        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右运动，为-1表示向左移动;
        self.fleet_direction = 1

        #外星人设置

        self.ship_limit = 4

        #以什么速度加快游戏节奏
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #初始化游戏动态设置
        self.ship_speed = 5
        self.bullet_speed = 5
        self.alien_speed = 3
        # fleet_direction为1表示向右运动，为-1表示向左移动
        self.fleet_direction = 1

        #记分设置
        self.aline_points = 3


    def increase_speed(self):
        #提高速度的值
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale