from pyengine import*

load_text = SimpleText('ЗАГРУЗКА', 36, center_x-100, center_y-50, color=white)
load_text.reset()
display.update()

desert = [Image('images/tiles/sand.png')]
swamp = [Image('images/tiles/swamp1.png'), Image('images/tiles/swamp2.png'), Image('images/tiles/swamp2.png')]
border = [Image('images/tiles/brick.png')]
winter = [Image('images/tiles/snow1.png'), Image('images/tiles/snow2.png')]
finish = [Image('images/tiles/crate_11.png')]

crate_img = Image('images/tiles/crate_24.png')          # тайлы и ресурсы
fuel_img = Image('images/tiles/fuel.png')
fuel_broken_img = Image('images/tiles/crate_36.png')
wall_img = Image('images/tiles/block_02.png')
water_img = Image('images/tiles/water.png')
broken_crate_img = Image('images/tiles/crate_32.png')

gear_img = Image('images/UI/gear.png')                  # картинки ui
heart_img = Image('images/UI/heart.png', size = (50, 50))
heart_blank_img = Image('images/UI/heart_blank.png', size = (50, 50))
menu_heart_img = Image('images/UI/heart.png', size=(108, 108))
menu_gear_img = Image('images/UI/gear.png', size=(108, 108))
menu_fuel_img = Image('images/UI/fuel.png', size=(108, 108))

black_square = Image('images/other/black_square.png')   # частицы и квадраты
black_square_50 = Image('images/other/black_square.png')
black_square_50.set_alpha(50)
raindrop_img = Image('images/other/raindrop.png', size = (8, 16))
snowdrop_img = Image('images/other/snowdrop.png', size = (8, 4))
wind_sand_img = Image('images/other/wind_sand.png', size = (8, 4))
smoke_img = Image('images/other/tile_0008.png', size=(16, 16))

car_desert_img = Image('images/car/desert.png')         # варианты машины
car_winter_img = Image('images/car/winter.png')
car_swamp_img = Image('images/car/swamp.png')
car_desert_winter_img = Image('images/car/desert-winter.png')
car_desert_swamp_img = Image('images/car/desert-swamp.png')
car_swamp_winter_img = Image('images/car/swamp-winter.png')
car_ultimate_img = Image('images/car/ultimate.png')

menu_briks_img = Image('images/tiles/block_06.png', size=(128, 128))  # хаб
menu_ground_img = Image('images/tiles/crate_11.png', size=(128, 128))
upgrade_1_img = Image('images/UI/desert.png', size=(108, 72))
upgrade_2_img = Image('images/UI/swamp.png', size=(108, 72))
upgrade_3_img = Image('images/UI/winter.png', size=(108, 72))
button_img = Image('images/UI/crate_09.png', size=(136, 136))
button_rect_img = Image('images/UI/environment_06.png', size=(136, 136))


music = mixer.Channel(1)
paint_it_black = mixer.Sound('sounds/paint.mp3')
#paint_it_black = mixer.Sound('sounds/naruto.mp3')

scene_car = Group()
ground = Group()
tires = Group()
walls = Group()
water = Group()
crates = Group()
barrels = Group()

wind = Group()
rain = Group()

