
import pygame as pg

from random import randint



class Base_sprite(pg.sprite.Sprite):
    def __init__(self, pic, x, y, w, h, speed_x=0, speed_y=0):
        super().__init__()
        self.picture = pg.transform.scale(
            pg.image.load(pic).convert_alpha(), (w, h)
        )
        self.image = self.picture
        self.rect = self.picture.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        
                
    def draw(self):
        mw.blit(self.picture, (self.rect.x, self.rect.y))
        # pg.draw.rect(mw, (255,0,0), self.rect, 3)


    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

class Hero(Base_sprite):
    energy = 0
    health = 100

    def update(self):
        self.energy += 1
        self.draw_health()

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.x >= 5:
            self.rect.x -= self.speed_x
            
        if keys[pg.K_RIGHT] and self.rect.x <= win_w - self.rect.width:            
            self.rect.x += self.speed_x 
            
        if keys[pg.K_UP] and self.rect.y >= 5:
            self.rect.y -= self.speed_y 
              
        if keys[pg.K_DOWN] and self.rect.y <= win_h - self.rect.height:            
            self.rect.y += self.speed_y
        
        if keys[pg.K_SPACE]:                       
                self.fire()
                
    def draw_health(self):
        rect1 = pg.Rect(self.rect.x, 
                        self.rect.bottom, 
                        self.rect.width / 100 * self.health, 
                        8)
        rect2 = pg.Rect(self.rect.x, 
                        self.rect.bottom, 
                        self.rect.width, 
                        10)
        g = int(255/100*self.health)
        if g<0:
            g = 0
        r = int(255 - g)        
        b = 50
        # print(r, g, b)
        pg.draw.rect(mw,(r,g,b), rect1)
        pg.draw.rect(mw,(200,200,30), rect2, 2)

    def draw(self):
        super().draw()
        self.draw_health()

    def fire(self):
        if self.energy >= 30:
            self.energy = 0 
            fire.play()
            w = 16
            h = 40
            bullet = Bullet('fire1.png', 
                            self.rect.x + self.rect.width/2 - w/2, 
                            self.rect.y - h,
                            w, h,
                            speed_x=0, speed_y=-5)
            bullets.add(bullet)
            all_sprite.add(bullet)
                   

class Star(Base_sprite):
    def update(self):
        super().update()
        if self.rect.y > win_size[y]:
            # stars.remove(self)
            self.kill()


class Ufo(Base_sprite):
    def update(self):
        global ufo_missed
        super().update()
        if self.rect.y > win_size[y]:
            # ufos.remove(self)
            self.kill()
            ufo_missed += 1


class Bullet(Base_sprite):
    pass



class Boom(pg.sprite.Sprite):
    def __init__(self, ufo_center, boom_sprites, booms) -> None:
        super().__init__() 
        #global booms, boom_sprites              
        self.frames = boom_sprites        
        self.frame_rate = 1   
        self.frame_num = 0
        self.image = boom_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = ufo_center
        self.add(booms)
        self.add(all_sprite)

    
    def next_frame(self):
        self.image = self.frames[self.frame_num]
        self.frame_num += 1
        if self.frame_num > len(self.frames)-1:
            self.frame_num = 0
        
    
    def update(self):
        self.next_frame()
        if self.frame_num == len(self.frames)-1:
            self.kill()



def sprites_load(folder, file_name, size, colorkey=(0,0,0)):    
    sprites = []
    load = True
    num = 1
    while load:
        try:
            spr = pg.image.load(f'{folder}\\{file_name}{num}.png')
            spr = pg.transform.scale(spr,size)
            if colorkey: spr.set_colorkey(colorkey)
            sprites.append(spr)
            num += 1
        except:
            load = False
    return sprites



def set_text(text, x, y, color=(255,255,200)):
    mw.blit(
        font1.render(text, True, color),(x,y)
    )


def spawn_star():
    size = randint(15, 40)
    star = Star('star1.png', randint(0, win_size[x]), -10, size, size, 0, randint(2, 9))
    stars.add(star)
    all_sprite.add(star)

def spawn_ufo():
    ufo = Ufo('ufo1.png', randint(0, win_size[x]-90), -100, 90, 90, 0, randint(1, 4))
    ufos.add(ufo)
    all_sprite.add(ufo)

pg.font.init()
font1 = pg.font.Font(None, 36)
# font2 = font.Font(None, 20)

win_w = 900
win_h = 700
win_size = (win_w, win_h)
x, y =0, 1

# mw = pg.display.set_mode((win_w, win_h), pg.FULLSCREEN)
mw = pg.display.set_mode(win_size)
pg.display.set_caption("Марс атакует")
clock = pg.time.Clock()


fon = pg.transform.scale(
    pg.image.load("fon2.jpg"), win_size)
fon_go = pg.transform.scale(
    pg.image.load("gameover.jpg"), win_size)

#музыка
pg.mixer.init()
pg.mixer.music.load('space.ogg')
pg.mixer.music.play()
fire = pg.mixer.Sound('laser.ogg')
boom_sound = pg.mixer.Sound('boom1.ogg')


# stars = []
# ufos = []
# bullets = []

boom_sprites = sprites_load('boom4', 'boom', (80,80))
# print(len(boom_sprites))

stars = pg.sprite.Group()
ufos = pg.sprite.Group()
bullets = pg.sprite.Group()
booms = pg.sprite.Group()
all_sprite = pg.sprite.Group()

font1 = pg.font.Font(None, 40)

hero = Hero('ship5.png', win_w/2 - 30, win_h - 150, 60, 80, 5, 5)
all_sprite.add(hero)


play = True
win = False
game = True
ticks = 1
ufo_missed = 0

while play:

    for e in pg.event.get():
        if e.type == pg.QUIT or \
                    (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                play  = False

    if game:        
        if ticks % 10 == 0: spawn_star()
        if not ticks % 50:  spawn_ufo()         
       
        mw.blit(fon, (0, 0))
       
        all_sprite.update()

        if pg.sprite.spritecollide(hero, ufos, False):
            hero.health -= 1
            if hero.health <= 0:
                game = False

        collides = pg.sprite.groupcollide(bullets, ufos, True, True)
        for bullet, ufo in collides.items():
            Boom(ufo[0].rect.center, boom_sprites, booms)
            # hero.points += 1
            boom_sound.play()

        all_sprite.draw(mw)  
        set_text(f"Пропущено: {ufo_missed}", 650, 20)
        # set_text(f"Здоровье: {hero.health}", hero.rect.x, hero.rect.y)

        if ufo_missed > 5:
            game = False

    else:
        mw.blit(fon_go, (0, 0))


    
    pg.display.update()
    clock.tick(60)
    ticks += 1
    
