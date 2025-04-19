import pygame as pg
#from sprites import Star
from random import randint
from config import *
#from math import sqrt
from sprites import Alien

def set_text(scr, text, size = 10, pos = (0,0), color = (255,255,55)):
    font = pg.font.Font(None, size)
    text_pic = font.render(str(text), True, color)
    scr.blit(text_pic,pos)




def alien_add(aliens, speed, ufo_sprites):      
    x = randint(-200, WINDOWS_SIZE[0]+200) 
    y = -100
    # макс количество в конфиге ALIENS_LIMIT
    aliens.add(Alien('111', x, y, 100, 90, speed, ufo_sprites))
    return aliens

def game_over(scr):
    background = pg.transform.scale(pg.image.load('pic\\game_over.jpg'),(WINDOWS_SIZE))
    scr.blit(background,(0,0))

def sprites_load(folder:str, file_name:str, size:tuple, colorkey:tuple = None):    
    sprites = []
    load = True
    num = 1
    while load:
        try:
            spr = pg.transform.scale(pg.image.load(f'{folder}\\{file_name}{num}.png'),size)
            if colorkey: spr.set_colorkey((0,0,0))
            sprites.append(spr)
            num += 1
        except:
            load = False
    return sprites

if __name__ == '__main__':
    pass