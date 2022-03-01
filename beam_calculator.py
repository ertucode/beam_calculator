import pygame
import math
from force import Force
from support import Support
from distributed_load import Distload
from moment import Moment
import myfuncs
from vars import beam_left, beam_right, beam_mid, beam_length, beam_height,\
     beam_below,beam_y,WIDTH,HEIGHT,BLACK,WHITE,ButtonKeys,ButtonQuestions


pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beam Calculator")


myforce = Force(7,100,120)
mysup = Support("pinned",5)
mysup2 = Support("roller",12)
mysup3 = Support("fixed",side = "right")
supports = [mysup,mysup2,mysup3]
myload = Distload(2,10,10,20,"up")
mymoment = Moment(10,-30)
objects = [myload,mymoment,myforce] + supports

def draw(win,objects):
    win.fill(WHITE)
    myfuncs.draw_at_center(win,(173,216,230),beam_mid,beam_y,beam_right-beam_left,beam_height,0)

    for object in objects:
        object.draw(win)

    

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

while run:
    FPS = 60
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == ButtonKeys.FixedSupportKey:
                Ans = AskForInputs(ButtonQuestions.FixedSupportQuestions)
                NewOb = supports.append(Support("fixed",Ans))
                objects.append = NewOb
            if event.key == ButtonKeys.PinnedSupportKey:
                Ans = AskForInputs(ButtonQuestions.PinnedSupportQuestions)
                NewOb = supports.append(Support("pinned",float(Ans)))
                objects.append = NewOb
            if event.key == ButtonKeys.RollerSupportKey:
                Ans = AskForInputs(ButtonQuestions.RollerSupportQuestions)
                NewOb = supports.append(Support("roller",float(Ans)))
                objects.append = NewOb
            if event.key == ButtonKeys.ForceKey:
                Ans = AskForInputs(ButtonQuestions.ForceQuestions)
                NewOb = forces.append(Force(float(Ans[0]),float(Ans[1]),float(Ans[2])))
                objects.append = NewOb
            if event.key == ButtonKeys.DistributedLoadKey:
                NewOb = distloads.append(Distload(float(Ans[1]),float(Ans[3]),float(Ans[2]),float(Ans[4]),str(Ans[0])))
                objects.append = NewOb           
            if event.key == ButtonKeys.MomentKey:
                Ans = AskForInputs(ButtonQuestions.MomentQuestions)
                NewOb = moments.append(Moment(float(Ans[0]),float(Ans[1])))
                objects.append = NewOb

    draw(win,objects)
pygame.quit()


