from __init__ import * 
from vars import beam_left, beam_right, beam_mid, beam_length,\
beam_height, beam_below,beam_y,WIDTH,HEIGHT,BLACK,tırtık_height,\
tırtık_count,sup_height, fixed_width, fixed_height
    

def draw_circles(win,COLOR,x,y,width,radius,th):
    count = math.floor(width / radius /2)
    center1x = x + radius
    center1y = y + radius
    for i in range(count):
        pygame.draw.circle(win,COLOR,(center1x+i*2.15*radius,center1y),radius,th)


class Support(Component):
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

class Demo:pass

class FixedSupport(Support):
    def __init__(self,side):
        self.side = side
        
        self.set_location_according_to_beam_length(beam_length)

        self.reaction_force = "Not Calculated"
        self.reaction_moment = "Not Calculated"

    def set_location_according_to_beam_length(self,beam_length):
        if self.side == "left":
            self.x = 0
            self.mappedx = beam_left
        elif self.side == "right":
            self.x = beam_length
            self.mappedx = beam_right

    def draw(self,win):
        if self.side == "left":
            self.draw_fixed_sup(win,BLACK,self.mappedx-fixed_width,beam_y - fixed_height/2,self.side,fixed_width,fixed_height,2)
        elif self.side == "right":
            self.draw_fixed_sup(win,BLACK,self.mappedx            ,beam_y - fixed_height/2,self.side,fixed_width,fixed_height,2)

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


class PointSupport(Support):
    def __init__(self, x):
        self.x = x
        self.ReactionForce = "Not Calculated"

    def draw(self, win):
        pygame.draw.lines(win,"black",True,self.points,2)


class PinnedSupport(PointSupport):
    def __init__(self, x):
        super.__init__(x)
        self.set_location_according_to_beam_length(beam_length)
    
    def set_location_according_to_beam_length(self, beam_length):
        self.mappedx = map_value(self.x,0,beam_length,beam_left,beam_right)
        x, y, width, height = self.mappedx, beam_below, sup_height, sup_height
        self.points = ((x,y),(x - width /2,y + height),(x + width /2,y + height))

    def draw(self, win):
        super().draw(win)
        self.draw_tırtık(win,"black","down",*self.points[1],sup_height,tırtık_height,tırtık_count,2)

    def __repr__(self):
        return f"|Support Type: pinned, Location: {self.x}, Reaction Force: {self.ReactionForce}|"

    def __eq__(self, other):
        return isinstance(other, FixedSupport) and self.x == other.x

class RollerSupport(PointSupport):
    def __init__(self, x):
        super.__init__(x)
        self.set_location_according_to_beam_length(beam_length)
    
    def set_location_according_to_beam_length(self, beam_length):
        self.mappedx = map_value(self.x,0,beam_length,beam_left,beam_right)

        # Setting up draw variables
        x, y, width, height = self.mappedx, beam_below, sup_height, sup_height * 0.8
        self.radius = 0.1 * sup_height
        self.points = ((x,y),(x - width /2,y + height),(x + width /2,y + height))
        self.tırtık_locy = y+height+1.9*self.radius

    def draw(self, win):
        super().draw(win)
        draw_circles(win,"black",*self.points[1],sup_height,self.radius,2)
        self.draw_tırtık(win,"black","down",self.points[1][0],self.tırtık_locy,sup_height,tırtık_height,tırtık_count,2)

    def __repr__(self):
        return f"|Support Type: roller, Location: {self.x}, Reaction Force: {self.ReactionForce}|"

    def __eq__(self, other):
        return isinstance(other, RollerSupport) and self.x == other.x

class DemoFixedSupport(Support, Demo):
    def __init__(self, side, demox, demoy, datas):
        self.side = side
        self.showx = demox
        self.showy = demoy

        self.datas = datas

    def draw(self,win):
        FixedSupport.draw_fixed_sup(win,BLACK,self.showx            ,self.showy,self.side,fixed_width/2,fixed_height/2,2)

    def __repr__(self):
        return f"demo-fixed: " + self.datas

    def __eq__(self,other):
        return isinstance(other, DemoFixedSupport) and self.showx == other.x and self.showy == other.y


class DemoPinnedSupport(PointSupport, Demo):
    def __init__(self, demox, demoy, datas):
        self.showx = demox
        self.showy = demoy
        self.points = ((demox,demoy),(demox - sup_height /2,demoy + sup_height),(demox + sup_height /2,demoy + sup_height))

        self.datas = datas

    def draw(self, win):
        super().draw(win)
        self.draw_tırtık(win,"black","down",*self.points[1],sup_height,tırtık_height,tırtık_count,2)

    def __repr__(self):
        return f"demo-pinned: " + self.datas

    def __eq__(self, other):
        return isinstance(other, DemoPinnedSupport) and self.datas == other.datas

class DemoRollerSupport(PointSupport, Demo):
    def __init__(self, x, y, datas):
        self.points = ((x,y),(x - sup_height /2,y + sup_height * 0.8),(x + sup_height /2,y + sup_height * 0.8))
        self.radius = 0.1 * sup_height
        self.tırtık_locy = y + sup_height * 0.8 + 1.9 * self.radius

        self.datas = datas

    def draw(self, win):
        super().draw(win)
        draw_circles(win,"black",*self.points[1],sup_height,self.radius,2)
        self.draw_tırtık(win,"black","down",self.points[1][0],self.tırtık_locy,sup_height,tırtık_height,tırtık_count,2)

    def __repr__(self):
        return f"|Support Type: demo-roller|" + self.datas

    def __eq__(self, other):
        return isinstance(other, DemoRollerSupport) and self.datas == other.datas


