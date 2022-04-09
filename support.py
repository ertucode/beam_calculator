import pygame
import math
import myfuncs
from vars import beam_left, beam_right, beam_mid, beam_length,\
beam_height, beam_below,beam_y,WIDTH,HEIGHT,BLACK,tırtık_height,\
tırtık_count,sup_height, fixed_width, fixed_height


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

def draw_fixed_sup(win,COLOR,x,y,side,width,height,th):
    pygame.draw.rect(win,COLOR,(x,y,width,height),th)
    trw = width/3
    if side == "left" or side=="demo":
        draw_tırtık(win,COLOR,"left",x-trw,y,trw,height,15,2)
    elif side == "right":
        draw_tırtık(win,COLOR,"left",x+width,y,trw,height,15,2)
    


def draw_circles(win,COLOR,x,y,width,radius,th):
    count = math.floor(width / radius /2)
    center1x = x + radius
    center1y = y + radius
    for i in range(count):
        pygame.draw.circle(win,COLOR,(center1x+i*2.15*radius,center1y),radius,th)

def draw_tırtık(win,COLOR,side,x,y,width,height,count,th):
    if side=="down":
        inc = width / count
        firstx1 = x - inc
        firsty1 = y + height
        firstx2 = x
        firsty2 = y
        pygame.draw.line(win,COLOR,(x-inc,y),(x+width+inc,y),th)
        for i in range(0,count+1):
            offset = i*inc
            pygame.draw.line(win,COLOR,(firstx1+offset,firsty1),(firstx2+offset,firsty2),th)

    if side == "left" or side=="right":
        inc = height / count
        firstx1 = x
        firsty1 = y - inc
        firstx2 = x + width
        firsty2 = y        
        for i in range(1,count+1):
            offset = i*inc
            pygame.draw.line(win,COLOR,(firstx1,firsty1+offset),(firstx2,firsty2+offset),th)

class Support:
    def __init__(self,type,x=0,side =None,demo=False,demox = 1000,demoy= 0):
        self.side = side
        self.demo = demo
        self.x = x
        if not self.demo:
            
            self.mappedx = myfuncs.map_value(x,0,beam_length,beam_left,beam_right)
            self.set_fixed()
        else:
            self.mappedx = demox
            self.demoy = demoy
        self.type = type
        self.ReactionForce = "Not Calculated"


    def set_fixed(self):
        if self.side == "left":
            self.x = 0
            self.mappedx = beam_left
        elif self.side == "right":
            self.x = beam_length
            self.mappedx = beam_right
        self.ReactionMoment = "Not Calculated"

    def UpdateBeamLength(self,beam_length):
        if self.type == "fixed":
            if self.side == "right":
                self.x = beam_length

        self.mappedx = myfuncs.map_value(self.x,0,beam_length,beam_left,beam_right)

    def draw(self,win,beam_length):
        if not self.demo:
            self.UpdateBeamLength(beam_length)

        if self.type=="pinned":
            if self.demo:
                draw_pinned_sup(win,BLACK,self.mappedx,self.demoy,sup_height,sup_height,2)
            else:
                draw_pinned_sup(win,BLACK,self.mappedx,beam_below,sup_height,sup_height,2)
        elif self.type=="roller":
            if self.demo:
                draw_roller_sup(win,BLACK,self.mappedx,self.demoy,sup_height,sup_height,2)
            else:
                draw_roller_sup(win,BLACK,self.mappedx,beam_below,sup_height,sup_height,2)
        elif self.type == "fixed":
            if not self.demo:
                if self.side == "left":
                    draw_fixed_sup(win,BLACK,self.mappedx-fixed_width,beam_y - fixed_height/2,self.side,fixed_width,fixed_height,2)
                elif self.side == "right":
                    draw_fixed_sup(win,BLACK,self.mappedx            ,beam_y - fixed_height/2,self.side,fixed_width,fixed_height,2)
            else:
                draw_fixed_sup(win,BLACK,self.mappedx            ,self.demoy,self.side,fixed_width/2,fixed_height/2,2)
    
    def __eq__(self,other):
         return self.type==other.type and self.x==other.x and self.side==other.side

    def __str__(self):
        if self.type == "fixed":
            return f"|Support Type: {self.type}, Side: {self.side}, Reaction Force: {self.ReactionForce}, Reaction Moment: {self.ReactionMoment}|"
        else:
            return f"|Support Type: {self.type}, Location: {self.x}, Reaction Force: {self.ReactionForce}|"


    def __repr__(self):
        return self.__str__()