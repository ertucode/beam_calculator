from components import * 
from variables import BEAM_LEFT, BEAM_RIGHT, BEAM_BOTTOM, BEAM_TOP


def draw_circles(win,COLOR,x,y,width,radius,th):
    """Draw circles along the width"""
    count = math.floor(width / radius /2)
    center1x = x + radius
    center1y = y + radius
    for i in range(count):
        pygame.draw.circle(win,COLOR,(center1x+i*2.15*radius,center1y),radius,th)

class Support(Component):
    # Constants for support 
    TIRTIK_HEIGHT = 5
    TIRTIK_COUNT = 6
    @staticmethod
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

class FixedSupport(Support):
    # Width and height of a fixed support
    DRAW_WIDTH = 10
    DRAW_HEIGHT = 100
    # Questions to ask to be able to construct 
    CONSTRUCT_QUESTIONS = ("Location[left/right]: ",)
    def __init__(self,side,beam_length):
        self.side = side
        
        self.set_location_according_to_beam_length(beam_length)

        self.reaction_force = "Not Calculated"
        self.reaction_moment = "Not Calculated"
    
    def setup_demo(self):
        """Setting up a demo surface"""
        draw_width = self.DRAW_WIDTH * 0.5
        draw_height = self.DRAW_HEIGHT * 0.5

        self.demo_surface = pygame.Surface.copy(demo_with_info.surface)
        rect = self.demo_surface.get_rect()
        FixedSupport.draw_fixed_sup(self.demo_surface, "black", rect.centerx, rect.centery - demo_with_info.height * 0.25 - 30, self.side, draw_width, draw_height, 2)   
        self.print_demo_data(("Fixed", f"{self.side}"), rect)

    def set_location_according_to_beam_length(self,beam_length):
        if self.side == "left":
            self.x = 0
            self.mappedx = BEAM_LEFT
        elif self.side == "right":
            self.x = beam_length
            self.mappedx = BEAM_RIGHT

    def draw(self,win):
        if self.side == "left":
            self.draw_fixed_sup(win,"black",self.mappedx-self.DRAW_WIDTH,BEAM_TOP - self.DRAW_HEIGHT/2,self.side,self.DRAW_WIDTH,self.DRAW_HEIGHT,2)
        elif self.side == "right":
            self.draw_fixed_sup(win,"black",self.mappedx            ,BEAM_TOP - self.DRAW_HEIGHT/2,self.side,self.DRAW_WIDTH,self.DRAW_HEIGHT,2)
        
    def duplicate(self, beam_length):
        """Needed since you can't deepcopy pygame.Surface objects"""
        dup = type(self)(self.side, beam_length)
        dup.reaction_force, dup.reaction_moment = self.reaction_force, self.reaction_moment
        return dup


    @staticmethod
    def draw_fixed_sup(win,COLOR,x,y,side,width,height,th):
        pygame.draw.rect(win,COLOR,(x,y,width,height),th)
        trw = width/3
        if side == "left":
            Support.draw_tırtık(win,COLOR,"left",x-trw,y,trw,height,15,2)
        elif side == "right":
            Support.draw_tırtık(win,COLOR,"left",x+width,y,trw,height,15,2)

    def __repr__(self):
        return f"|Support Type: fixed, Side: {self.side}, Reaction Force: {self.reaction_force}, Reaction Moment: {self.reaction_moment}|"

    def __eq__(self,other):
        return isinstance(other, FixedSupport) and self.side==other.side

    @classmethod
    def create_demo(cls):
        return cls("left", 10)

class PointSupport(Support):
    SIZE = 35
    # Questions to ask to be able to construct 
    CONSTRUCT_QUESTIONS = ("Location[m]: ",)
    def __init__(self, x):
        self.x = x
        self.reaction_force = "Not Calculated"

    def draw(self, win):
        pygame.draw.lines(win,"black",True,self.points,2)

    @classmethod
    def create_demo(cls):
        return cls(0, 10)

    def duplicate(self, beam_length):
        """Needed since you can't deepcopy pygame.Surface objects"""
        dup = type(self)(self.x, beam_length)
        dup.reaction_force = self.reaction_force
        return dup

class PinnedSupport(PointSupport):
    def __init__(self, x,beam_length):
        super().__init__(x)
        self.set_location_according_to_beam_length(beam_length)
    
    def setup_demo(self):
        """Setting up a demo surface"""
        self.demo_surface = pygame.Surface.copy(demo_with_info.surface)
        rect = self.demo_surface.get_rect()
        
        x, y, width, height = rect.centerx, rect.top + self.SIZE - 20, self.SIZE, self.SIZE
        points = ((x,y),(x - width /2,y + height),(x + width /2,y + height))
        pygame.draw.lines(self.demo_surface, "black", True, points, 2)
        self.draw_tırtık(self.demo_surface,"black","down",*points[1],self.SIZE,self.TIRTIK_HEIGHT,self.TIRTIK_COUNT,2)
        self.print_demo_data(("Pinned", f"{self.x} m"), rect)


    def set_location_according_to_beam_length(self, beam_length):
        self.mappedx = map_value(self.x,0,beam_length,BEAM_LEFT,BEAM_RIGHT)
        x, y, width, height = self.mappedx, BEAM_BOTTOM, self.SIZE, self.SIZE
        self.points = ((x,y),(x - width /2,y + height),(x + width /2,y + height))

    def draw(self, win):
        super().draw(win)
        self.draw_tırtık(win,"black","down",*self.points[1],self.SIZE,self.TIRTIK_HEIGHT,self.TIRTIK_COUNT,2)

    def __repr__(self):
        return f"|Support Type: pinned, Location: {self.x}, Reaction Force: {self.reaction_force}|"

    def __eq__(self, other):
        return isinstance(other, FixedSupport) and self.x == other.x

class RollerSupport(PointSupport):
    def __init__(self, x,beam_length):
        super().__init__(x)
        self.set_location_according_to_beam_length(beam_length)
    
    def setup_demo(self):
        """Setting up a demo surface"""
        self.demo_surface = pygame.Surface.copy(demo_with_info.surface)
        rect = self.demo_surface.get_rect()
        
        x, y, width, height = rect.centerx, rect.top + self.SIZE - 20, self.SIZE, self.SIZE * 0.8
        radius = 0.1 * self.SIZE
        points = ((x,y),(x - width /2,y + height),(x + width /2,y + height))
        tırtık_locy = y+height+1.9*radius
        pygame.draw.lines(self.demo_surface, "black", True, points, 2)
        draw_circles(self.demo_surface,"black",*points[1],self.SIZE,radius,2)
        self.draw_tırtık(self.demo_surface,"black","down",points[1][0],tırtık_locy,self.SIZE,self.TIRTIK_HEIGHT,self.TIRTIK_COUNT,2)
        self.print_demo_data(("Roller", f"{self.x} m"), rect)     
    
    def set_location_according_to_beam_length(self, beam_length):
        self.mappedx = map_value(self.x,0,beam_length,BEAM_LEFT,BEAM_RIGHT)

        # Setting up draw variables
        x, y, width, height = self.mappedx, BEAM_BOTTOM, self.SIZE, self.SIZE * 0.8
        self.radius = 0.1 * self.SIZE
        self.points = ((x,y),(x - width /2,y + height),(x + width /2,y + height))
        self.tırtık_locy = y+height+1.9*self.radius

    def draw(self, win):
        super().draw(win)
        draw_circles(win,"black",*self.points[1],self.SIZE,self.radius,2)
        self.draw_tırtık(win,"black","down",self.points[1][0],self.tırtık_locy,self.SIZE,self.TIRTIK_HEIGHT,self.TIRTIK_COUNT,2)

    def __repr__(self):
        return f"|Support Type: roller, Location: {self.x}, Reaction Force: {self.reaction_force}|"

    def __eq__(self, other):
        return isinstance(other, RollerSupport) and self.x == other.x




