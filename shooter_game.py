from pygame import *
from random import randint
init()
'''Необходимые классы'''

#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    bullet_timer = 0
    bullet_timer_max = 20
    life = 3
    points = 0
    dif = 1
    ufo_count = 0

    def update(self):
        self.bullet_timer -=1
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 50:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 70:
            self.rect.y += self.speed
        if keys[K_SPACE]:
           self.fire()

    def fire(self):
        if self.bullet_timer<=0:
            bullet = Bullet('fire1.png',
                            self.rect.centerx-5, self.rect.y-10,
                            5,10,20)
            bullets.add(bullet)
            kick.play()
            self.bullet_timer = self.bullet_timer_max

class Bullet(GameSprite):    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -20:
            self.kill()
        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed



def set_text(scr, text, size = 10, 
                pos = (0,0), 
                color = (255,255,55)):
    font1 = font.Font(None, size)
    text_pic = font1.render(str(text), True, color)
    scr.blit(text_pic, pos)



#Игровая сцена:
win_width = 500
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption("Космос-стар")

background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

#Персонажи игры:
player = Player('rocket.png', win_width/2-25, win_height-80, 5, 50,70)



game = True
finish = False
win = False
clock = time.Clock()
FPS = 60
ufo_for_dif = 5


#bullets = []
ufos = sprite.Group()
bullets = sprite.Group()

enemy_timer = 120
ticks = 0

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
kick = mixer.Sound('fire.ogg')




while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish != True:
        if ticks%enemy_timer == 0:
            ufo = Enemy('ufo.png', randint(0, win_width-35), -70,
                            1+player.dif, 70, 50)
            ufos.add(ufo)
            player.ufo_count += 1
            



        window.blit(background,(0, 0))
        
        if sprite.groupcollide(bullets, ufos, True, True):
            player.points += 1

        if sprite.spritecollide(player, ufos, True):
            player.life -= 1
        
        if player.life == 0:
            finish = True

        player.update()
        player.reset()

        ufos.update()
        ufos.draw(window)

        bullets.update()
        bullets.draw(window)

        if player.ufo_count % ufo_for_dif == 0:
            player.dif += 1
            player.ufo_count = 1


        set_text(window, "Очки - " + str(player.points), 30, (5,5), (255,255,255)) 
        set_text(window, "Сложность - " + str(player.dif), 30, (310,5), (255,255,255))
        set_text(window, "враги - " + str(player.ufo_count), 30, (310,50), (255,255,255)) 
        
    else:
        if win:
            go = GameSprite('win.jpg', 0,0, 0, 700, 500)
            go.reset()
        else:rirururu
            # если конец игры
            go = GameSprite('gameover.jpg', 0,0, 0, 700, 500)
            go.reset()

    display.update()
    clock.tick(FPS)
    ticks += 1
