import pygame
import math
import myfuncs
from vars import beam_left, beam_right, beam_mid, beam_length,\
beam_height, beam_below,beam_y,WIDTH,HEIGHT,BLACK,tırtık_height,\
tırtık_count,sup_height


def draw_pinned_sup(win,COLOR,x,y,width,height,th,type="pinned"):
    points = ((x,y),(x - width /2,y + height),(x + width /2,y + height))
    pygame.draw.lines(win,COLOR,True,points,th)
    if type=="pinned":
        draw_tırtık(win,COLOR,"down",x - width / 2,y+height,width,tırtık_height,tırtık_count,th)

def draw_roller_sup(win,COLOR,x,y,width,height,th):
    height_pinned = height-height/5
    radius = (height-height_pinned)/2
    draw_pinned_sup(win,COLOR,x,y,width,height_pinned,th,type="roller")
    draw_circles(win,COLOR,x-width/2,y+height_pinned,width,radius,2)
    draw_tırtık(win,COLOR,"down",x-width/2,y+height_pinned+1.9*radius,width,tırtık_height,tırtık_count,2)


def draw_circles(win,COLOR,x,y,width,radius,th):
    count = math.floor(width / radius /2)
    center1x = x + radius
    center1y = y + radius
    for i in range(count):
        pygame.draw.circle(win,COLOR,(center1x+i*2.15*radius,center1y),radius,th)

def draw_tırtık(win,COLOR,side,x,y,width,height,count,th):
    inc = width / count
    if side=="down":
        firstx1 = x - inc
        firsty1 = y + height
        firstx2 = x
        firsty2 = y
        pygame.draw.line(win,COLOR,(x-inc,y),(x+width+inc,y),th)
        for i in range(0,count+1):
            offset = i*inc
            pygame.draw.line(win,COLOR,(firstx1+offset,firsty1),(firstx2+offset,firsty2),th)

class Support:
    def __init__(self,x,type):
        self.x = x
        self.mappedx = myfuncs.map_value(x,0,beam_length,beam_left,beam_right)
        self.type = type

    def draw(self,win):
        if self.type=="pinned":
            draw_pinned_sup(win,BLACK,self.mappedx,beam_below,(beam_right-beam_left)/10,sup_height,2)
        elif self.type=="roller":
            draw_roller_sup(win,BLACK,self.mappedx,beam_below,(beam_right-beam_left)/10,sup_height,2)