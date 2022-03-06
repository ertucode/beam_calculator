import pygame

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
        self.big = False
        if self.x<=pos[0] and self.x+self.width>=pos[0]:
            if self.y<=pos[1] and self.y+self.height>=pos[1]:
                self.big = True


