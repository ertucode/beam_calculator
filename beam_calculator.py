import pygame
import math
from force import Force
from support import Support
from distributed_load import Distload
from moment import Moment
import myfuncs
from vars import beam_left, beam_right, beam_mid, beam_length, beam_height,\
     beam_below,beam_y,WIDTH,HEIGHT,BLACK,WHITE,ButtonKeys,ButtonQuestions,ButtonTexts,\
         ButtonFont, ButtonFontSize, ButtonWidth, ButtonXMid, ButtonHeight, ButtonYStart, ButtonYInc



pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beam Calculator")


def DrawButtons(win,ButtonKeys,ButtonQuestions,ButtonTexts):
    myfuncs.DrawButton(win,BLACK,ButtonXMid,ButtonYStart,ButtonWidth,ButtonHeight,2,ButtonTexts["FixedSupportText"],BLACK,ButtonFont,ButtonFontSize)
    myfuncs.DrawButton(win,BLACK,ButtonXMid,ButtonYStart+1*ButtonYInc,ButtonWidth,ButtonHeight,2,ButtonTexts["PinnedSupportText"],BLACK,ButtonFont,ButtonFontSize)
    myfuncs.DrawButton(win,BLACK,ButtonXMid,ButtonYStart+2*ButtonYInc,ButtonWidth,ButtonHeight,2,ButtonTexts["RollerSupportText"],BLACK,ButtonFont,ButtonFontSize)
    myfuncs.DrawButton(win,BLACK,ButtonXMid,ButtonYStart+3*ButtonYInc,ButtonWidth,ButtonHeight,2,ButtonTexts["ForceText"],BLACK,ButtonFont,ButtonFontSize)
    myfuncs.DrawButton(win,BLACK,ButtonXMid,ButtonYStart+4*ButtonYInc,ButtonWidth,ButtonHeight,2,ButtonTexts["DistributedLoadText"],BLACK,ButtonFont,ButtonFontSize)
    myfuncs.DrawButton(win,BLACK,ButtonXMid,ButtonYStart+5*ButtonYInc,ButtonWidth,ButtonHeight,2,ButtonTexts["MomentText"],BLACK,ButtonFont,ButtonFontSize)
    myfuncs.DrawButton(win,BLACK,ButtonXMid,ButtonYStart+6*ButtonYInc,ButtonWidth,ButtonHeight,2,ButtonTexts["ShowText"],BLACK,ButtonFont,ButtonFontSize)

def draw(win,objects):
    win.fill(WHITE)
    myfuncs.draw_at_center(win,(173,216,230),beam_mid,beam_y,beam_right-beam_left,beam_height,0)

    for subclass in objects:
        for object in objects[subclass]:
            object.draw(win)
    
    DrawButtons(win,ButtonKeys,ButtonQuestions,ButtonTexts)

    pygame.display.update()


run = True

clock = pygame.time.Clock()

def AskForInputs(questions):
    answers = []
    for question in questions:
        answers.append(input(question))
    return answers

""" supports = []
forces = []
distloads = []
moments = [] """
objects = {
    "supports": [],
    "forces": [],
    "distloads": [],
    "moments": []
}

#def CalculateSupportReactions(objects):


while run:
    FPS = 60
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == ButtonKeys["FixedSupportKey"]:
                Ans = AskForInputs(ButtonQuestions["FixedSupportQuestions"])
                NewOb = Support("fixed",side=Ans[0])
                objects["supports"].append(NewOb)
            if event.key == ButtonKeys["PinnedSupportKey"]:
                Ans = AskForInputs(ButtonQuestions["PinnedSupportQuestions"])
                NewOb = Support("pinned",float(Ans[0]))
                objects["supports"].append(NewOb)
            if event.key == ButtonKeys["RollerSupportKey"]:
                Ans = AskForInputs(ButtonQuestions["RollerSupportQuestions"])
                NewOb = Support("roller",float(Ans[0]))
                objects["supports"].append(NewOb)
            if event.key == ButtonKeys["ForceKey"]:
                Ans = AskForInputs(ButtonQuestions["ForceQuestions"])
                NewOb = Force(float(Ans[0]),float(Ans[1]),float(Ans[2]))
                objects["forces"].append(NewOb)
            if event.key == ButtonKeys["DistributedLoadKey"]:
                Ans = AskForInputs(ButtonQuestions["DistributedLoadQuestions"])
                NewOb = Distload(float(Ans[1]),float(Ans[3]),float(Ans[2]),float(Ans[4]),str(Ans[0]))
                objects["distloads"].append(NewOb)          
            if event.key == ButtonKeys["MomentKey"]:
                Ans = AskForInputs(ButtonQuestions["MomentQuestions"])
                NewOb = Moment(float(Ans[0]),float(Ans[1]))
                objects["moments"].append(NewOb)
            if event.key == ButtonKeys["ShowItemsKey"]:
                print(objects)
    draw(win,objects)
pygame.quit()


