import pygame
import math

def map_value(val,min1,max1,min2,max2):
    return (val-min1)*(max2-min2)/(max1-min1)+min2

def draw_at_center(win,COLOR,center_x,center_y,width,height,th):
    x = center_x - width/2
    y = center_y - height/2
    pygame.draw.rect(win,COLOR,(x,y,width,height),th)

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

def draw_arrow_tip(win,COLOR,x,y,angle,size):
    tip1_ang = angle + 2*math.pi/6
    end1 = (x+math.cos(tip1_ang)*size,y+math.sin(tip1_ang)*size)
    tip2_ang = angle + 4*math.pi/6
    end2 = (x+math.cos(tip2_ang)*size,y+math.sin(tip2_ang)*size)
    pygame.draw.line(win,COLOR,(x,y),end1,2)
    pygame.draw.line(win,COLOR,(x,y),end2,2)
