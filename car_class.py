import arcade

class Car(arcade.AnimatedTimeBasedSprite):
	def __init__(self, screen, frames, g_scale, speed = 3.5):
		super().__init__('images/car/car.png', scale = g_scale)
		self.scale = g_scale
		self.shadow = arcade.Sprite('images/other/shadow.png', scale=2.5*g_scale)
		self.frames = frames
		self.speed = speed*g_scale
		self.center_x = -self.width
		
		self.change_x = 6*g_scale

	def update(self):
		self.center_x += self.change_x
		self.center_y += self.change_y

		self.shadow.center_x = self.center_x
		self.shadow.center_y = self.center_y-self.height/3
		self.update_animation()