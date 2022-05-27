from vars import beam_left, beam_right, beam_mid, beam_length, \
    beam_height, beam_below,beam_y,WIDTH,HEIGHT,BLACK,forcelen,momentw

from __init__ import *

def draw_arrow_tip(win,COLOR,x,y,angle,size):
    tip1_ang = angle + 2*math.pi/6
    end1 = (x+math.cos(tip1_ang)*size,y+math.sin(tip1_ang)*size)
    tip2_ang = angle + 4*math.pi/6
    end2 = (x+math.cos(tip2_ang)*size,y+math.sin(tip2_ang)*size)
    pygame.draw.line(win,COLOR,(x,y),end1,2)
    pygame.draw.line(win,COLOR,(x,y),end2,2)

def draw_moment(win,COLOR,posx,posy,width,dir,th):
    if dir == "CCW":
        pygame.draw.arc(win,COLOR,(posx-width/2,posy,width,width),math.pi/2,2*math.pi,th)
        draw_arrow_tip(win,COLOR,posx+1/2*width-width/20,posy+2/4*width-width/8,0,8)
    if dir == "CW":
        pygame.draw.arc(win,COLOR,(posx-width/2,posy,width,width),math.pi/2,2*math.pi,th)
        draw_arrow_tip(win,COLOR,posx+width/10,posy-width/16,math.pi/2.75,8)

class Moment(Component):
    POSY = beam_y - 6* beam_height
    SIZE = 40
    def __init__(self,x,mag):
        self.x = x
        self.mag = mag
        self.set_dir()

        self.set_location_according_to_beam_length(beam_length)
     
    def set_dir(self):
        if self.mag>0:
            self.direction = "CCW"
        elif self.mag < 0:
            self.direction = "CW"
            
    def set_location_according_to_beam_length(self,beam_length):
        self.mappedx = map_value(self.x,0,beam_length,beam_left,beam_right)

    def draw(self,win):
        draw_moment(win,BLACK,self.mappedx,self.POSY,self.SIZE,self.direction,2)

    def __eq__(self,other):
        return isinstance(other, Moment) and self.x == other.x and self.mag==other.mag

    def __repr__(self):
        return "Moment, Location:"+str(self.x)+", Magnitude:"+str(self.mag)

class DemoMoment(Demo):
    SIZE = 30
    def __init__(self,demox,demoy,direction,datas):
        self.datas = datas
        self.direction = direction
        
        self.showx = demox
        self.showy = demoy - DemoMoment.SIZE * 0.5

    def draw(self,win):
        draw_moment(win,BLACK,self.showx,self.showy,self.SIZE,self.direction,2)

    def __eq__(self,other):
        return isinstance(other, DemoMoment) and self.datas == other.datas
    
    def __repr__(self):
        return "demo-moment: " + self.datas