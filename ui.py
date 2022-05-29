import pygame
import time
from variables import WIDTH, HEIGHT

mainfont = "berlinsansfbdemikalın"

def print_text(win,x,y,text,font="berlinsansfbdemikalın",fontsize=15,color=(0,0,0)):
    pos = (x,y)
    myfont = pygame.font.SysFont(font,fontsize)
    text_sur = myfont.render(text,True,color)
    win.blit(text_sur,pos)

def print_text_at_center(win,text_rect,text,font="berlinsansfbdemikalın",fontsize=15,color=(0,0,0)):
    xc = text_rect[0] + text_rect[2]/2
    yc = text_rect[1] + text_rect[3]/2
    myfont = pygame.font.SysFont(font,fontsize)
    text_sur = myfont.render(text,True,color)
    text_rect = text_sur.get_rect(center=(xc, yc))
    win.blit(text_sur,text_rect)

def draw_rect_at_center(win,COLOR,center_x,center_y,width,height,th):
    x = center_x - width/2
    y = center_y - height/2
    pygame.draw.rect(win,COLOR,(x,y,width,height),th)

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
        # Diagonal line
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round((a**2 + b**2) ** 0.5)
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

def draw_dashed_outline(win,outlinecolor,orect):
    draw_dashed_line(win,outlinecolor,orect.topright,orect.topleft,2)
    draw_dashed_line(win,outlinecolor,orect.bottomleft,orect.bottomright,2)
    draw_dashed_line(win,outlinecolor,orect.topleft,orect.bottomleft,2)
    draw_dashed_line(win,outlinecolor,orect.bottomright,orect.topright,2)

def display_message(win, message, text_rect):
    """Display a message for 1 second"""
    #text_rect = pygame.Rect(WIDTH/2-50,HEIGHT-30,100,20)
    myfont = pygame.font.SysFont(mainfont,12)
    text_sur = myfont.render(message,True,"black")
    win.blit(text_sur,text_rect)
    pygame.display.update()
    time.sleep(1)

def scale_rect(rect,scale_factor):
    center = rect.center
    rect.w = rect.w*scale_factor
    rect.h = rect.h*scale_factor
    rect.center = center
    return rect

def point_in_rect(point, rect):
    return rect[0] <= point[0] <= rect[0] + rect[2] and rect[1] <= point[1] <= rect[1] + rect[3]