import pygame
from myfuncs import ScaleRect
from myfuncs import draw_arrow as DrawArrow
from vars import WIDTH
from numpy import arange
from math import sqrt



from force import Force
from support import Support
from distributed_load import Distload
from moment import Moment
from button import Button
from vars import fixed_height

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
        c = round(sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)
    
class EntryHandler:
    def __init__(self,entries,x,y,xSpacing=0,ySpacing=0,Exist = True,type=None):
        self.entries = entries
        self.x = x
        self.y = y
        self.xSpacing = xSpacing
        self.ySpacing = ySpacing
        self.Exist = Exist
        self.results = None
        self.type = type
        self.arrowimg = pygame.image.load("arroww.png")
        ### change font with a press

    def DrawPrompts(self,win):
        if self.ySpacing:
            for i,entry in enumerate(self.entries):
                if i!=0:
                    text_rect = pygame.Rect(self.x,self.y+i*(self.ySpacing+self.entries[i-1].height),entry.PromptWidth,entry.height)
                else:
                    text_rect = pygame.Rect(self.x,self.y,entry.PromptWidth,entry.height)
                text_rect = ScaleRect(text_rect,0.95)
                myfont = pygame.font.SysFont(entry.font,entry.fontsize)
                text_sur = myfont.render(entry.PromptText,True,entry.PromptTextColor)
                win.blit(text_sur,text_rect)
                
                if entry.Active:
                    #pygame.draw.circle(win,(255,0,0),(text_rect.left-10,text_rect.centery),5)
                    #DrawArrow(win,entry.PromptBackgroundColor,(text_rect.left-40,text_rect.centery),(text_rect.left-10,text_rect.centery),2)
                    win.blit(self.arrowimg,(text_rect.left-60,text_rect.top-7))

    def DrawEntries(self,win):
        if self.ySpacing:
            for i,entry in enumerate(self.entries):
                if i!=0:
                    text_rect = pygame.Rect(self.x+entry.PromptWidth,self.y+i*(self.ySpacing+entry.height),entry.InputWidth,entry.height)
                else:
                    text_rect = pygame.Rect(self.x+entry.PromptWidth,self.y,entry.InputWidth,entry.height)
                text_rect = ScaleRect(text_rect,0.95)
                myfont = pygame.font.SysFont(entry.font,entry.fontsize)
                text_sur = myfont.render(entry.InputText,True,entry.InputTextColor)
                win.blit(text_sur,text_rect)


    def DrawBackground(self,win):
        if self.ySpacing:
            for i,entry in enumerate(self.entries):
                if i!=0:
                    PromptBg = pygame.Rect(self.x,self.y+i*(self.ySpacing+self.entries[i-1].height),entry.PromptWidth,entry.height)
                else:
                    PromptBg = pygame.Rect(self.x,self.y,entry.PromptWidth,entry.height)
                if i!=0:
                    InputBg = pygame.Rect(self.x+entry.PromptWidth,self.y+i*(self.ySpacing+entry.height),entry.InputWidth,entry.height)
                else:
                    InputBg = pygame.Rect(self.x+entry.PromptWidth,self.y,entry.InputWidth,entry.height)
                pygame.draw.rect(win,entry.PromptBackgroundColor,PromptBg)
                pygame.draw.rect(win,entry.InputBackgroundColor,InputBg)

    def DrawActive(self,win):
        type = self.GetActiveType()
        xoff = 40
        yoff = 20
        sideL = 100
        orect = pygame.Rect(WIDTH-xoff-sideL,yoff,sideL,sideL)
        if type == "fixed" or type == "pinned" or type == "roller" or type == "force" or type == "distload" or type == "moment":
            outlinecolor = (255,0,0)
            self.DrawDemoOutline(win,outlinecolor,orect)
        if type == "fixed":
            demo = Support("fixed",side="left",demo=True,demox = orect.centerx,demoy = orect.centery - fixed_height/4 )
        elif type == "pinned":
            demo = Support("pinned",demo=True,demox = orect.centerx,demoy = orect.centery)
        elif type == "roller":
            demo = Support("roller",demo=True,demox = orect.centerx,demoy = orect.centery)
        elif type == "force":
            demo = Force(0,10,45,demo=True,demox=orect.centerx-0.125*orect.w,demoy=orect.centery+0.125*orect.h)
        elif type == "distload":
            xoff = 10
            demo = Distload(orect.left + xoff,orect.right - xoff,2,3,"down",demo=True,demoy=orect.centery)
        elif type == "moment":
            demo = Moment(orect.centerx,1,demo=True,demoy=orect.centery)
        else:
            demo = None
            orect.w = orect.w * 1.1
            orect.h = orect.h * 1.1
            pygame.draw.rect(win,(255,255,255),orect)
        if demo:
            demo.draw(win,1)

#######################
    def DrawDemoOutline(self,win,outlinecolor,orect):
        draw_dashed_line(win,outlinecolor,orect.topright,orect.topleft,2)
        draw_dashed_line(win,outlinecolor,orect.bottomleft,orect.bottomright,2)
        draw_dashed_line(win,outlinecolor,orect.topleft,orect.bottomleft,2)
        draw_dashed_line(win,outlinecolor,orect.bottomright,orect.topright,2)


    def draw(self,win):
        self.DrawBackground(win)
        self.DrawPrompts(win)
        self.DrawEntries(win)
        self.DrawActive(win)


    def HandleKeyInputs(self,key):
        if key == pygame.K_DOWN:
            self.ActivateNextOne()
        elif key == pygame.K_UP:
            self.ActivatePreviousOne()  
        elif key == pygame.K_RETURN:
            if self.getActiveInd() != len(self.entries)-1:
                self.ActivateNextOne() 
            else: 
                self.ReturnResults()

        elif key == pygame.K_TAB:
            if self.NoActive():
                self.ActivateOne(0) 
            else:
                self.ActivateNextOne() 
        elif key == pygame.K_ESCAPE:
            self.DeactivateAll()
        else:
            pass

    def ActivateOne(self,index):
        for ind, entry in enumerate(self.entries):
            if ind == index:
                entry.Activate()
            else:
                entry.Deactivate()

    def DeactivateAll(self):
        for entry in self.entries:
            entry.Deactivate()

    def ActivateNextOne(self):
        n = len(self.entries)
        for ind, entry in enumerate(self.entries):
            if entry.Active:
                if ind == n-1:
                    self.ActivateOne(0)
                    break
                else:
                    self.ActivateOne(ind+1)
                    break

    def NoActive(self):
        for _, entry in enumerate(self.entries):
            if entry.Active:
                return False
        return True  

    def ActivatePreviousOne(self):
        n = len(self.entries)
        for ind, entry in enumerate(self.entries):
            if entry.Active:
                if ind == 0:
                    self.ActivateOne(n-1)
                    break
                else:
                    self.ActivateOne(ind-1)
                    break
    
    def HandleHovering(self,pos):
        for i,entry in enumerate(self.entries):
            if i!=0:
                promptrect = pygame.Rect(self.x,self.y+i*(self.ySpacing+self.entries[i-1].height),entry.PromptWidth,entry.height)
                inputrect = pygame.Rect(self.x+entry.PromptWidth,self.y+i*(self.ySpacing+entry.height),entry.InputWidth,entry.height)
            else:
                promptrect = pygame.Rect(self.x,self.y,entry.PromptWidth,entry.height)
                inputrect = pygame.Rect(self.x+entry.PromptWidth,self.y,entry.InputWidth,entry.height)

            if promptrect.x<=pos[0] and promptrect.x+promptrect.width>=pos[0]:
                if promptrect.y<=pos[1] and promptrect.y+promptrect.height>=pos[1]:
                    entry.hoveringprompt = True
                else: entry.hoveringprompt = False
            else: entry.hoveringprompt = False
            
            if inputrect.x<=pos[0] and inputrect.x+inputrect.width>=pos[0]:
                if inputrect.y<=pos[1] and inputrect.y+inputrect.height>=pos[1]:
                    entry.hoveringinput = True
                else: entry.hoveringinput = False
            else: entry.hoveringinput = False
        self.ChangeCursor()

    def ChangeCursor(self):
        for i,entry in enumerate(self.entries):
            if entry.hoveringprompt:
                HoveringSomePrompt = True
                break
            else: 
                HoveringSomePrompt = False
            if entry.hoveringinput:
                HoveringSomeInput = True
                break
            else: 
                HoveringSomeInput = False
        if HoveringSomePrompt:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif HoveringSomeInput:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def HandleMouseDown(self,pos):
        for i,entry in enumerate(self.entries):
            if entry.hoveringprompt:
                self.ActivateOne(i)
                break
            if entry.hoveringinput:
                self.ActivateOne(i)
                break

    def getActiveInd(self):
        for i,entry in enumerate(self.entries):
            if entry.Active:
                return i
        return None

    def TypeToActive(self,event):
        ind = self.getActiveInd()
        if isinstance(ind, int):
            if event.key == pygame.K_BACKSPACE:
                self.entries[ind].InputText = self.entries[ind].InputText[:-1]
            if self.entries[ind].getLetter:
                if event.unicode.isalpha():
                    if len(self.entries[ind].InputText)<=10:
                        self.entries[ind].InputText += event.unicode
            elif self.entries[ind].getLetter == False:
                try:
                    int(event.unicode) 
                    if len(self.entries[ind].InputText)<=10:
                        self.entries[ind].InputText += event.unicode
                except:
                    pass
                if str(event.unicode) == "." or str(event.unicode) == "-":
                   if len(self.entries[ind].InputText)<=10:
                        self.entries[ind].InputText += event.unicode 

    def GetActiveType(self):
        for entry in self.entries:
            if entry.Active:
                return entry.type
        return None
            
    def ReturnResults(self):
        self.results = []
        for i,entry in enumerate(self.entries):
            self.results.append(entry.InputText)
        self.Exist = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)




