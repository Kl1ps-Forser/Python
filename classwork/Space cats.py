import time
from sprite import *

def dialogue_mode(sprite, text):
    sprite.update()
    screen.blit(space, (0, 0))
    screen.blit(sprite.image, sprite.rect)

    text1 = f1.render(text[text_number], True, 'White')
    screen.blit(text1, (280, 450))

    if text_number < len(start_text) - 1:
        if text_number < 2:
            text2 = f1.render(text[text_number + 1], True, 'White')
            screen.blit(text2, (280, 470))
        else:
            text2 = f1.render(text[3], True, 'White')
            screen.blit(text2, (280, 470))

pg.init()
pg.mixer.init()

size = (800, 600)
screen = pg.display.set_mode(size)
pg.display.set_caption("Космические коты")

FPS = 120
clock = pg.time.Clock()

is_running = True
mode = "start_scene"

meteorites = pg.sprite.Group()
mice = pg.sprite.Group()
lasers = pg.sprite.Group()

space = pg.image.load('фон.png')
space = pg.transform.scale(space, size)

heart = pg.image.load('heart.png')
heart = pg.transform.scale(heart, (30, 30)).convert_alpha()
heart_count = 3

captain = Captain()
alien = Alien()
star_ship = Starship()

start_text = ["Мы засекли сигнал с планеты Мур.",
              "",
              "Наши друзья, инопланетные коты,",
              "нуждаются в помощи.",
              "Космические мыши хотят съесть их луну,",
              "потому что она похожа на сыр.",
              "Как долго наш народ страдал от них, ",
              "теперь и муряне в беде...",
              "Мы должны помочь им.",
              "Вылетаем прямо сейчас.",
              "Спасибо, что починил звездолёт, штурман. ",
              "Наконец-то функция автопилота работает.",
              "Поехали!"]

alien_text = ["СПАСИТЕ! МЫ ЕЛЕ ДЕРЖИМСЯ!",
              "",
              "Мыши уже начали грызть луну...",
              "Скоро куски луны будут падать на нас.",
              "Спасите муриан!", ]

final_text = ["Огромное вам спасибо,",
              "друзья с планеты Мяу!",
              "Как вас называть? Мяуанцы? Мяуриане?",
              "В любом случае, ",
              "теперь наша планета спасена!",
              "Мы хотим отблагодарить вас.",
              "Капитан Василий и его штурман получают",
              "орден SKYSMART.",
              "А также несколько бутылок нашей",
              "лучшей валерьянки.",
              "",
              ""]

text_number = 0

f1 = pg.font.Font('шрифт.otf', 25)

pg.mixer.music.load('background.wav')
pg.mixer.music.set_volume(0.3)
pg.mixer.music.play()
laser_sound = pg.mixer.Sound('laser.wav')
fight = pg.mixer.Sound('fight.wav')

while is_running:
    # СОБЫТИЯ
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
        if event.type == pg.KEYDOWN:
            if mode == 'start_scene':
                text_number += 2
                if text_number > len(start_text):
                    text_number = 0
                    mode = 'meteorites'
                    start_time = time.time()

            if mode == 'alien_scene':
                text_number += 2
                if text_number > len(alien_text):
                    text_number = 0
                    alien.rect.topleft = (-30, 600)

                    alien.mode = "up"
                    mode = 'moon'
                    start_time = time.time()
                    star_ship.switch_mode()

            if mode == 'final_scene':
                text_number += 2
                if text_number > len(final_text):
                    text_number = 0
                    mode = 'end'

            if mode == 'moon':
                if event.key == pg.K_SPACE:
                    lasers.add(Laser(star_ship.rect.midtop))
                    laser_sound.play()

    # ОБНОВЛЕНИЯ
    if mode == "start_scene":
        dialogue_mode(captain, start_text)

    if mode == "meteorites":
        fight.set_volume(0.5)
        fight.play()

        if time.time() - start_time > 3.0:
            mode = "alien_scene"

        if random.randint(1, 50) == 1:
            meteorites.add(Meteorite())

        star_ship.update()
        meteorites.update()

        hits = pg.sprite.spritecollide(star_ship, meteorites, True)
        for hit in hits:
            heart_count -= 1
            if heart_count == 0:
                is_running = False

        screen.blit(space, (0, 0))
        screen.blit(star_ship.image, star_ship.rect)
        meteorites.draw(screen)
        for i in range(heart_count):
            screen.blit(heart, (i * 30, 10))

    if mode == "alien_scene":
        dialogue_mode(alien, alien_text)

    if mode == "moon":
        if time.time() - start_time > 5.0:
            mode = "final_scene"
        fight.play()

        if random.randint(1, 50) == 1:
            mice.add(Mouse_starship())

        star_ship.update()
        mice.update()
        lasers.update()

        hits = pg.sprite.spritecollide(star_ship, mice, dokill=True)
        for hit in hits:
            heart_count -= 1
            if heart_count == 0:
                is_running = False

        hits = pg.sprite.groupcollide(lasers, mice, True, True)

        screen.blit(space, (0, 0))
        screen.blit(star_ship.image, star_ship.rect)
        mice.draw(screen)
        lasers.draw(screen)
        for i in range(heart_count):
            screen.blit(heart, (i * 30, 10))

    if mode == "final_scene":
        dialogue_mode(alien, final_text)

    pg.display.flip()
    clock.tick(FPS)
