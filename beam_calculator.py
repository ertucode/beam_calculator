import pygame
import math
from force import Force
from support import Support
from distributed_load import Distload
from moment import Moment
import myfuncs
from vars import beam_left, beam_right, beam_mid, beam_length, beam_height, beam_below,beam_y,WIDTH,HEIGHT,BLACK,WHITE


pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beam Calculator")


myforce = Force(7,100,120)
mysup = Support("pinned",5)
mysup2 = Support("roller",12)
mysup3 = Support("fixed",side = "right")
supports = [mysup,mysup2,mysup3]
myload = Distload(2,10,10,20,"up")
mymoment = Moment(10,-30)
objects = [myload,mymoment,myforce] + supports

def draw(win,objects):
    win.fill(WHITE)
    myfuncs.draw_at_center(win,(173,216,230),beam_mid,beam_y,beam_right-beam_left,beam_height,0)

    for object in objects:
        object.draw(win)

    

    pygame.display.update()


run = True

clock = pygame.time.Clock()

while run:
    FPS = 60
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    
    draw(win,objects)
pygame.quit()


