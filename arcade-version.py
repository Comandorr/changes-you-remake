import arcade
import random
import pyglet

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(arcade.AnimatedTimeBasedSprite):
	def setup(self):
		shadow_texture = arcade.make_soft_circle_texture(72, (100, 100, 100))
		self.shadow = arcade.Sprite('images/other/shadow.png', scale=2.5)
		self.frames = [car1, car2]
		self.speed = 4
		self.center_x = SCREEN_WIDTH/6
		self.center_y = SCREEN_HEIGHT/2
		self.change_x = 7

	def update(self):
		global x_start
		self.center_x += self.change_x
		self.center_y += self.change_y
		
		if self.left < x_start:
			self.left = x_start
		elif self.right > x_start+SCREEN_WIDTH - 1:
			self.right = x_start+SCREEN_WIDTH - 1
		if self.bottom < 0:
			self.bottom = 0
		elif self.top > SCREEN_HEIGHT - 1:
			self.top = SCREEN_HEIGHT - 1
		self.shadow.center_x = self.center_x
		self.shadow.center_y = self.center_y-7
		self.update_animation()
		

sand_texture = arcade.Texture.create_filled('sand', [16,4], (255, 127, 39))
rain_texture = arcade.Texture.create_filled('rain', [6,24], (0, 162, 232))
snow_texture = arcade.Texture.create_filled('snow', [16,4], (173, 173, 173))
car1 = arcade.AnimationKeyframe(0, 166, arcade.load_texture('images/car/car.png'))
car2 = arcade.AnimationKeyframe(1, 166, arcade.load_texture('images/arcade/car2.png'))


class SandParticle(arcade.FadeParticle):
	def __init__(self):
		global x_start
		super().__init__(sand_texture, (-15, 0.0),
		lifetime=1,
		center_xy=(SCREEN_WIDTH+x_start, random.randint(0, SCREEN_HEIGHT)),
		end_alpha=100)


class SnowParticle(arcade.FadeParticle):
	def __init__(self):
		global x_start
		super().__init__(snow_texture, (-15, 0.0),
		lifetime=1,
		center_xy=(SCREEN_WIDTH+x_start, random.randint(0, SCREEN_HEIGHT)),
		end_alpha=100)


class RainParticle(arcade.FadeParticle):
	def __init__(self):
		global x_start
		super().__init__(rain_texture, (-7, -10),
		lifetime=1,
		center_xy=(random.randint(0, SCREEN_WIDTH*2) + x_start, SCREEN_HEIGHT),
		angle = -20, end_alpha=50)


class SandEmitter(arcade.Emitter):
	def __init__(self):
		super().__init__(
            center_xy=(0.0, 0.0),
            emit_controller=arcade.EmitInterval(0.0075),
            particle_factory=lambda emitter: SandParticle())


class SnowEmitter(arcade.Emitter):
	def __init__(self):
		super().__init__(
            center_xy=(0.0, 0.0),
            emit_controller=arcade.EmitInterval(0.0075),
            particle_factory=lambda emitter: SnowParticle())


class RainEmitter(arcade.Emitter):
	def __init__(self):
		super().__init__(
            center_xy=(0.0, 0.0),
            emit_controller=arcade.EmitInterval(0.01),
            particle_factory=lambda emitter: RainParticle())


class Game(arcade.Window):
	def __init__(self):
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

	def setup(self):
		self.keys = {'w':False, 's':False, 'a':False, 'd':False}
		self.player_list = arcade.SpriteList()
		self.player = Player('images/car/car.png')
		self.player.setup()
		self.player_list.append(self.player.shadow)
		self.player_list.append(self.player)
		self.location = 'desert'
		self.way = ['desert']

		self.map = arcade.SpriteList()
		self.generate_locations()
		self.emitter = SandEmitter()
		
		self.camera = arcade.Camera()
		self.kilometers_text = arcade.Text(str(self.camera.position[0]), 100+SCREEN_WIDTH-50, SCREEN_HEIGHT-100, (0,0,0), 20)
		self.location_text = arcade.Text(str(self.location), 100, SCREEN_HEIGHT-100, (0,0,0), 20)

	def generate_locations(self):
		self.way = ['desert', 'winter', 'swamp']
		for i in range(len(self.way)):
			w = self.way[i]
			for x in range((i*7500), 7500 + (i*7500), 64):
				for y in range(32, SCREEN_HEIGHT+31, 64):
					if w == 'desert':
						image = 'images/tiles/sand.png'
					elif w == 'swamp':
						image = 'images/tiles/swamp'+str(random.randint(1,3))+'.png'
					elif w == 'winter':
						image = 'images/tiles/snow'+str(random.randint(1,2))+'.png'
					self.map.append(arcade.Sprite(image,
					center_x=x, center_y=y,
					hit_box_algorithm = None))

	def on_draw(self):
		self.camera.use()
		self.clear()
		self.map.draw()
		self.player_list.draw()
		self.emitter.draw()
		self.kilometers_text.draw()
		self.location_text.draw()
		
		
	def update_player_speed(self):
		self.player.change_x = 7
		self.player.change_y = 0
		if self.keys['w'] and not self.keys['s']:
			self.player.change_y = self.player.speed/2
		if self.keys['s'] and not self.keys['w']:
			self.player.change_y = -self.player.speed/2
		if self.keys['d'] and not self.keys['a']:
			self.player.change_x = 7 + self.player.speed
		if self.keys['a'] and not self.keys['d']:
			self.player.change_x = 7-self.player.speed

	def on_update(self, delta_time):
		self.camera.goal_position = self.camera.position + pyglet.math.Vec2(7, 0)
		global x_start
		x_start = self.camera.position[0]
		self.player_list.update()
		self.emitter.update()
		self.location = self.way[int(x_start//7500)]
		self.kilometers_text.position = (x_start + SCREEN_WIDTH-75, SCREEN_HEIGHT-50)
		self.kilometers_text.text = str(int(x_start//10))
		self.location_text.position = (x_start + 100, SCREEN_HEIGHT-50)
		if self.location_text.text != self.location:
			self.location_text.text = self.location
			if self.location == 'desert':
				self.emitter = SandEmitter()
			elif self.location == 'winter':
				self.emitter = SnowEmitter()
			elif self.location == 'swamp':
				self.emitter = RainEmitter()

	def on_key_press(self, key, modifiers):
		if key == arcade.key.W:
			self.keys['w'] = True
		if key == arcade.key.S:
			self.keys['s'] = True
		if key == arcade.key.D:
			self.keys['d'] = True
		if key == arcade.key.A:
			self.keys['a'] = True
		self.update_player_speed()
		
	def on_key_release(self, key, modifiers):
		if key == arcade.key.W:
			self.keys['w'] = False
		if key == arcade.key.S:
			self.keys['s'] = False
		if key == arcade.key.D:
			self.keys['d'] = False
		if key == arcade.key.A:
			self.keys['a'] = False
		self.update_player_speed()


game = Game()
game.setup()
game.run()


