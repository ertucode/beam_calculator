from vars import beam_left, beam_right, beam_mid, beam_length, \
    beam_height, beam_below,beam_y,WIDTH,HEIGHT,BLACK,forcelen

from __init__ import *

class Force(Component):
    SHOW_LEN = 75
    def __init__(self,x,mag,angle):
        self.x = x

        self.set_location_according_to_beam_length(beam_length)
        self.mag = mag
        self.angle = math.radians(angle)
        self.calc_fx_fy()

    def calc_fx_fy(self):
        self.fx = self.mag*math.cos(self.angle)
        self.fy = self.mag*math.sin(self.angle)

    def set_location_according_to_beam_length(self,beam_length):
        self.mappedx = map_value(self.x,0,beam_length,beam_left,beam_right)
        self.startpos = (self.mappedx,beam_y)
        self.endpos = (self.startpos[0]+self.SHOW_LEN*math.cos(self.angle),self.startpos[1]-self.SHOW_LEN*math.sin(self.angle))

    def draw(self,win,beam_length):
        draw_arrow(win,BLACK,self.startpos,self.endpos,2)

    def __repr__(self):
        return "Force, Location: " + str(self.x) + ", Magnitude: " + str(self.mag) + ", Angle: " + str(self.angle)

    def __eq__(self,other):
        return isinstance(other, Force) and self.x == other.x and self.mag==other.mag and self.angle == other.angle

class DemoForce(Demo):
    SHOW_LEN = 37.5
    def __init__(self,demox,demoy,angle,datas):
        angle = math.radians(angle)
        self.startpos = (demox,demoy)
        self.endpos = (self.startpos[0]+self.SHOW_LEN*math.cos(angle),self.startpos[1]-self.SHOW_LEN*math.sin(angle))
        
        self.datas = datas

    def draw(self,win,beam_length):
        draw_arrow(win,BLACK,self.startpos,self.endpos,2)

    def __repr__(self):
        return "demo-force: " + self.datas

    def __eq__(self,other):
        return isinstance(other, DemoForce) and self.datas == other.datas

