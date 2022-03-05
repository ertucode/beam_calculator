import pygame
from sys import exit as CloseProgram

class Button:
    def __init__(self,x,y,width=0,height=0,thickness=0,color = None,imgloc = None,text="",font="comicsans",fontsize=10,fontcolor = (0,0,0),questions=[],type=None):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.big = False
        self.questions = questions
        self.type = type

        self.imgloc = imgloc
        if self.imgloc:
            self.InitializeImg()
        else:
            self.width = width
            self.height = height
            self.color = color
            self.thickness = thickness


    def InitializeImg(self):
        self.img = pygame.image.load(self.imgloc)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.scale = 1.1
        self.IMG = pygame.transform.scale(self.img,(self.width*self.scale,self.height*self.scale))

    def draw(self,win):
        self.ToggleBig()
        if self.big == True:
            win.blit(self.IMG,(self.x - self.width *(self.scale-1)/2,self.y - self.height*(self.scale-1)/2))
        elif self.img:
            win.blit(self.img,(self.x,self.y))
        else:
            pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height),self.thickness)
        myfont = pygame.font.SysFont(self.font, self.fontsize)
        TextRender = myfont.render(self.text,True,self.fontcolor)
        TextRect = TextRender.get_rect(center=(self.x+self.width/2,self.y+self.height/2))
        win.blit(TextRender,TextRect)

    def isHovering(self,pos):
        self.hover = False
        if self.x<=pos[0] and self.x+self.width>=pos[0]:
            if self.y<=pos[1] and self.y+self.height>=pos[1]:
                self.hover = True
                return True
        return False

    def ToggleBig(self):
        self.big = self.hover


class EntryField:
    def __init__(self,x,y,PromptWidth=0,EntryWidth=80,height=0,thickness=0,color = None,imgloc = None,PromptText="",EntryText="",font="comicsans",fontsize=10,\
        fontcolor = (0,0,0),bgcolor = (255,255,255),outlinecolor = (0,0,0),outlinethickness=2,type=None,\
            minbox = 800,place=1):
        self.x = x
        self.y = y
        self.height = height
        self.PromptWidth = PromptWidth
        self.EntryWidth = EntryWidth
        self.set_width()
        self.EntryText = EntryText
        self.PromptText = PromptText
        self.font = font
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.outlinecolor = outlinecolor
        self.outlinethickness = outlinethickness
        self.bgcolor = bgcolor
        self.type = type
        self.LOffset = 0.1
        self.TOffset = 0.1
        self.minbox = minbox
        self.place = place
        self.Active = False
        self.hover = False
        self.deactivate = False
        self.tabbing = False

    def set_width(self):
        self.width = self.PromptWidth + self.EntryWidth

    def GetUserInput(self,win,count):
        all_rect = pygame.Rect(self.x,self.y,self.width,self.height)
        
        ###  + self.PromptWidth*self.LOffset,self.prompt.top + self.height*self.TOffset
        # Write entry
        
        if self.Drawing:
            # Write prompt
            bg = pygame.Rect(self.x,self.y,self.width,self.height)
            pygame.draw.rect(win,self.bgcolor,bg)
            self.prompt_rect = pygame.Rect(self.x + self.PromptWidth * self.LOffset,self.y,self.PromptWidth,self.height)
            InputFont = pygame.font.SysFont(self.font,self.fontsize)
            prompt_text_sur = InputFont.render(self.PromptText,True,self.fontcolor)
            win.blit(prompt_text_sur,self.prompt_rect)
            if self.Active:
                outlinecolor = (155,155,0)
            else:
                outlinecolor = self.outlinecolor
            pygame.draw.rect(win,outlinecolor,all_rect,self.outlinethickness)
            entry_text_sur = InputFont.render(self.EntryText,True,self.fontcolor)
            win.blit(entry_text_sur,(self.x + self.PromptWidth + self.EntryWidth * self.LOffset,self.prompt_rect.top + self.height*self.TOffset))
            
            if self.Active:
                bg = pygame.Rect(self.x + (1-self.LOffset)*self.PromptWidth ,self.y + self.TOffset*self.height ,self.EntryWidth,self.height*(1-2*self.TOffset))
                pygame.draw.rect(win,self.bgcolor,bg)
                #pygame.draw.rect(win,(50,50,50),bg)
                entry_text_sur = InputFont.render(self.EntryText,True,self.fontcolor)
                self.set_width()
                
                
                win.blit(entry_text_sur,(self.x + self.PromptWidth + self.EntryWidth * self.LOffset,self.prompt_rect.top + self.height*self.TOffset))
                all_rect.w = max(self.PromptWidth + entry_text_sur.get_width() + 10 , self.minbox)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        CloseProgram()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if self.isHovering(pos):
                            pass
                        else:
                            self.Active = False
                            self.deactivate = True
                            print("deactivate")
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.EntryText = self.EntryText[:-1]
                        elif event.key == pygame.K_RETURN:
                            print(self.EntryText)
                            return self.EntryText
                        elif event.key == pygame.K_ESCAPE:
                            #self.NotDrawing()
                            self.Active = False
                            self.deactivate = True
                        elif event.key == pygame.K_F10:
                            self.Active = False
                        elif event.key == pygame.K_F11:
                            self.Active = True
                        elif event.key == pygame.K_TAB:
                            self.Active = False
                            self.tabbing = True
                        else:
                            if len(self.EntryText)<10:
                                self.EntryText += event.unicode
                #pygame.display.update()

        return ["None",None]

    def ChangeActivity(self,place):
        if self.place == place:
            self.Active = True

    def NotDrawing(self):
        self.Drawing = False
        self.Active = False

    def isHovering(self,pos):
        self.hover = False
        if self.x<=pos[0] and self.x+self.width>=pos[0]:
            if self.y<=pos[1] and self.y+self.height>=pos[1]:
                self.hover = True
                return True
            else: return False
        else: return False


