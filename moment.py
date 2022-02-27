from vars import beam_left, beam_right, beam_mid, beam_length, \
    beam_height, beam_below,beam_y,WIDTH,HEIGHT,BLACK,forcelen,momentw

import pygame
import math
import myfuncs

def draw_moment(win,COLOR,posx,posy,width,dir,th):
    if dir == "CCW":
        pygame.draw.arc(win,COLOR,(posx-width/2,posy,width,width),math.pi/2,2*math.pi,th)
        #pygame.draw.circle(win,BLACK,(posx,posy+width/2),width/2,2)
        myfuncs.draw_arrow_tip(win,COLOR,posx+1/2*width-width/20,posy+2/4*width-width/8,0,8)
    if dir == "CW":
        pygame.draw.arc(win,COLOR,(posx-width/2,posy,width,width),math.pi/2,2*math.pi,th)
        myfuncs.draw_arrow_tip(win,COLOR,posx+width/10,posy-width/16,math.pi/2.75,8)

class Moment:
    def __init__(self,x,mag):
        self.x = x
        self.mappedx = myfuncs.map_value(x,0,beam_length,beam_left,beam_right)
        self.mag = mag
        self.set_dir()
        
    def set_dir(self):
        if self.mag>0:
            self.dir = "CCW"
        elif self.mag < 0:
            self.dir = "CW"

    def draw(self,win):
        draw_moment(win,BLACK,self.mappedx,beam_mid - 6* beam_height,momentw,self.dir,2)
        