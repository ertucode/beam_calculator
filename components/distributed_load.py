
from __init__ import *

from vars import beam_left, beam_right, beam_mid, beam_length, \
    beam_height, beam_below,beam_y,WIDTH,HEIGHT,BLACK,forcelen,distload_h

def draw_dist_load(win,COLOR,x,y,width,height,dir,startmag,endmag,maxmag):
    space = 15
    count = math.ceil(width/space)
    space = width/count
    hstart = map_value(startmag,0,maxmag,0,height)
    hend = map_value(endmag,0,maxmag,0,height)
    hinc = (hend-hstart) / count
    if dir == "up":
        mult = 1
    elif dir == "down":
        mult = -1
    for i in range(count+1):
        draw_arrow(win,COLOR,(x+i*space,y+mult*(hstart+i*hinc)),(x+i*space,y),2)
    pygame.draw.line(win,COLOR,(x,y+mult*hstart),(x+width,y+mult*hend),2)


class Distload(Component):
    HEIGHT = 50
    def __init__(self,startx,endx,startmag,endmag,direction):
        self.startx = startx
        self.endx = endx

        self.startmag = startmag
        self.endmag = endmag
        self.maxmag = max(self.startmag,self.endmag)
        
        self.set_location_according_to_beam_length(beam_length)
        self.calculate_equivalent_quantiies()

        self.direction = direction
        self.type = "distload"

    def set_location_according_to_beam_length(self,beam_length):
        self.mappedstartx = map_value(self.startx,0,beam_length,beam_left,beam_right)
        self.mappedendx = map_value(self.endx,0,beam_length,beam_left,beam_right)
        self.width = self.mappedendx - self.mappedstartx

    def draw(self,win,beam_length):
        draw_dist_load(win,BLACK,self.mappedstartx,beam_y,self.width,self.HEIGHT,self.direction,self.startmag,self.endmag,self.maxmag)
        
    
    def calculate_equivalent_quantiies(self):
        width = self.endx-self.startx
        if self.startmag >= self.endmag:
            MaxLoad = self.startmag
            MinLoad = self.endmag
            TriLoc = width / 3
        else:
            MaxLoad = self.endmag
            MinLoad = self.startmag
            TriLoc = 2 * width / 3       
        RectForce = MinLoad * width
        TriForce = (MaxLoad - MinLoad) * width / 2
        self.eq_force = RectForce + TriForce
        self.eq_loc = (RectForce*width/2+TriForce*TriLoc)/self.eq_force
        self.eq_loc = self.startx + self.eq_loc
        
    def __eq__(self,other):
        return self.startx==other.startx and self.endx==other.endx and self.startmag==other.startmag and self.endmag==other.endmag and self.direction==other.direction

    def __repr__(self):
        return f"DistributedLoad, Start/End: {self.startx}/{self.endx}, Magnitudes: {self.startmag},{self.endmag}, Direction: {self.direction}"

class DistloadDemo(Demo):
    HEIGHT = 25
    def __init__(self, startx, endx, startmag, endmag, locy, direction, datas):
        self.startx = startx
        self.endx = endx
        self.startmag = startmag
        self.endmag = endmag
        self.maxmag = max(self.startmag, self.endmag)
        
        self.width = self.endx - self.startx
        self.showy = locy

        self.direction = direction

    def draw(self,win,beam_length):
        draw_dist_load(win,BLACK,self.startx,self.showy,self.width,self.HEIGHT,self.direction,self.startmag,self.endmag,self.maxmag)

    def __repr__(self):
        return "demo-distload: " + self.datas
