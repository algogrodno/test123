from os import remove
import pygame as pg
from other import set_text
from sprites import *
from config import *
from other import *
from random import randint
from time import time
pg.init()

pg.display.set_caption("Star Aliens")
mw = pg.display.set_mode(WINDOWS_SIZE)
mw.fill(BACK_COLOR)
clock = pg.time.Clock()


background = pg.transform.scale(pg.image.load('pic\\fon1.jpg'),(WINDOWS_SIZE))
ship = Ship('pic\\starship2.png', WINDOWS_SIZE[0]/2,WINDOWS_SIZE[1]-150,70,100)

#boom_sprites = sprites_load('pic\\boom2', 'boom',(100,100), (0,0,0))
#boom_sprites = sprites_load('pic\\boom3', 'boom', (100,100))
boom_sprites = sprites_load('pic\\boom4', 'boom', (100,100), (0,0,0))
ufo_sprites = sprites_load('pic\\ufo1', 'ufo', (100,90))
meteors_sprites = [sprites_load('pic\\meteor1', 'meteor', (80,80)),
                   sprites_load('pic\\meteor1', 'meteor', (60,60)),
                   sprites_load('pic\\meteor1', 'meteor', (40,40))]
# print(len(meteors_sprites))


sound_fon = pg.mixer.Sound('snd\\fon1.mp3')
sound_fire = pg.mixer.Sound('snd\\fire1.mp3')
sound_boom = pg.mixer.Sound('snd\\boom1.mp3')
sound_fon.set_volume(0.1)
sound_fire.set_volume(0.1)
sound_boom.set_volume(0.1)
sound_fon.play(-1)


stars = pg.sprite.Group()
fiers = pg.sprite.Group()
aliens = pg.sprite.Group()
booms = pg.sprite.Group()
meteors = pg.sprite.Group()

for i in range(20): stars.add(Star(True))

SCORE = 0
TICKS = 0
ticks = 0
fps = 0
key_wait = 0
play = True
gameover = False
t = time()

while play:
    for e in pg.event.get():            
            if e.type == pg.QUIT or \
                    (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                play  = False    
    
            # if e.type == pg.KEYDOWN:
            #     if e.key == pg.K_UP:
            #         print('up-ok')
            #     elif e.key == pg.K_DOWN:
            #         print('down-ok')
            # elif e.type == pg.KEYUP:
            #     if e.key == pg.K_UP:
            #         print('up-no')
            #     elif e.key == pg.K_DOWN:
            #         print('down-no')

    
    mw.blit(background,(0,0))

    if TICKS % STAR_WAIT == 0:        
        stars.add(Star())

    stars.update()
    stars.draw(mw)

    if gameover:
        game_over(mw)        
    else:
        

        if True: # управление 
            if pg.key.get_pressed()[pg.K_DOWN]:
                ship.movey = 'down'
            if pg.key.get_pressed()[pg.K_UP]:
                ship.movey = 'up'
            if pg.key.get_pressed()[pg.K_RIGHT]:
                ship.movex = 'right'
            if pg.key.get_pressed()[pg.K_LEFT]:
                ship.movex = 'left'
            if pg.key.get_pressed()[pg.K_SPACE]: # ОГОНЬ
                ship.fire(fiers, sound_fire, FIRE_WAIT)  

            if pg.key.get_pressed()[pg.K_1]: # скорость корабля -
                ship.speed -= 1        
            if pg.key.get_pressed()[pg.K_2]: # скорость корабля +
                ship.speed += 1
            if pg.key.get_pressed()[pg.K_3]: # скорость стрельбы +        
                if FIRE_WAIT > 2:  FIRE_WAIT -= 1 
                else: FIRE_WAIT =  1
            if pg.key.get_pressed()[pg.K_4]: # скорость стрельбы -
                FIRE_WAIT += 1    
            if pg.key.get_pressed()[pg.K_5]: # скорость НЛО +
                for alien in aliens:
                    alien.speed += 1        
            if pg.key.get_pressed()[pg.K_6]: # скорость НЛО +
                for alien in aliens:            
                    if alien.speed > 2:  alien.speed -= 1 
                    else: alien.speed =  1
            
            if pg.key.get_pressed()[pg.K_q]:    # Добавить НЛО
                Alien(ufo_sprites, aliens)
                alien_wait = 5
            if pg.key.get_pressed()[pg.K_a]:  # включить/выключить появление НЛО
                if key_wait == 0:
                    ALIEN = not ALIEN
                    key_wait = KEY_WAIT
                else:
                    key_wait -= 1 
            
        
        # добавляем НЛО через заданный период
        if TICKS % NEW_ALIEN_WAIT == 0 :
            if ALIEN and len(aliens) < ALIENS_LIMIT:  
                #alien_add(aliens, ALIEN_SPEED, ufo_sprites)
                Alien(ufo_sprites, aliens)
        
        # добавляем метеоры через заданный период
        if TICKS % NEW_METEOR_WAIT == 0 :            
            Meteor(meteors_sprites, meteors)


        # попаднаия пуль в НЛО
        collisions = pg.sprite.groupcollide(aliens, fiers, True, True)
        for a, f in collisions.items():       
            #print(a.rect.x, f[0].rect.x)
            SCORE += 1
            if SCORE % FIRE_BONUS == 0: 
                # каждые десять очков бонус к стрельбе
                FIRE_WAIT -= 2
                if FIRE_WAIT<2:FIRE_WAIT = 2
            NEW_ALIEN_WAIT -= 2
            if NEW_ALIEN_WAIT <= 0 : NEW_ALIEN_WAIT = 4
            ALIEN_SPEED += 0.05

            # рисуем взрыв на месте НЛО
            Boom(a.rect.center, boom_sprites, booms)
            sound_boom.play()

        # столкновение игрока и НЛО
        # if pg.sprite.spritecollide(ship, aliens, False):
        #     gameover = True
    
        #print(TICKS, len(aliens), aliens)

        aliens.update(ship)
        aliens.draw(mw)
        
        fiers.update()
        fiers.draw(mw)            
        
        booms.update()
        booms.draw(mw)

        meteors.update()
        meteors.draw(mw)
        
        ship.update()
        ship.draw(mw)
        
        # подсчет FPS
        t2 = time()
        if t2-t > 1:                        
            t = t2        
            fps = TICKS-ticks
            ticks = TICKS

        # текст
        set_text(mw, f"Скорость - {ship.speed}", 30, (10,10))    
        set_text(mw, f"Огонь - {int(FIRE_WAIT)}", 30, (870,10))
        set_text(mw, int(ALIEN), 30, (960,680))
        set_text(mw, f"Чужих - {len(aliens)}", 30, (10,680))
        set_text(mw,f"ОЧКИ - {SCORE}", 40, (500,10))
        set_text(mw,f"звезд-{len(stars)}", 30, (500,680))
        set_text(mw,f"метеоров-{len(meteors)}", 30, (300,680))
        set_text(mw, f"x-{ship.rect.x} y-{ship.rect.y}", 30, (150,680))
        set_text(mw,f"fps-{fps}", 30, (700,680))

    
    # добавляем звезды через заданный период
    # тут для того что бы ивдны были даже когда гамеовер
    

    

    pg.display.update()
    clock.tick(FPS)
    #pg.event.pump()
    TICKS += 1

pg.quit()