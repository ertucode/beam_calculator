import pygame
from vars import ButtonFont

def textOutline(font, message, fontcolor, outlinecolor):
    base = font.render(message, 0, fontcolor)
    outline = textHollow(font, message, outlinecolor)
    img = pygame.Surface(outline.get_size(), 16)
    img.blit(base, (1, 1))
    img.blit(outline, (0, 0))
    img.set_colorkey(0)
    return img

def textHollow(font, message, fontcolor):
    notcolor = [c^0xFF for c in fontcolor]
    base = font.render(message, 0, fontcolor, notcolor)
    size = base.get_width() + 2, base.get_height() + 2
    img = pygame.Surface(size, 16)
    img.fill(notcolor)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, notcolor)
    img.blit(base, (1, 1))
    img.set_colorkey(notcolor)
    return img

class Button:
    def __init__(self,x,y,width=0,height=0,thickness=0,color = None,imgloc = None,text="",font=ButtonFont,fontsize=10,fontcolor = (0,255,0),questions=[],type=None,textoffset = 0.05):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.big = False
        self.questions = questions
        self.type = type
        self.textoffset = textoffset

        self.imgloc = imgloc
        if self.imgloc:
            self.InitializeImg()
        else:
            self.color = color
            self.thickness = thickness


    def InitializeImg(self):
        self.img = pygame.image.load(self.imgloc)
        self.img = pygame.transform.scale(self.img,(self.width,self.height))
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

        self.drawTextLeftRight(win)


    def drawTextLeftRight(self,win):
        myfont = pygame.font.SysFont(self.font, self.fontsize)
        if len(self.text)==1 or isinstance(self.text,str):
            TextRender = myfont.render(self.text,True,self.fontcolor)
            TextRect = TextRender.get_rect(center=(self.x+self.width/2,self.y+self.height/2))
            win.blit(TextRender,TextRect)

        elif len(self.text) == 2:
            self.yc = self.y + self.height/2
            text1 = myfont.render(self.text[0],True,self.fontcolor)
            text2 = myfont.render(self.text[1],True,self.fontcolor)
            text1 = textOutline(myfont, self.text[0], (0,200,0), (1,1,1))
            text2 = textOutline(myfont, self.text[1], (0,200,0), (1,1,1))
            self.yc = self.y + (self.height-text1.get_height())/2

            text1pos = (self.x + self.textoffset * self.width ,self.yc)
            text2pos = (self.x + self. width - text2.get_width() - self.textoffset * self.width,self.yc)
            win.blit(text1,text1pos)
            win.blit(text2,text2pos)




    def isHovering(self,pos):
        self.big = False
        if self.x<=pos[0] and self.x+self.width>=pos[0]:
            if self.y<=pos[1] and self.y+self.height>=pos[1]:
                self.big = True


