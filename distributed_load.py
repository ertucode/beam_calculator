import myfuncs
import pygame
from math import ceil
from vars import beam_left, beam_right, beam_mid, beam_length, \
    beam_height, beam_below,beam_y,WIDTH,HEIGHT,BLACK,forcelen,distload_h

def draw_dist_load(win,COLOR,x,y,width,height,dir,startmag,endmag,maxmag):
    space = 15
    count = ceil(width/space)
    space = width/count
    hstart = myfuncs.map_value(startmag,0,maxmag,0,height)
    hend = myfuncs.map_value(endmag,0,maxmag,0,height)
    hinc = (hend-hstart) / count
    if dir == "up":
        mult = 1
    elif dir == "down":
        mult = -1
    for i in range(count+1):
        myfuncs.draw_arrow(win,COLOR,(x+i*space,y+mult*(hstart+i*hinc)),(x+i*space,y),2)
    pygame.draw.line(win,COLOR,(x,y+mult*hstart),(x+width,y+mult*hend),2)


class Distload:
    def __init__(self,startx,endx,startmag,endmag,dir,demo=False,demoy=0):
        self.demo = demo
        self.startx = startx
        self.endx = endx
        self.startmag = startmag
        self.endmag = endmag
        self.h = 50
        if not self.demo:
            self.mappedstartx = myfuncs.map_value(startx,0,beam_length,beam_left,beam_right)
            self.mappedendx = myfuncs.map_value(endx,0,beam_length,beam_left,beam_right)
            self.width = self.mappedendx - self.mappedstartx
            self.CalcEquivalent()
        else:
            self.width = self.endx - self.startx
            self.demoy = demoy
            self. h *= 0.5
        

        self.dir = dir
        self.type = "distload"
        

    def UpdateBeamLength(self,beam_length):
        self.mappedstartx = myfuncs.map_value(self.startx,0,beam_length,beam_left,beam_right)
        self.mappedendx = myfuncs.map_value(self.endx,0,beam_length,beam_left,beam_right)
        self.width = self.mappedendx - self.mappedstartx

    def draw(self,win,beam_length):
        maxmag = max(self.startmag,self.endmag)
        if not self.demo:
            self.UpdateBeamLength(beam_length)
            draw_dist_load(win,BLACK,self.mappedstartx,beam_y,self.width,self.h,self.dir,self.startmag,self.endmag,maxmag)
        if self.demo:
            draw_dist_load(win,BLACK,self.startx,self.demoy,self.width,self.h,self.dir,self.startmag,self.endmag,maxmag)
        
    
    def CalcEquivalent(self):
        width = self.endx-self.startx
        if self.startmag >= self.endmag:
            MaxLoad = self.startmag
            MinLoad = self.endmag
            TriLoc = self.startx + width / 3
        else:
            MaxLoad = self.endmag
            MinLoad = self.startmag
            TriLoc = self.endx - width / 3       
        RectForce = MinLoad * width
        TriForce = (MaxLoad - MinLoad) * width / 2
        self.EqForce = RectForce + TriForce
        self.EqLoc = (RectForce*width/2+TriForce*TriLoc)/self.EqForce

    def __eq__(self,other):
        return self.startx==other.startx and self.endx==other.endx and self.startmag==other.startmag and self.endmag==other.endmag and self.dir==other.dir
    
    def __str__(self):
        return f"DistributedLoad, Start/End: {self.startx}/{self.endx}, Magnitudes: {self.startmag},{self.endmag}, Direction: {self.dir}"

    def __repr__(self):
        return self.__str__()