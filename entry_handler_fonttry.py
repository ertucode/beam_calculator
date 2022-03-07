import pygame
from myfuncs import ScaleRect
from myfuncs import draw_arrow as DrawArrow
from vars import allfonts

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
        self.fonts = allfonts
        self.Nfonts = len(self.fonts)
        self.fontind = -1
        self.entrycounter = 0
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
                    DrawArrow(win,entry.PromptBackgroundColor,(text_rect.left-40,text_rect.centery),(text_rect.left-10,text_rect.centery),2)

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


    def draw(self,win):
        self.DrawBackground(win)
        self.DrawPrompts(win)
        self.DrawEntries(win)

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
        elif key == pygame.K_F12:
            self.fontind += 1
            if self.fontind == self.Nfonts:
                self.fontind = 0
            
            self.entrycounter +=1
            if self.entrycounter == len(self.entries):
                self.entrycounter = 0
            self.UpdateFont()

        elif key == pygame.K_F11:
            self.fontind -= 1
            if self.fontind <= -1:
                self.fontind = self.Nfonts-1
            
            self.entrycounter -=1
            if self.entrycounter == -1:
                self.entrycounter = len(self.entries)-1
            self.UpdateFont()
        elif key == pygame.K_KP_MULTIPLY:
            print(self.fonts[self.fontind])
        elif key == pygame.K_TAB:
            if self.NoActive():
                self.ActivateOne(0) 
            else:
                self.ActivateNextOne() 
        elif key == pygame.K_ESCAPE:
            self.DeactivateAll()
        else:
            pass
        
    def UpdateFont(self):
        print(self.entrycounter)
        self.entries[self.entrycounter].font = self.fonts[self.fontind]

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
            

    def ReturnResults(self):
        self.results = []
        for i,entry in enumerate(self.entries):
            self.results.append(entry.InputText)
        self.Exist = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)




