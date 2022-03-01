import pygame
import math
from force import Force
from support import Support
from distributed_load import Distload
from moment import Moment
import myfuncs
from vars import beam_left, beam_right, beam_mid, beam_length, beam_height,\
     beam_below,beam_y,WIDTH,HEIGHT,BLACK,WHITE,ButtonKeys,ButtonQuestions,ButtonTexts,\
         ButtonFont


pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beam Calculator")


def DrawButtons(win,ButtonKeys,ButtonQuestions,ButtonTexts):
    myfuncs.DrawButton(win,BLACK,WIDTH/2,20,200,40,2,ButtonTexts["FixedSupportText"],BLACK,ButtonFont,20)
    myfuncs.DrawButton(win,BLACK,WIDTH/2,60,200,40,2,ButtonTexts["PinnedSupportText"],BLACK,ButtonFont,20)
    myfuncs.DrawButton(win,BLACK,WIDTH/2,100,200,40,2,ButtonTexts["RollerSupportText"],BLACK,ButtonFont,20)
    myfuncs.DrawButton(win,BLACK,WIDTH/2,140,200,40,2,ButtonTexts["ForceText"],BLACK,ButtonFont,20)
    myfuncs.DrawButton(win,BLACK,WIDTH/2,180,200,40,2,ButtonTexts["DistributedLoadText"],BLACK,ButtonFont,20)
    myfuncs.DrawButton(win,BLACK,WIDTH/2,220,200,40,2,ButtonTexts["MomentText"],BLACK,ButtonFont,20)
    myfuncs.DrawButton(win,BLACK,WIDTH/2,260,200,40,2,ButtonTexts["ShowText"],BLACK,ButtonFont,20)

def draw(win,objects):
    win.fill(WHITE)
    myfuncs.draw_at_center(win,(173,216,230),beam_mid,beam_y,beam_right-beam_left,beam_height,0)

    for object in objects:
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

supports = []
forces = []
distloads = []
moments = []
objects = []


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
                supports.append(NewOb)
                objects.append(NewOb)
            if event.key == ButtonKeys["PinnedSupportKey"]:
                Ans = AskForInputs(ButtonQuestions["PinnedSupportQuestions"])
                NewOb = Support("pinned",float(Ans[0]))
                supports.append(NewOb)
                objects.append(NewOb)
            if event.key == ButtonKeys["RollerSupportKey"]:
                Ans = AskForInputs(ButtonQuestions["RollerSupportQuestions"])
                NewOb = Support("roller",float(Ans[0]))
                supports.append(NewOb)
                objects.append(NewOb)
            if event.key == ButtonKeys["ForceKey"]:
                Ans = AskForInputs(ButtonQuestions["ForceQuestions"])
                NewOb = Force(float(Ans[0]),float(Ans[1]),float(Ans[2]))
                forces.append(NewOb)
                objects.append(NewOb)
            if event.key == ButtonKeys["DistributedLoadKey"]:
                Ans = AskForInputs(ButtonQuestions["DistributedLoadQuestions"])
                NewOb = Distload(float(Ans[1]),float(Ans[3]),float(Ans[2]),float(Ans[4]),str(Ans[0]))
                distloads.append(NewOb)
                objects.append(NewOb)           
            if event.key == ButtonKeys["MomentKey"]:
                Ans = AskForInputs(ButtonQuestions["MomentQuestions"])
                NewOb = Moment(float(Ans[0]),float(Ans[1]))
                moments.append(NewOb)
                objects.append(NewOb)
            if event.key == ButtonKeys["ShowItemsKey"]:
                print(objects[0])
                print(objects)
    draw(win,objects)
pygame.quit()


