import arcade
from car_class import Car

class Enemy(Car):
	def __init__(self, screen, frames, g_scale, bullet_list, center_y, speed = 4):
		super().__init__(screen, frames, g_scale, speed = 4)
		self.bullet_list = bullet_list
		self.time_since_last_firing = 0.0
		self.time_between_firing = 0.2
		self.shoot = False
		self.change_x = 5.5*g_scale
		self.center_y = center_y
	
	def update(self, delta_time: float = 1/60):
		super().update()
		self.time_since_last_firing += delta_time
		if self.shoot and self.time_since_last_firing >= self.time_between_firing:
			self.time_since_last_firing = 0
			bullet = arcade.Sprite("images/other/bullet.png", scale = g_scale*1.5)
			bullet.center_x = self.right
			bullet.center_y = self.center_y
			bullet.change_x = 50*g_scale
			self.bullet_list.append(bullet)