import pygame
import math
import myfuncs
from vars import beam_left, beam_right, beam_mid, beam_length, \
    beam_height, beam_below,beam_y,WIDTH,HEIGHT,BLACK,forcelen

class Force:
    def __init__(self,x,mag,angle):
        self.x = x
        self.mappedx = myfuncs.map_value(x,0,beam_length,beam_left,beam_right)
        self.mag = mag
        self.angle = math.radians(angle)
        self.calc_fx_fy()
        self.type = "force"



    def calc_fx_fy(self):
        self.fx = self.mag*math.cos(self.angle)
        self.fy = self.mag*math.sin(self.angle)

    def draw(self,win):
        startpos = (self.mappedx,beam_y)
        endpos = (startpos[0]+forcelen*math.cos(self.angle),startpos[1]-forcelen*math.sin(self.angle))
        myfuncs.draw_arrow(win,BLACK,startpos,endpos,2)

    def __str__(self):
        return "Force, Location: " + str(self.x) + ", Magnitude: " + str(self.mag) + ", Angle: " + str(self.angle)

    def __repr__(self):
        return self.__str__()