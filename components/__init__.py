import pygame
import math
from variables import HEIGHT, FULLHEIGHT
import ui

class ShapeDemo:
    """Demo surface for just showing the shape"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.surface = pygame.Surface((width + 5, height + 5))
        self.surface.fill("white")
        ui.draw_dashed_outline(self.surface, (220,220,255), pygame.Rect(0, 0, width, height))

class ShapeDemoWithInfo(ShapeDemo):
    """Demo surface for showing the shape and the info"""
    def __init__(self, width, height, text_offset):
        super().__init__(width, height)
        self.text_offset = text_offset

demo_for_shape = ShapeDemo(100, 116)
demo_with_info = ShapeDemoWithInfo(100, FULLHEIGHT - HEIGHT + 10, 15)

class Component:
    """Common functions for the components"""
    def draw_shape_and_info(self, surface, point):
        surface.blit(self.demo_surface, point)  

    def draw_demo_shape(self, surface, point):
        demo_surface = pygame.Surface.copy(demo_for_shape.surface)
        demo_surface.blit(self.demo_surface, (0,0), (0, 0, demo_for_shape.width, demo_for_shape.height - 5))
        surface.blit(demo_surface, point)

    def print_demo_data(self, datas, rect):
        for ind,data in enumerate(datas):
            text_rect = rect.x,rect.y+ind*demo_with_info.text_offset,demo_with_info.width, demo_with_info.height
            ui.print_text_at_center(self.demo_surface,text_rect,data,font="javanesetext",fontsize=14)


def map_value(val,min1,max1,min2,max2):
    """Map a value to an interval"""
    return (val-min1)*(max2-min2)/(max1-min1)+min2

def draw_arrow(win,COLOR,startpos,endpos,th):
    """Draw an arrow from startpos to endpos"""
    line_len = math.sqrt((endpos[1]-startpos[1])**2+(endpos[0]-startpos[0])**2)
    arrow_len = line_len / 8
    angle = math.atan2((endpos[1]-startpos[1]),(endpos[0]-startpos[0]))
    pygame.draw.line(win,COLOR,startpos,endpos,2)
    tip1_ang = angle + 7*math.pi/6
    end1 = (endpos[0]+math.cos(tip1_ang)*arrow_len,endpos[1]+math.sin(tip1_ang)*arrow_len)
    tip2_ang = angle + 5*math.pi/6
    end2 = (endpos[0]+math.cos(tip2_ang)*arrow_len,endpos[1]+math.sin(tip2_ang)*arrow_len)
    pygame.draw.line(win,COLOR,endpos,end1,th)
    pygame.draw.line(win,COLOR,endpos,end2,th)




