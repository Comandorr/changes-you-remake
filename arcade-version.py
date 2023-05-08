import arcade
import random
import pyglet
from car_class import Car
from player_class import Player
from enemy_class import Enemy

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# ENEMY UDATE OLD
#	def update(self, delta_time: float = 1 / 60):
#		global x_start, g_scale
#		self.speed *= g_scale
#		self.center_x += self.change_x
#		self.center_y += self.change_y
#
#		self.shadow.center_x = self.center_x
#		self.shadow.center_y = self.center_y-self.height/3
#		self.update_animation()
#		self.time_since_last_firing += delta_time
#		
#		if self.shoot and self.time_since_last_firing >= self.time_between_firing:
#			self.time_since_last_firing = 0
#			bullet = arcade.Sprite("images/other/bullet.png", scale = g_scale*1.5)
#			bullet.center_x = self.right
#			bullet.center_y = self.center_y
#			bullet.change_x = 50*g_scale
#			self.bullet_list.append(bullet)


sand_texture = arcade.Texture.create_filled('sand', [16,5], (255, 127, 39))
rain_texture = arcade.Texture.create_filled('rain', [6,24], (0, 162, 232))
snow_texture = arcade.Texture.create_filled('snow', [16,4], (173, 173, 173))

car1 = arcade.AnimationKeyframe(0, 166, arcade.load_texture('images/car/car.png'))
car2 = arcade.AnimationKeyframe(1, 166, arcade.load_texture('images/arcade/car2.png'))
e1 = arcade.AnimationKeyframe(0, 166, arcade.load_texture('images/enemies/rounded_yellow.png'))
e2 = arcade.AnimationKeyframe(1, 166, arcade.load_texture('images/enemies/rounded_yellow2.png'))

tire_texture = arcade.make_soft_square_texture(8, (0,0,0), center_alpha = 50, outer_alpha = 50)

class TireParticle(arcade.FadeParticle):
	def __init__(self, p, sdvig):
		super().__init__(tire_texture, change_xy = (0,0),
		lifetime= 2,
		center_xy=(p.player.left, p.player.center_y-7),
		end_alpha=100)


def new_tire(player):
	return TireParticle(player, sdgvig)


class SandParticle(arcade.FadeParticle):
	def __init__(self):
		global x_start
		super().__init__(sand_texture, (-25, 0.0),
		lifetime= 0.75 + random.random(),
		center_xy=(SCREEN_WIDTH+x_start, random.randint(0, SCREEN_HEIGHT)),
		end_alpha=100)


class SnowParticle(arcade.FadeParticle):
	def __init__(self):
		global x_start
		super().__init__(snow_texture, (-15, 0.0),
		lifetime=SCREEN_WIDTH/800,
		center_xy=(SCREEN_WIDTH+x_start, random.randint(0, SCREEN_HEIGHT)),
		end_alpha=100)


class RainParticle(arcade.FadeParticle):
	def __init__(self):
		global x_start
		super().__init__(rain_texture, (-7, -10),
		lifetime=SCREEN_WIDTH/600,
		center_xy=(random.randint(0, SCREEN_WIDTH*2) + x_start, SCREEN_HEIGHT),
		angle = -20, end_alpha=50)


class SandEmitter(arcade.Emitter):
	def __init__(self):
		super().__init__(
            center_xy=(0.0, 0.0),
            emit_controller=arcade.EmitInterval(0.005),
            particle_factory=lambda emitter: SandParticle())

class TireEmitter(arcade.Emitter):
	def __init__(self, player):
		super().__init__(
            center_xy=(0.0, 0.0),
            emit_controller=arcade.EmitInterval(0.03),
            particle_factory= new_tire)
		self.player = player

class TireEmitter2(arcade.Emitter):
	def __init__(self, player):
		super().__init__(
            center_xy=(0.0, 0.0),
            emit_controller=arcade.EmitInterval(0.03),
            particle_factory= new_tire2)
		self.player = player


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
		global SCREEN_WIDTH, SCREEN_HEIGHT
		super().__init__(fullscreen=True, vsync=True)
		#super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
		SCREEN_WIDTH, SCREEN_HEIGHT =  arcade.get_display_size()
		self.player = None
		self.player_list = None
		self.map = None
		self.keys = None
		self.location = None
		global g_scale
		g_scale = SCREEN_WIDTH/1080

	def setup(self):
		global g_scale
		self.cutscene = True
		
		self.keys = {'w':False, 's':False, 'a':False, 'd':False}
		self.bullet_list = arcade.SpriteList()
		self.player_list = arcade.SpriteList()
		self.player = Player(self, [car1, car2], g_scale, self.bullet_list)
		#self.player.setup()
		self.player_list.append(self.player.shadow)
		self.player_list.append(self.player)

		self.enemies = arcade.SpriteList()
		self.enemy1 = Enemy(self, [e1, e2], g_scale, self.bullet_list, self.height*0.25)
		#self.enemy1.setup(SCREEN_HEIGHT/4)
		self.enemy2 = Enemy(self, [e1, e2], g_scale, self.bullet_list, self.height*0.75)
		#self.enemy2.setup(SCREEN_HEIGHT/4*3)
		self.enemies.append(self.enemy1.shadow)
		self.enemies.append(self.enemy1)
		self.enemies.append(self.enemy2.shadow)
		self.enemies.append(self.enemy2)

		self.location = 'desert'
		self.way = ['desert']

		self.map = arcade.SpriteList()
		self.generate_locations()
		self.emitter = SandEmitter()
		
		self.camera = arcade.Camera()
		self.camera.position = pyglet.math.Vec2(SCREEN_WIDTH/2, 0)
		self.kilometers_text = arcade.Text(str(self.camera.position[0]), SCREEN_WIDTH, SCREEN_HEIGHT-100, (0,0,0), 20*g_scale)
		self.location_text = arcade.Text(str(self.location), 50, SCREEN_HEIGHT-100, (0,0,0), 20*g_scale)
		arcade.load_font('F77 Minecraft.ttf')
		self.upper_text = arcade.Text("LET'S "*10, self.camera.position[0]+SCREEN_WIDTH/4, SCREEN_HEIGHT-100, (255, 255, 255), 40*g_scale, font_name = 'F77 Minecraft')
		self.bottom_text = arcade.Text("GO "*10, self.camera.position[0]+SCREEN_WIDTH/4, 100, (255, 255, 255), 40*g_scale, font_name = 'F77 Minecraft')
		self.letsgo = arcade.Text("LET'S GO", self.camera.position[0]+SCREEN_WIDTH/4, 100, (0,0,0), 162*g_scale, font_name = 'F77 Minecraft')

		self.music = arcade.Sound('sounds/the_sound.mp3')
		self.media_player = self.music.play(loop=True)
		self.music.set_volume(1, self.media_player)
		# the_sound
		# paint
		
		
		
		self.black_texture = arcade.Texture.create_filled('black', [SCREEN_WIDTH, SCREEN_HEIGHT], (0, 0, 0))
		self.black_texture.alpha = 255
		self.time = 0

		self.explosion = arcade.load_animated_gif('images/boom.gif')
		self.explosion.scale = 0.8
		self.explosion2 = arcade.load_animated_gif('images/boom.gif')
		self.explosion2.scale = 0.1

		#self.tire_emitter = TireEmitter(self.player)
		#self.tire_emitter2 = TireEmitter2(self.player)

	def generate_locations(self):
		self.way = ['desert', 'desert', 'desert', 'winter', 'swamp']
		for i in range(len(self.way)):
			w = self.way[i]
			for x in range((i*15000), 15000 + (i*15000), 64):
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
		self.clear()
		
		self.map.draw()
		self.player_list.draw()
		
		self.enemies.draw()
		self.emitter.draw()
		#self.tire_emitter.draw()
		#self.tire_emitter2.draw()
		self.bullet_list.draw()
		#self.kilometers_text.draw()
		#self.location_text.draw()
		if self.cutscene:
			self.black_texture.draw_sized(self.camera.position[0] + SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 
				SCREEN_WIDTH, SCREEN_HEIGHT, alpha = self.black_texture.alpha)
			if self.black_texture.alpha > 0.5:
				self.black_texture.alpha -= 0.5
			
			self.black_texture.draw_sized(self.camera.position[0] + SCREEN_WIDTH/2, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT/4)
			self.black_texture.draw_sized(self.camera.position[0] + SCREEN_WIDTH/2, 0, SCREEN_WIDTH, SCREEN_HEIGHT/4)
			if self.time > 13:
				self.upper_text.draw()
				self.letsgo.color = (255, 255, 255)
				self.letsgo.draw()
			if self.time > 13.1:
				self.bottom_text.draw()
				self.letsgo.color = (0,0,0)
				self.explosion.center_x = self.camera.position[0]+SCREEN_WIDTH/2
				self.explosion.center_y = SCREEN_HEIGHT/2
				self.explosion.draw()
				self.letsgo.draw()
		
	def update_player_speed(self):
		global g_scale, x_start
		self.player.change_x = 5*g_scale
		self.player.change_y = 0
		if self.keys['w'] and not self.keys['s']:
			self.player.change_y = self.player.speed/1.5
		if self.keys['s'] and not self.keys['w']:
			self.player.change_y = -self.player.speed/1.5
		if self.keys['d'] and not self.keys['a']:
			self.player.change_x = 5*g_scale + self.player.speed
		if self.keys['a'] and not self.keys['d']:
			self.player.change_x = 5*g_scale - self.player.speed
		if self.player.left < x_start:
			self.player.left = x_start
		elif self.player.right > x_start+SCREEN_WIDTH - 1:
			self.player.right = x_start+SCREEN_WIDTH - 1
		if self.player.bottom < 0:
			self.player.bottom = 0
		elif self.player.top > SCREEN_HEIGHT - 1:
			self.player.top = SCREEN_HEIGHT - 1


	def on_update(self, delta_time):
		global x_start, g_scale
		self.time += delta_time
		self.camera.use()
		if self.time > 13:
			self.explosion.update()
			self.explosion.update_animation()

		x_start = self.camera.position[0]
		self.emitter.update()
		#self.tire_emitter.update()
		#self.tire_emitter2.update()
		if self.cutscene:
			if self.time >= 0:
				self.player_list.update()
				if self.player.center_x >= x_start+SCREEN_WIDTH/3:
					self.player.center_x = x_start+SCREEN_WIDTH/3
					self.player.change_x = 5*g_scale
			else:
				self.player.center_x = x_start-self.player.width

			if self.time < 6.5:
				self.enemy1.center_x = x_start-self.enemy1.width
				self.enemy2.center_x = x_start-self.enemy2.width
			if self.time >= 6.5 and self.time < 13.6:
				self.enemies.update()
				if self.player.center_x - self.enemy1.center_x <= 250*g_scale:
					self.enemy1.change_x = 5*g_scale
					self.enemy2.change_x = 5*g_scale
			elif self.time >= 13.6:
				self.enemies.update()
				for e in self.enemies:
					e.shoot = True
				self.enemy1.change_x = 5*g_scale
				self.enemy2.change_x = 4.5*g_scale
				self.enemy1.change_y = 1.5*g_scale
				self.enemy2.change_y = -1.25*g_scale
				self.cutscene = False
			
		else:
			self.enemies.update()
			self.player_list.update()
			self.update_player_speed()
		for bullet in self.bullet_list:
			if bullet.left > x_start+SCREEN_WIDTH:
				bullet.remove_from_sprite_lists()
		self.bullet_list.update()
		
		self.camera.goal_position = self.camera.position + pyglet.math.Vec2(5*g_scale, 0)

		self.location = self.way[int(x_start//15000)]
		self.kilometers_text.position = (x_start + SCREEN_WIDTH-150, SCREEN_HEIGHT-50)
		self.kilometers_text.text = str(int(x_start//10))
		self.kilometers_text.text = str(int(self.enemy1.center_x-x_start))
		self.upper_text.position = (self.camera.position[0], SCREEN_HEIGHT-110)
		self.bottom_text.position = (self.camera.position[0], 35)
		self.letsgo.position = (self.camera.position[0], SCREEN_HEIGHT/2-120)
		self.location_text.position = (x_start + 25, SCREEN_HEIGHT-50)
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
		
	def on_key_release(self, key, modifiers):
		if key == arcade.key.W:
			self.keys['w'] = False
		if key == arcade.key.S:
			self.keys['s'] = False
		if key == arcade.key.D:
			self.keys['d'] = False
		if key == arcade.key.A:
			self.keys['a'] = False
		

game = Game()
game.setup()
game.run()


