import pygame
import math
from vars import HEIGHT, FULLHEIGHT
import ui

def init_demo(width, height):
    OUTLINE_COLOR = (220,220,255)
    DEMO_SURFACE = pygame.Surface((width + 5, height + 5))
    DEMO_SURFACE.fill("white")
    ui.draw_dashed_outline(DEMO_SURFACE, OUTLINE_COLOR, pygame.Rect(0, 0, width, height))
    return DEMO_SURFACE

class DemoWithInfo:
    OUTLINE_WIDTH = 100
    OUTLINE_HEIGHT = FULLHEIGHT - HEIGHT + 10
    DEMO_SURFACE = init_demo(OUTLINE_WIDTH, OUTLINE_HEIGHT)

class DemoForShape:
    OUTLINE_WIDTH = 100
    OUTLINE_HEIGHT = 116
    DEMO_SURFACE = init_demo(OUTLINE_WIDTH, OUTLINE_HEIGHT)

class Component:
    def draw_shape_and_info(self, surface, point):
        surface.blit(self.demo_surface, point)  

    def draw_demo_shape(self, surface, point):
        demo_surface = pygame.Surface.copy(DemoForShape.DEMO_SURFACE)
        demo_surface.blit(self.demo_surface, (0,0), (0, 0, DemoWithInfo.OUTLINE_WIDTH, DemoForShape.OUTLINE_HEIGHT - 5))
        surface.blit(demo_surface, point)

TIRTIK_HEIGHT = 5
TIRTIK_COUNT = 6

def map_value(val,min1,max1,min2,max2):
    return (val-min1)*(max2-min2)/(max1-min1)+min2

def draw_arrow(win,COLOR,startpos,endpos,th):
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



TEXT_YOFFSET = 15
def print_demo_data(surf, datas, orect, width, height):
    for ind,data in enumerate(datas):
        text_rect = orect.x,orect.y+ind*TEXT_YOFFSET,width,height
        ui.print_text_at_center(surf,text_rect,data,font="javanesetext",fontsize=14)
