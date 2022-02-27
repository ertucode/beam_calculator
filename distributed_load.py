import myfuncs
import pygame
from vars import beam_left, beam_right, beam_mid, beam_length, \
    beam_height, beam_below,beam_y,WIDTH,HEIGHT,BLACK,forcelen

def draw_dist_load(win,COLOR,x,y,width,height,dir):
    space = 15
    count = round(width/space)
    space = width/count
    if dir == "up":
        mult = 1
    elif dir == "down":
        mult = -1
    for i in range(count+1):
        myfuncs.draw_arrow(win,COLOR,(x+i*space,y+mult*height),(x+i*space,y),2)
    pygame.draw.line(win,COLOR,(x,y+mult*height),(x+width,y+mult*height),2)


class Distload:
    def __init__(self,startx,endx,mag,dir):
        self.startx = startx
        self.mappedstartx = myfuncs.map_value(startx,0,beam_length,beam_left,beam_right)
        self.endx = endx
        self.mappedendx = myfuncs.map_value(endx,0,beam_length,beam_left,beam_right)
        self.width = self.mappedendx - self.mappedstartx
        self.mag = mag
        self.dir = dir

    def draw(self,win):
        draw_dist_load(win,BLACK,self.mappedstartx,beam_mid,self.width,beam_height*2,self.dir)