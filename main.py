from pyengine import*
from random import*
from settings import*
create_window(window_width, window_height)
from pyengine import win_w, win_h, center_x, center_y, window
from resources import*

mouse.set_visible(False)
world_x = center_x

locations = [desert, swamp, winter]
current_track = [desert, choice([swamp, winter])]
scene = current_track[0]
n = 0
first_entry = True

WIND = False
RAIN = False
ENGINE = True

if scene == swamp:
    RAIN = True
elif scene == winter or scene == desert:
    WIND = True


class SmokeParticle(SimpleSprite):
    def __init__(self, x, y):
        super().__init__(smoke_img, x, y)
        self.add(wind, scene_car)

    def update(self):
        if self.image.get_alpha() > 0:
            self.image.set_alpha(self.image.get_alpha()-3)
            self.y -= 2
            self.x += 2
            self.image = transform.scale(self.image, (self.rect.width + 2, self.rect.height + 2))
            self.rect.width += 2
            self.rect.height += 2


class WindDust(SimpleSprite):
    def __init__(self, x, y):
        if scene in [winter, winter+swamp, swamp+winter, winter+border, border+winter, winter+winter] :
            super().__init__(snowdrop_img, x, y)
        else:
            super().__init__(wind_sand_img, x, y)
        self.add(wind, scene_car)

    def update(self):
        self.x -= wind_speed
        if self.x <= 0:
            scene_car.remove(self)
            wind.remove(self)


class RainDrop(SimpleSprite):
    def __init__(self, x, y):
        super().__init__(raindrop_img, x, y)
        self.destination = randint(int(win_h/2), win_h)
        self.add(rain, scene_car)

    def update(self):
        self.y += rain_speed
        if WIND:
            self.x -= wind_speed
        if self.y >= self.destination:
            self.kill()


class Car(SimpleSprite):
    def __init__(self, img, x, y, speed = 1):
        super().__init__(img, x, y)
        self.speed = speed
        self.orig_speed = speed
        self.original = img
        self.frame = 0
        self.fps = 0
        self.aniframe = 10
        self.hitbox = Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height/2)
        self.kilometers = 0
        self.original_height = self.rect.height

    def animate(self):
        self.fps += 1
        if self.frame == 0 and self.fps >= self.aniframe:
            self.frame = 1
            self.image = transform.scale(self.original, (self.rect.width, self.original_height))
            self.y -= 1
            self.fps = 0
        elif self.frame == 1 and self.fps >= self.aniframe:
            self.frame = 0
            self.image = transform.scale(self.original, (self.rect.width, self.original_height - 1))
            self.y += 1
            self.fps = 0

    def up(self):
        self.y -= self.speed/2
        self.aniframe = 5

    def down(self):
        self.y += self.speed/2
        self.aniframe = 5

    def right(self):
        global world_x
        for i in scene_car:
            i.x -= self.speed
        world_x += self.speed
        self.aniframe = 5
        SimpleSprite(black_square_50, self.x, self.y+14).add(scene_car, tires)
        SimpleSprite(black_square_50, self.x, self.y+20).add(scene_car, tires)
        self.kilometers += self.speed
        if chance(10):
            SmokeParticle(self.x - 16, self.rect.bottom - 16)


    def update(self):
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y + self.rect.height/2
        self.aniframe = 10
        if ENGINE:
            keys = key.get_pressed()
            if keys[K_w] or keys[K_UP]:
                self.up()
            if keys[K_s] or keys[K_DOWN]:
                self.down()
            self.right()
        self.animate()


def upgrade():
    global fuel_need
    fuel_need += 0.005
    if desert_upgrade and winter_upgrade and swamp_upgrade:
        car.image = car_ultimate_img
    elif desert_upgrade and swamp_upgrade:
        car.image = car_desert_swamp_img
    elif desert_upgrade and winter_upgrade:
        car.image = car_desert_winter_img
    elif winter_upgrade and swamp_upgrade:
        car.image = car_swamp_winter_img
    elif desert_upgrade:
        car.image = car_desert_img
    elif swamp_upgrade:
        car.image = car_swamp_img
    elif winter_upgrade:
        car.image = car_winter_img
    car.original = car.image
    car_menu.image = transform.scale(car.image, (360, 120))


car = Car(Image('images/car/car.png', size=(72, 24)), center_x/2, center_y, speed = 7)
shadow = SimpleSprite(Image('images/other/shadow.png', size = (72, 24)), car.x, car.y)
car_menu = SimpleSprite(Image('images/car/car.png', size = (360, 120)), center_x/2, center_y)
shadow_menu = SimpleSprite(Image('images/other/shadow.png', size = (360, 120)), car.x, car.y + 30)

for x in range(win_w//64+1):
    for y in range(win_h//64+1):
        SimpleSprite(choice(scene), x*64, y*64).add(scene_car, ground)

if cutscene:
    car.x = -84
    R0 = SimpleSprite(
        transform.scale(black_square, (win_w, win_h)) , 0, 0)
    R1 = SimpleSprite(
        transform.scale(black_square, (win_w, win_h/5)), 0, 0)
    R2 = SimpleSprite(
        transform.scale(black_square, (win_w, win_h/5)), 0, win_h*0.8+1)
    text_up = SimpleText('год 2052', 64, win_w/2, win_h*0.1, color = white)
    text_up.position[0] = win_w/2 - text_up.rect.width/2
    text_down = SimpleText('ты последний выживший', 64, win_w/2, win_h*0.9, color = white)
    text_down.position[0] = win_w/2 - text_down.rect.width/2
    text_center = SimpleText('CHANGES', 100, win_w/5, win_h/2)
    text_center.position[1] = center_y - text_down.rect.height/2


button_restart = SimpleText(
    ' продолжить ', 48, center_x, center_y, color=white, background=black)
button_restart.position[0] = center_x - button_restart.rect.width/2
button_restart.position[1] = center_y - button_restart.rect.height/2
kilometers_text = SimpleText(
    'км', 24, win_w-100, 0, background=gray)
location_text = SimpleText(
    'Пустыня', 24, win_w-150, kilometers_text.rect.height, background=gray)
fuel_icon = SimpleSprite(
    Image('images/UI/fuel.png'),
    win_w/3.2, win_h - 75)
fuel_bar = SimpleSprite(
    Image('images/other/black_square.png', size = (win_w/2, 20)),
    win_w/3, win_h - 50)
fuel_bar_shadow = SimpleSprite(
    Image('images/other/black_square_50.png', size = (win_w/3+5, 30)),
    win_w/3, win_h - 55)
gear = SimpleSprite(gear_img, center_x + win_w/6, 0)
heart = SimpleSprite(heart_img, center_x -75, 0)
heart_blank = SimpleSprite(heart_blank_img, center_x - 75, 0)
gears_text = SimpleText(str(gears), 36, win_w, 35)
gears_game_text = SimpleText(str(gears), 30,  win_w - 300, 10, background=gray)
fuel_text = SimpleText(str(fuel) + '/100', 36, win_w, 35)
fuel_text.position[0] = win_w - fuel_text.rect.width
menu_wall = SimpleSprite(menu_briks_img, 0, 0)
menu_floor = SimpleSprite(menu_ground_img, 0, 0)
button_continue = SimpleText(' продолжить путь -> ', 48, win_w, win_h - 100, background=gray)
button_continue.position[0] = win_w - 100 - button_continue.rect.width
button_exit = SimpleText(' выход ', 48, center_x, win_h/3*2, background=gray)
button_exit.position[0] = center_x - button_exit.rect.width/2
button_exit.position[1] = center_y + button_exit.rect.height*2
button_up_1 = SimpleSprite(upgrade_1_img, center_x + win_w/8, win_h/5)
button_up_2 = SimpleSprite(upgrade_2_img, center_x + 2*win_w/8, win_h/5)
button_up_3 = SimpleSprite(upgrade_3_img, center_x + 3*win_w/8, win_h/5)
hub_text_back = SimpleSprite(transform.scale(black_square, (win_w/3, win_h/3)), center_x + win_w/9, win_h/3)
hub_text_back.image.set_alpha(150)
hub_text_1 = SimpleText('привал', 36, center_x + win_w/8, win_h/2.5-15, color=white)
hub_text_2 = SimpleText('выберите один из апгрейдов', 24, center_x + win_w/8, win_h/2.5+50, color=white)
hub_text_3 = SimpleText('улучшение будет стоить 10 деталей', 24, center_x + win_w/8, win_h/2.5+100, color=white)
hub_text_4 = SimpleText('после этого - продолжите свой путь', 24, center_x + win_w/8, win_h/2.5+150, color=white)
button_back = SimpleSprite(button_img, 0, 0)
button_accept = SimpleText(' >улучшить< ', 36, -200, -200, background=gray)
button_rect = SimpleSprite(button_rect_img, -200, -200)
menu_heart = SimpleSprite(menu_heart_img, button_up_1.x, hub_text_back.rect.bottom + 25)
menu_gear  = SimpleSprite(menu_gear_img,  button_up_2.x, menu_heart.y)
menu_fuel  = SimpleSprite(menu_fuel_img,  button_up_3.x, menu_heart.y)


if MUSIC:                                                   # включение музыки
    music.play(paint_it_black, 100)
start_time = time.get_ticks()

while cutscene:
    time_passed = time.get_ticks() - start_time
    for e in event.get():
        if e.type == QUIT:
            cutscene = False
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE or e.key == K_SPACE:
                cutscene = False
                car.replace(center_x/2, center_y)

    for i in scene_car.sprites():
        if i.x <= -64:
            i.kill()

    if ground.sprites()[-1].x <= win_w:
        x = ground.sprites()[-1].x+64
        for y in range(win_h//64+1):
            SimpleSprite(choice(scene), x, y*64).add(scene_car, ground)


    fill_window(black)
    ground.reset()
    tires.reset()
    car.animate()
    shadow.replace(car.x-3, car.y+10)
    shadow.reset()
    car.reset()
    if WIND:
        for y in range(0, win_h):
            if chance(wind_rapid, max = 1001):
                WindDust(x = win_w, y = y).add(scene_car)
    if RAIN:
        for x in range(0, int(win_w/4)):
            if chance(rain_rapid, max = 1001):
                RainDrop(x*8, y = 0).add(scene_car)

    wind.update()
    wind.reset()
    rain.update()
    rain.reset()
    R0.reset()
    if R0.image.get_alpha() > 0:
        R0.image.set_alpha(R0.image.get_alpha()-1)
    R1.reset()
    R2.reset()
    if time_passed > 3500:
        text_up.reset()
    if time_passed > 5400:
        text_down.reset()
    if time_passed > 7500:
        text_up.position[1] -= 3
        text_down.position[1] += 3
    if time_passed > 8500:
        if car.x < center_x/4:
            car.x += 5
            SimpleSprite(black_square_50, car.x, car.y+14).add(scene_car, tires)
            SimpleSprite(black_square_50, car.x, car.y+20).add(scene_car, tires)
        else:
            car.right()
    if time_passed > 11550: #9400
        text_center.reset()
    if time_passed > 12500:
        if R1.y > -win_h/4:
            R1.y -= 2
            R2.y += 2
        if text_center.image.get_alpha() > 0:
            text_center.image.set_alpha(text_center.image.get_alpha()-3)
        else:
            if car.x < center_x/2:
                car.x += 5
            else:
                car.right()
    if time_passed > 16000:
        cutscene = False

    display.update()
    clock.tick(60)


while run:
    if CURRENT_SCENE == 'game':                                 # сцена игры
        if ENGINE:
            mouse.set_visible(False)
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    CURRENT_SCENE = 'menu'
                if e.key == K_SPACE:
                    if mouse.get_visible():
                        if lives > 0 and fuel > 1:
                            sprite.spritecollide(car, walls, True)
                            ENGINE = True
                            mouse.set_visible(False)
                            music.set_volume(1)
                        else:
                            run = False
            if e.type == MOUSEBUTTONDOWN:
                if not ENGINE:
                    if button_restart.rect.collidepoint(mouse.get_pos()):
                        if lives > 0 and fuel > 1:
                            sprite.spritecollide(car, walls, True)
                            ENGINE = True
                            mouse.set_visible(False)
                            music.set_volume(1)
                        else:
                            run = False

        fill_window(gray)
        for i in scene_car.sprites():
            if i.x <= -64:
                i.kill()

        if WIND:                                            # ветер и снег
            for y in range(0, win_h):
                if chance(wind_rapid, max = 1001):
                    WindDust(x = win_w, y = y).add(scene_car)
        if RAIN:                                            # дождь
            for x in range(0, int(win_w/4)):
                if chance(rain_rapid, max = 1001):
                    RainDrop(x*8, y = 0).add(scene_car)

        if ground.sprites()[-1].x <= win_w:                 # спавн новых тайлов
            x = ground.sprites()[-1].x+64
            for y in range(win_h//64+1):
                SimpleSprite(choice(scene), x, y*64).add(scene_car, ground)
                if chance(1) and scene != border and scene != finish:               # ящики
                    SimpleSprite(crate_img, x, y*64).add(scene_car, crates)

                elif chance(1) and scene != border and scene != finish:             # бочки
                    SimpleSprite(fuel_img, x, y*64).add(scene_car, barrels)

                elif chance(walls_chance) and scene in [desert, winter]:  # стены
                    SimpleSprite(wall_img, x, y*64).add(scene_car, walls)

                elif chance(20) and scene == swamp:             # вода
                    SimpleSprite(water_img, x, y*64).add(scene_car, water)

        for c in crates.sprites():                          # столкновение с ящиками
            if c.rect.colliderect(car.hitbox) and ENGINE:
                c.image = broken_crate_img
                c.rect.width = c.rect.height = 0
                gears += 1

        for b in barrels.sprites():                         # столкновение с бочкой
            if b.rect.colliderect(car.hitbox) and ENGINE:
                b.image = fuel_broken_img
                b.rect.width = b.rect.height = 0
                fuel = fuel + 10
                if fuel > fuel_max:
                    fuel = fuel_max

        for w in walls.sprites():                           # столкновение со стенами
            if w.rect.colliderect(car.hitbox) and ENGINE:
                if winter_upgrade:
                    w.image = fuel_broken_img
                    w.rect.width = 0
                    w.rect.height = 0
                else:
                    ENGINE = False
                    time_dead = time.get_ticks()
                    lives -= 1
                    music.set_volume(0.5)

        for w in water.sprites():                           # торможение об воду в болоте
            if w.rect.colliderect(car.hitbox) and ENGINE:
                if swamp_upgrade:
                    car.speed *= 1.25
                else:
                    car.speed *= 0.5

        if scene == desert and desert_upgrade:              # ускорение в пустыне
            car.speed *= 1.25
        if scene == winter and winter_upgrade:              # торможение в тундре
            car.speed *= 0.75

        ground.reset()                                      # отрисовка графики
        crates.reset()
        crates.reset()
        barrels.reset()
        tires.reset()

        shadow.replace(car.x-3, car.y+10)
        walls.reset()
        shadow.reset()
        water.reset()
        car.update()
        car.reset()

        wind.update()
        wind.reset()
        rain.update()
        rain.reset()

        car.speed = car.orig_speed

        if not ENGINE:                                      # кнопка рестарт
            if (time.get_ticks() - time_dead) > 1000:
                mouse.set_visible(True)
                if lives == 0 or fuel <= 0.5:
                    button_restart.setText(' игра окончена ')
                    button_restart.position[0] = center_x - button_restart.rect.width/2
                    music.set_volume(0.5)
                button_restart.reset()

        kilometers_text.setText(str(int(car.kilometers//10)) + ' м')
        kilometers_text.position[0] = win_w - kilometers_text.rect.width
        kilometers_text.reset()
        if scene == winter:
            location_text.setText('Тундра')
        elif scene == desert:
            location_text.setText('Пустыня')
        elif scene == swamp:
            location_text.setText('Болота')
        else:
            location_text.setText('')
        location_text.position[0] = win_w - location_text.rect.width
        location_text.reset()

                                              # работа с топливом
        fuel_bar.image = transform.scale(fuel_bar.image, (win_w/3 * fuel/fuel_max, 20))
        fuel_bar_shadow.reset()
        fuel_bar.reset()
        fuel_icon.replace(win_w/3.2, win_h - 75)
        fuel_icon.reset()
        if ENGINE:
            fuel -= fuel_need
        if fuel <= 0.5 and ENGINE:
            ENGINE = False
            time_dead = time.get_ticks()


        gears_game_text.setText('   x ' + str(gears))
        gears_game_text.reset()
        gear.replace(win_w - 325, 0)
        gear.reset()

        for x in range(3):
            if lives >= x+1:
                heart.replace(center_x - 75 + 50*x, 0)
                heart.reset()
            else:
                heart_blank.replace(center_x - 75 + 50*x, 0)
                heart_blank.reset()

        if first_entry:                                             # старт локаций
            if car.kilometers//10 == way_len:
                scene = current_track[0] + current_track[1]
                if current_track[1]== winter or current_track[1] == desert:
                    WIND, RAIN = True, False
                elif current_track[1] == swamp:
                    WIND, RAIN = False, True
            elif car.kilometers//10 == way_len + 100:
                scene = current_track[1]
                if scene == winter or scene == desert:
                    WIND, RAIN = True, False
                elif scene == swamp:
                    WIND, RAIN = False, True
            elif car.kilometers//10 == way_len*2 + 100:
                scene = current_track[1] + border
            elif car.kilometers//10 == way_len*2 + 200:
                scene = border
                RAIN = WIND = False
            elif car.kilometers//10 == way_len*2 + 400:
                CURRENT_SCENE = 'hub'

        else:                                                       # переход локаций
            if car.kilometers//10 < 100:
                scene = current_track[0] + border
                if current_track[0] == winter or current_track[0] == desert:
                    WIND, RAIN = True, False
                elif current_track[0] == swamp:
                    WIND, RAIN =  False, True

            elif car.kilometers//10 == 100:
                scene = current_track[0]
                if scene == winter or scene == desert:
                    WIND, RAIN = True, False
                elif scene == swamp:
                    WIND, RAIN = False, True

            elif car.kilometers//10 == way_len + 100:
                scene = current_track[0] + current_track[1]
                if current_track[1]== winter or current_track[1] == desert:
                    WIND, RAIN = True, False
                elif current_track[1] == swamp:
                    WIND, RAIN = False, True

            elif car.kilometers//10 == way_len + 300:
                scene = current_track[1]
                if scene == winter or scene == desert:
                    WIND, RAIN = True, False
                elif scene == swamp:
                    WIND, RAIN = False, True

            elif car.kilometers//10 == way_len*2 + 300:
                scene = current_track[1] + border
                WIND = RAIN = False

            elif car.kilometers//10 == way_len*2 + 500:
                scene = border

            elif car.kilometers//10 == way_len*2 + 700:
                if desert_upgrade and winter_upgrade and swamp_upgrade:
                    scene = finish
                else:
                    CURRENT_SCENE = 'hub'
                    first_entry = True
            elif car.kilometers//10 == way_len*2 + 800:
                run = False

    elif CURRENT_SCENE == 'hub':                                # сцена хаба
        if first_entry:
            mouse.set_visible(True)
            fill_window(dark_gray)
            fuel_icon.replace(fuel_text.position[0] - fuel_icon.rect.width - 10, 25)
            gears_text.position[0] = fuel_icon.x - gears_text.rect.width - 65
            gears_text.position[1] = 35
            button_continue.position[0] = win_w - 100 - button_continue.rect.width
            button_continue.position[1] = win_h - 100
            button_exit.position[1] = button_continue.position[1]
            button_exit.position[0] = 100
            first_entry = False
            music.set_volume(0.5)

        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == MOUSEBUTTONDOWN:
                if button_continue.rect.collidepoint(mouse.get_pos()):          # переключение на игру
                    CURRENT_SCENE = 'game'
                    car.kilometers = 0
                    current_track[0] = current_track[1]
                    current_track[1] = choice(locations)
                    scene = current_track[0]
                    walls_chance += 1
                    button_accept.position = [-200, -200]
                    button_rect.replace(-200, -200)
                    first_entry = False
                    music.set_volume(1)

                elif button_exit.rect.collidepoint(mouse.get_pos()):            # выход
                    run = False
                elif button_accept.rect.collidepoint(mouse.get_pos()):
                    if gears >= 10:
                        gears -= 10
                        if button_rect.y == menu_heart.y-14 and button_rect.x == menu_heart.x-14:
                            if lives < 3:
                                lives += 1
                            else:
                                gears += 10
                        elif button_rect.y == menu_gear.y-14 and button_rect.x == menu_gear.x-14:
                            fuel_max += 10
                            fuel += 10
                            if fuel > fuel_max:
                                fuel = fuel_max
                        elif button_rect.y == menu_fuel.y-14 and button_rect.x == menu_fuel.x-14:
                            fuel += 50
                            if fuel > fuel_max:
                                fuel = fuel_max
                        elif button_rect.x == button_up_1.x-14:
                            desert_upgrade = True
                            car.orig_speed *= 1.25
                            button_up_1.x = - 200
                        elif button_rect.x == button_up_2.x-14:
                            swamp_upgrade = True
                            button_up_2.x = - 200
                        elif button_rect.x == button_up_3.x-14:
                            winter_upgrade = True
                            button_up_3.x = - 200
                        upgrade()

                elif button_up_1.rect.collidepoint(mouse.get_pos()):
                    hub_text_1.setText('улучшение пустыни')
                    hub_text_2.setText('> увеличивает скорость машины')
                    hub_text_3.setText('> добавляет маневренности')
                    hub_text_4.setText('> машине требуется больше топлива')
                    button_accept.position = [
                        hub_text_back.x + hub_text_back.rect.width/2 - button_accept.rect.width/2,
                        hub_text_back.rect.bottom - button_accept.rect.height*1.5]
                    button_rect.replace(button_up_1.x-14, button_up_1.y-32)
                elif button_up_2.rect.collidepoint(mouse.get_pos()):
                    hub_text_1.setText('улучшение болота')
                    hub_text_2.setText('> увеличивает скорость в болотах')
                    hub_text_3.setText('> машина не вязнет в трясине')
                    hub_text_4.setText('> машине требуется больше топлива')
                    button_accept.position = [
                        hub_text_back.x + hub_text_back.rect.width/2 - button_accept.rect.width/2,
                        hub_text_back.rect.bottom - button_accept.rect.height*1.5]
                    button_rect.replace(button_up_2.x-14, button_up_2.y-32)
                elif button_up_3.rect.collidepoint(mouse.get_pos()):
                    hub_text_1.setText('улучшение тундры')
                    hub_text_2.setText('> позволяет уничтожать препятствия')
                    hub_text_3.setText('> замедляет машину в снегах')
                    hub_text_4.setText('> машине требуется больше топлива')
                    button_accept.position = [
                        hub_text_back.x + hub_text_back.rect.width/2 - button_accept.rect.width/2,
                        hub_text_back.rect.bottom - button_accept.rect.height*1.5]
                    button_rect.replace(button_up_3.x-14, button_up_3.y-32)
                elif menu_heart.rect.collidepoint(mouse.get_pos()):
                    hub_text_1.setText('ремонт машины')
                    hub_text_2.setText('> восстанавливает одну жизнь')
                    hub_text_3.setText('> максимум - 3 жизни')
                    hub_text_4.setText('> стоит 10 деталей')
                    button_accept.position = [
                        hub_text_back.x + hub_text_back.rect.width/2 - button_accept.rect.width/2,
                        hub_text_back.rect.bottom - button_accept.rect.height*1.5]
                    button_rect.replace(menu_heart.x-14, menu_heart.y-14)
                elif menu_gear.rect.collidepoint(mouse.get_pos()):
                    hub_text_1.setText('расширенный бак')
                    hub_text_2.setText('> вмещает на 10 единиц')
                    hub_text_3.setText('   топлива больше ({})'.format(str(fuel_max+10)))
                    hub_text_4.setText('> стоит 10 деталей')
                    button_accept.position = [
                        hub_text_back.x + hub_text_back.rect.width/2 - button_accept.rect.width/2,
                        hub_text_back.rect.bottom - button_accept.rect.height*1.5]
                    button_rect.replace(menu_gear.x-14, menu_gear.y-14)
                elif menu_fuel.rect.collidepoint(mouse.get_pos()):
                    hub_text_1.setText('переработка топлива')
                    hub_text_2.setText('> перерабатывает 10 деталей')
                    hub_text_3.setText('   в 50 единиц топлива')
                    hub_text_4.setText('> максимум - {} единиц'.format(str(fuel_max)))
                    button_accept.position = [
                        hub_text_back.x + hub_text_back.rect.width/2 - button_accept.rect.width/2,
                        hub_text_back.rect.bottom - button_accept.rect.height*1.5]
                    button_rect.replace(menu_fuel.x-14, menu_fuel.y-14)

        fuel_text.setText(str(int(fuel)) + '/' + str(fuel_max))
        gears_text.setText(str(gears))
        gear.replace(gears_text.position[0] - gear.rect.width - 10, 25)
        fuel_text.position[0] = win_w - fuel_text.rect.width - 10

        for x in range(win_w//128 + 1):
            for y in range(win_h//128//2):
                menu_wall.replace(x*128, y*128)
                menu_wall.reset()
            for y in range(win_h//128//2, win_h//128 + 1):
                menu_floor.replace(x*128, y*128)
                menu_floor.reset()

        for i in range(3):
            if lives >= i+1:
                heart.replace(gear.x - 200 + i*50, 25)
                heart.reset()
            else:
                heart_blank.replace(gear.x - 200 + i*50, 25)
                heart_blank.reset()

        for i in [
            shadow_menu, car_menu, gears_text, fuel_text,
            gear, fuel_icon, button_continue]:
            i.reset()
        for i in [button_up_1, button_up_2, button_up_3]:
            button_back.replace(i.x-14, i.y-32)
            button_back.reset()
        for i in [menu_heart, menu_gear, menu_fuel]:
            button_back.replace(i.x-14, i.y-14)
            button_back.reset()
        for i in [
            button_up_1, button_up_2, button_up_3, button_exit, hub_text_back,
            hub_text_1, hub_text_2, hub_text_3, hub_text_4, button_accept,
            button_rect, menu_gear, menu_heart, menu_fuel]:
            i.reset()

    elif CURRENT_SCENE == 'menu':                               # сцена меню
        music.set_volume(0.5)
        mouse.set_visible(True)
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN:
                if button_continue.rect.collidepoint(mouse.get_pos()):
                    CURRENT_SCENE = 'game'
                    music.set_volume(1)
                elif button_exit.rect.collidepoint(mouse.get_pos()):
                    run = False
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    CURRENT_SCENE = 'game'
                    music.set_volume(1)

        button_exit.position[0] = center_x - button_exit.rect.width/2
        button_exit.position[1] = center_y + button_exit.rect.height*2
        button_continue.position[0] = center_x - button_continue.rect.width/2
        button_continue.position[1] = center_y - button_continue.rect.height*2
        button_continue.reset()
        button_exit.reset()

    display.update()
    clock.tick(60)


if scene == finish:
    cutscene = True
    start_time = time.get_ticks()
    text_center = SimpleText(' to be continued... ', 64 , 0, 0, background=gray)
    text_center.position[0] = center_x - text_center.rect.width/2
    text_center.position[1] = center_y - text_center.rect.height/2
    R1.y = -win_h/4
    R2.y = win_h
    R2.image = transform.scale(R2.image, (win_w, win_h/2))

    R0.image.set_alpha(0)

while cutscene:
    time_passed = time.get_ticks() - start_time
    for e in event.get():
        if e.type == QUIT:
            cutscene = False
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE or e.key == K_SPACE:
                cutscene = False

    if car.x < win_w + 200:
        car.x += 5
        SimpleSprite(black_square_50, car.x, car.y+14).add(tires)
        SimpleSprite(black_square_50, car.x, car.y+20).add(tires)

    fill_window(gray)
    ground.reset()
    tires.reset()
    car.animate()
    shadow.replace(car.x-3, car.y+10)
    shadow.reset()
    car.reset()

    if R1.y < 0 and time_passed > 2:
        R1.y += 2
        R2.y -= 2

    if R1.y == 0:
        text_center.reset()

    R1.reset()
    R2.reset()

    if time_passed > 5500 and R0.image.get_alpha() < 255:
        R0.image.set_alpha(R0.image.get_alpha() + 1)
    R0.reset()

    if time_passed > 12000:
        text_center = SimpleText('конец', 64 , 0, 0, color=white)
        text_center.position[0] = center_x - text_center.rect.width/2
        text_center.position[1] = center_y - text_center.rect.height/2
        text_center.reset()

    display.update()
    clock.tick(60)
