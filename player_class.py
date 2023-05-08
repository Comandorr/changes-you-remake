import arcade
from car_class import Car

class Player(Car):
    def __init__(self, screen, frames, g_scale, bullet_list, speed = 3.5):
        super().__init__(screen, frames, g_scale, speed = 3.5)
        self.bullet_list = bullet_list
        self.center_y = screen.height/2