from variables import BEAM_LEFT, BEAM_RIGHT, BEAM_HEIGHT, BEAM_TOP

from components import *

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
    POSY = BEAM_TOP - 6* BEAM_HEIGHT
    SIZE = 40

    CONSTRUCT_QUESTIONS = ("Location[m]: ","Magnitude[Nm][""+"" for CCW ""-""CW]: ")
    def __init__(self, x, mag, beam_length):
        self.x = x
        self.mag = mag
        self.set_dir()

        self.set_location_according_to_beam_length(beam_length)
    
    def setup_demo(self):
        self.demo_surface = pygame.Surface.copy(DemoWithInfo.DEMO_SURFACE)
        rect = self.demo_surface.get_rect()
        
        draw_moment(self.demo_surface,"black",rect.centerx,rect.top + self.SIZE,self.SIZE,self.direction,2)
        print_demo_data(self.demo_surface, ("Moment", f"x = {self.x}",f"Mag = {self.mag}",f"Dir = {self.direction}"), rect, DemoWithInfo.OUTLINE_WIDTH, DemoWithInfo.OUTLINE_HEIGHT) 

    def set_dir(self):
        if self.mag>0:
            self.direction = "CCW"
        elif self.mag < 0:
            self.direction = "CW"
            
    def set_location_according_to_beam_length(self,beam_length):
        self.mappedx = map_value(self.x,0,beam_length,BEAM_LEFT,BEAM_RIGHT)

    def draw(self,win):
        draw_moment(win,"black",self.mappedx,self.POSY,self.SIZE,self.direction,2)

    def __eq__(self,other):
        return isinstance(other, Moment) and self.x == other.x and self.mag==other.mag

    def __repr__(self):
        return "Moment, Location:"+str(self.x)+", Magnitude:"+str(self.mag)

    @classmethod
    def create_demo(cls):
        return cls(0, 15, 10)

    def duplicate(self, beam_length):
        """Needed since you can't deepcopy pygame.Surface objects"""
        return type(self)(self.x, self.mag, beam_length)
