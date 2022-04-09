import pygame
import math
import myfuncs
from vars import beam_left, beam_right, beam_mid, beam_length, \
    beam_height, beam_below,beam_y,WIDTH,HEIGHT,BLACK,forcelen

class Force:
    def __init__(self,x,mag,angle,demo=False,demox=None,demoy=None):
        self.x = x
        self.demo = demo
        self.demox = demox
        self.demoy = demoy
        self.deg = angle
        if demo:
            self.mappedx = self.demox
            self.forcelen = 75/2
        else:
            self.mappedx = myfuncs.map_value(x,0,beam_length,beam_left,beam_right)
            self.forcelen= 75
        self.mag = mag
        self.angle = math.radians(angle)
        self.calc_fx_fy()
        self.type = "force"

    def calc_fx_fy(self):
        self.fx = self.mag*math.cos(self.angle)
        self.fy = self.mag*math.sin(self.angle)

    def UpdateBeamLength(self,beam_length):
        self.mappedx = myfuncs.map_value(self.x,0,beam_length,beam_left,beam_right)

    def draw(self,win,beam_length):
        if not self.demo:
            self.UpdateBeamLength(beam_length)
            startpos = (self.mappedx,beam_y)
            endpos = (startpos[0]+self.forcelen*math.cos(self.angle),startpos[1]-self.forcelen*math.sin(self.angle))
        else:
            startpos = (self.demox,self.demoy)
            self.forcelen = self.forcelen
            endpos = (startpos[0]+self.forcelen*math.cos(self.angle),startpos[1]-self.forcelen*math.sin(self.angle))
        myfuncs.draw_arrow(win,BLACK,startpos,endpos,2)

    def __str__(self):
        return "Force, Location: " + str(self.x) + ", Magnitude: " + str(self.mag) + ", Angle: " + str(self.angle)

    def __repr__(self):
        return self.__str__()

    def __eq__(self,other):
        return self.x == other.x and self.mag==other.mag and self.angle == other.angle