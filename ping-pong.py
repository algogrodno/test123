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
class Rocket(GameSprite):
    bullet_timer = 0
    bullet_timer_max = 20
    life = 3
    points = 0
    dif = 1
    ufo_count = 0

    def update_l(self):  
        keys = key.get_pressed()        
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 70:
            self.rect.y += self.speed
        
    def update_r(self):  
        keys = key.get_pressed()        
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 70:
            self.rect.y += self.speed


#Игровая сцена:
win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption("Космос-стар")

background = transform.scale(
    image.load(r"C:\Users\User\AppData\Local\Programs\Algoritmika\vscode\data\extensions\algoritmika.algopython-20230320.193254.0\data\student\2425117\184431\p_fon3.jpg"), 
    (win_width, win_height))

#Персонажи игры:
#player = Rocket('rocket.png', win_width/2-25, win_height-80, 5, 50,70)



game = True
finish = False
win = False
clock = time.Clock()
FPS = 60
ufo_for_dif = 5


# #bullets = []
# ufos = sprite.Group()
# bullets = sprite.Group()

enemy_timer = 120
ticks = 0

#музыка
# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()
# kick = mixer.Sound('fire.ogg')




while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background,(0,0))
    display.update()
    clock.tick(FPS)
    ticks += 1
