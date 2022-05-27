import pygame
import math
import copy

def map_value(val,min1,max1,min2,max2):
    return (val-min1)*(max2-min2)/(max1-min1)+min2

def draw_rect_at_center(win,COLOR,center_x,center_y,width,height,th):
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

def DrawButton(win,BUTTONCOLOR,x,y,width,height,th,text,TEXTCOLOR,FontType,FontSize):
    x = x - width / 2
    y = y - height / 2
    ButtonRect = pygame.Rect(x,y,width,height)
    pygame.draw.rect(win,BUTTONCOLOR,ButtonRect,th)
    myfont = pygame.font.SysFont(FontType, FontSize)
    TextRender = myfont.render(text,True,TEXTCOLOR)
    TextRect = TextRender.get_rect(center=(x+width/2,y+height/2))
    win.blit(TextRender,TextRect)

def DrawButtonImg(win,BUTTONCOLOR,x,y,width,height,th,text,TEXTCOLOR,FontType,FontSize):
    ButtonImg = pygame.image.load("images/button.png")
    x = x - width / 2
    y = y - height / 2
    ButtonRect = pygame.Rect(x,y,width,height)
    win.blit(ButtonImg,(x,y-height/2))
    myfont = pygame.font.SysFont(FontType, FontSize)
    TextRender = myfont.render(text,True,TEXTCOLOR)
    TextRect = TextRender.get_rect(center=(x+width/2,y+height/2))
    TextRect.y = TextRect.y + 10
    win.blit(TextRender,TextRect)

def scale_rect(rect,ScaleFactor):
    center = rect.center
    rect.w = rect.w*ScaleFactor
    rect.h = rect.h*ScaleFactor
    rect.center = center
    return rect

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in range(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in range(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)

def DrawDemoOutline(win,outlinecolor,orect):
    draw_dashed_line(win,outlinecolor,orect.topright,orect.topleft,2)
    draw_dashed_line(win,outlinecolor,orect.bottomleft,orect.bottomright,2)
    draw_dashed_line(win,outlinecolor,orect.topleft,orect.bottomleft,2)
    draw_dashed_line(win,outlinecolor,orect.bottomright,orect.topright,2)