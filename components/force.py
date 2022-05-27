from vars import BEAM_LEFT, BEAM_RIGHT, BEAM_TOP,BLACK

from components import *

class Force(Component):
    SHOW_LEN = 75
    def __init__(self,x,mag,angle,beam_length):
        self.x = x
        self.angle_in_degrees = angle

        self.mag = mag
        self.angle = math.radians(angle)

        self.calc_fx_fy()
        self.set_location_according_to_beam_length(beam_length)
        self.setup_demo()
    
    def setup_demo(self):
        self.demo_surface = pygame.Surface.copy(Demo.DEMO_SURFACE)
        rect = self.demo_surface.get_rect()
        desy = rect.top + 40
        length = self.SHOW_LEN * 0.5
        posx = rect.centerx - math.cos(self.angle)*length / 2
        posy = desy + math.sin(self.angle)*length /2
        endpos = (posx+length*math.cos(self.angle),posy-length*math.sin(self.angle))
        draw_arrow(self.demo_surface,BLACK,(posx, posy),endpos,2)
        print_demo_data(self.demo_surface, ("Force", f"x = {self.x}",f"Mag = {self.mag}",f"Ang = {self.angle_in_degrees}"), rect, Demo.OUTLINE_WIDTH, Demo.OUTLINE_HEIGHT)

    def draw_demo(self, surface, point):
        surface.blit(self.demo_surface, point)

    def calc_fx_fy(self):
        self.fx = self.mag*math.cos(self.angle)
        self.fy = self.mag*math.sin(self.angle)

    def set_location_according_to_beam_length(self,beam_length):
        self.mappedx = map_value(self.x,0,beam_length,BEAM_LEFT,BEAM_RIGHT)
        self.startpos = (self.mappedx,BEAM_TOP)
        self.endpos = (self.startpos[0]+self.SHOW_LEN*math.cos(self.angle),self.startpos[1]-self.SHOW_LEN*math.sin(self.angle))

    def draw(self,win):
        draw_arrow(win,BLACK,self.startpos,self.endpos,2)

    def __repr__(self):
        return "Force, Location: " + str(self.x) + ", Magnitude: " + str(self.mag) + ", Angle: " + str(self.angle)

    def __eq__(self,other):
        return isinstance(other, Force) and self.x == other.x and self.mag==other.mag and self.angle == other.angle


