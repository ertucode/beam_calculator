
from components import *

from variables import BEAM_LEFT, BEAM_RIGHT, BEAM_TOP

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

    CONSTRUCT_QUESTIONS = ("Direction[up/down]:","Starting Location[m]: ","Starting Magnitude[N/m]: ","Ending Location[m]: ","Ending Magnitude[N/m]: ")
    def __init__(self,startx,endx,startmag,endmag,direction,beam_length):
        self.startx = startx
        self.endx = endx

        self.startmag = startmag
        self.endmag = endmag
        self.maxmag = max(self.startmag,self.endmag)
        
        self.set_location_according_to_beam_length(beam_length)
        self.calculate_equivalent_quantities()

        self.direction = direction
    
    def setup_demo(self):
        self.demo_surface = pygame.Surface.copy(DemoWithInfo.DEMO_SURFACE)
        rect = self.demo_surface.get_rect()
        XOFF = 10
        if self.direction == "down":
            y = rect.top + self.HEIGHT
        elif self.direction == "up":
            y = rect.top + self.HEIGHT * 0.5
        startx = rect.left + XOFF
        width = rect.right - 2 * XOFF
        draw_dist_load(self.demo_surface,"black",startx,y,width,self.HEIGHT * 0.5,self.direction,self.startmag,self.endmag,self.maxmag)
        print_demo_data(self.demo_surface, ("Distributed L.", f"Dir = {self.direction}",f"x_i = {self.startx}",f"x_f = {self.endx}",f"Mag_i = {self.startmag}",f"Mag_f = {self.endmag}"),
                 rect, DemoWithInfo.OUTLINE_WIDTH, DemoWithInfo.OUTLINE_HEIGHT)


    def set_location_according_to_beam_length(self,beam_length):
        self.mappedstartx = map_value(self.startx,0,beam_length,BEAM_LEFT,BEAM_RIGHT)
        self.mappedendx = map_value(self.endx,0,beam_length,BEAM_LEFT,BEAM_RIGHT)
        self.width = self.mappedendx - self.mappedstartx

    def draw(self,win):
        draw_dist_load(win,"black",self.mappedstartx,BEAM_TOP,self.width,self.HEIGHT,self.direction,self.startmag,self.endmag,self.maxmag)
    
    def calculate_equivalent_quantities(self):
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
        return isinstance(other, Distload) and self.startx==other.startx and self.endx==other.endx and self.startmag==other.startmag and self.endmag==other.endmag and self.direction==other.direction

    def __repr__(self):
        return f"DistributedLoad, Start/End: {self.startx}/{self.endx}, Magnitudes: {self.startmag},{self.endmag}, Direction: {self.direction}"

    @classmethod
    def create_demo(cls):
        return cls(0, 15, 10, 15, "down", 25)

    def duplicate(self, beam_length):
        """Needed since you can't deepcopy pygame.Surface objects"""
        return type(self)(self.startx,self.endx,self.startmag,self.endmag,self.direction, beam_length)