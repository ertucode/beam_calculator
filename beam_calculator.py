import pygame
import math
from force import Force
from support import Support
from distributed_load import Distload
from moment import Moment
from button import Button
from numpy import AxisError, array, linalg
import numpy as np
import myfuncs
import copy
import matplotlib.pyplot as plt

from vars import beam_left, beam_right, beam_mid, beam_length, beam_height,\
     beam_below,beam_y,WIDTH,HEIGHT,BLACK,WHITE,ButtonKeys,ButtonQuestions,ButtonTexts,\
         ButtonFont, ButtonFontSize, ButtonWidth, ButtonX, ButtonHeight, ButtonYStart, ButtonYInc



pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beam Calculator")

buttons = []
TextColor = WHITE
fontsize = 17
buttons.append(Button(ButtonX,ButtonYStart,imgloc="buttonnn.png",text=ButtonTexts["FixedSupport"],fontsize=fontsize,fontcolor=TextColor,questions=ButtonQuestions["FixedSupport"],type="fixed"))
buttons.append(Button(ButtonX,ButtonYStart+1*ButtonYInc,imgloc="buttonnn.png",text=ButtonTexts["PinnedSupport"],fontsize=fontsize,fontcolor=TextColor,questions=ButtonQuestions["PinnedSupport"],type="pinned"))
buttons.append(Button(ButtonX,ButtonYStart+2*ButtonYInc,imgloc="buttonnn.png",text=ButtonTexts["RollerSupport"],fontsize=fontsize,fontcolor=TextColor,questions=ButtonQuestions["RollerSupport"],type="roller"))
buttons.append(Button(ButtonX,ButtonYStart+3*ButtonYInc,imgloc="buttonnn.png",text=ButtonTexts["Force"],fontsize=fontsize,fontcolor=TextColor,questions=ButtonQuestions["Force"],type="force"))
buttons.append(Button(ButtonX,ButtonYStart+4*ButtonYInc,imgloc="buttonnn.png",text=ButtonTexts["DistributedLoad"],fontsize=fontsize,fontcolor=TextColor,questions=ButtonQuestions["DistributedLoad"],type="distload"))
buttons.append(Button(ButtonX,ButtonYStart+5*ButtonYInc,imgloc="buttonnn.png",text=ButtonTexts["Moment"],fontsize=fontsize,fontcolor=TextColor,questions=ButtonQuestions["Moment"],type="moment"))
buttons.append(Button(ButtonX,ButtonYStart+6*ButtonYInc,imgloc="buttonnn.png",text=ButtonTexts["ShowDiagrams"],fontsize=fontsize,fontcolor=TextColor,type="show"))

def draw(win,objects,buttons,sol):
    win.fill(WHITE)
    myfuncs.draw_at_center(win,(173,216,230),beam_mid,beam_y,beam_right-beam_left,beam_height,0)
    myfuncs.draw_at_center(win,BLACK,beam_mid,beam_y,beam_right-beam_left,beam_height,1)

    if not sol:
        pygame.draw.circle(win,(255,0,0),(WIDTH/2,20),10)

    for button in buttons:
        button.draw(win)
    for subclass in objects:
        for object in objects[subclass]:
            object.draw(win)
    
    

    pygame.display.update()


run = True

clock = pygame.time.Clock()

def AskForInputs(questions):
    answers = []
    for question in questions:
        answers.append(input(question))
    return answers

objects = {
    "supports": [Support("pinned",0),Support("roller",8)],
    "forces": [Force(11,20,270)],
    "distloads": [Distload(0,8,40,40,"down")],
    "moments": [Moment(11,-150)]
}

def CalculateSupportReactions(objects):
    fy = 0
    distcount = 0
    try:
        for distload in objects["distloads"]:
            ang = 90 if distload.dir == "up" else 270
            objects["forces"].append(Force(distload.EqLoc,distload.EqForce,ang))
            distcount += 1
    except:
        pass

    for force in objects["forces"]:
        fy +=force.fy

    totalmom = 0
    for moment in objects["moments"]:
        totalmom += moment.mag

    rows = []
    row1 = []
    for support in objects["supports"]:
        row1.append(1)
    
    rows.append(row1)
    rrow = []
    rrow.append(-fy)

    for support in objects["supports"]:
        newrow = []
        fmom = 0
        for force in objects["forces"]:
            fmom += force.fy * (force.x-support.x)
        for othersup in objects["supports"]:
            newrow.append(othersup.x-support.x)
        rows.append(newrow)
        rrow.append(-fmom-totalmom) 
    delete = True
    fixedcount = 0
    for support in objects["supports"]:
        if support.type == "fixed":
            delete = False
            fixedcount +=1
            for row in rows:
                row.append(1)
            rows[0][-1] = 0


    if delete:
        del rows[-1]
        del rrow[-1]

    nmat = array(rows)
    cons = array(rrow)

    objects["forces"] = myfuncs.RemoveLastN(objects["forces"],distcount)
    
    if linalg.det(nmat) != 0:
        ans = linalg.solve(nmat,cons)
        #print(ans)
    else:
        #print(f"There is no independent solution")
        return False
        
    
    for ind, support in enumerate(objects["supports"]):
        support.ReactionForce = ans[ind]

    for support in objects["supports"]:
        if support.type == "fixed":
            support.ReactionMoment = ans[-fixedcount]
            fixedcount -= 1
    
    return True
    
def GetUserInput(win):
    getting = True
    user_input = ""
    text_rect = pygame.Rect(WIDTH/2,20,300,20)
    InputFont = pygame.font.SysFont("comicsans",15)
    while getting:
        bg = pygame.Rect(ButtonX+ButtonWidth,0,WIDTH,100)
        pygame.draw.rect(win,WHITE,bg)
        text_sur = InputFont.render(user_input,True,BLACK)
        pygame.draw.rect(win,BLACK,text_rect,2)
        win.blit(text_sur,(text_rect.x+5,text_rect.centery-text_rect.height/2))
        text_rect.w = max(text_sur.get_width() + 10,200)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global run
                run = False
                getting = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    print(user_input)
                    return user_input
                    getting = False
                else:
                    user_input += event.unicode
                if event.key == pygame.K_ESCAPE:
                    getting = False



def PlotDiagrams(objects,beam_length):
    inc = 0.005
    shears = []
    moments = []
    x = np.arange(0,beam_length,inc)
    SupForcedCopy = copy.deepcopy(objects)
    for support in SupForcedCopy["supports"]:
        ang = 90 if support.ReactionForce >= 0 else 270
        SupForcedCopy["forces"].append(Force(support.x,support.ReactionForce,ang))
        if support.type == "fixed":
            SupForcedCopy["moments"].append(Moment(support.x,support.ReactionMoment))
    
    del SupForcedCopy["supports"]
    
    for i in range(len(x)):
        IncludedObjects = copy.deepcopy(SupForcedCopy)
        for distload in IncludedObjects["distloads"]:
            if distload.startx < x[i]:
                if distload.endx > x[i]:
                    distload.endx = x[i]
                    distload.CalcEquivalent()
            ang = 90 if distload.dir == "up" else 270
            IncludedObjects["forces"].append(Force(distload.EqLoc,distload.EqForce,ang))
        del IncludedObjects["distloads"]
        for subclass in IncludedObjects:
                for object in IncludedObjects[subclass]:
                    if object.x > x[i]:
                        IncludedObjects[subclass].remove(object)
        IncludedObjects["supports"] = []
        IncludedObjects["supports"].append(Support("fixed",x[i],side="sec-right"))
        CalculateSupportReactions(IncludedObjects)
        shears.append(-IncludedObjects["supports"][0].ReactionForce)
        moments.append(IncludedObjects["supports"][0].ReactionMoment)
    
    x = np.insert(x,0,0)
    x = np.append(x,beam_length)
    shears.insert(0,0)
    moments.insert(0,0)
    shears.append(0)
    moments.append(0)

    fig, subplot = plt.subplots(2,sharex=True)
    subplot[0].plot(x,shears)
    subplot[0].set_title("Shear Diagram")
    subplot[0].fill(x, shears, facecolor='blue', alpha=0.1)
    subplot[0].axhline(y=0, color='r', linestyle='--')
    plt.xlim([0,beam_length])
    subplot[1].plot(x,moments)
    subplot[1].set_title("Moment Diagram")
    subplot[1].fill(x, moments, facecolor='blue', alpha=0.1)
    subplot[1].axhline(y=0, color='r', linestyle='--')
    plt.xlim([0,beam_length])
    plt.show()
        



while run:
    FPS = 60
    clock.tick(FPS)
    t = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                button.isHovering(pos)
                if button.big:
                    Ans = AskForInputs(button.questions)
                    if button.type == "fixed":
                        NewOb = Support("fixed",side=Ans[0])
                        objects["supports"].append(NewOb)   
                    elif button.type == "pinned":
                        NewOb = Support("pinned",float(Ans[0]))
                        objects["supports"].append(NewOb)
                    elif button.type == "roller":
                        NewOb = Support("roller",float(Ans[0]))
                        objects["supports"].append(NewOb)
                    elif button.type == "force":
                        NewOb = Force(float(Ans[0]),float(Ans[1]),float(Ans[2]))
                        objects["forces"].append(NewOb)
                    elif button.type == "distload":
                        NewOb = Distload(float(Ans[1]),float(Ans[3]),float(Ans[2]),float(Ans[4]),str(Ans[0]))
                        objects["distloads"].append(NewOb)   
                    elif button.type == "moment":
                        NewOb = Moment(float(Ans[0]),float(Ans[1]))
                        objects["moments"].append(NewOb)   
                    elif button.type == "show":
                        PlotDiagrams(objects,beam_length)

        if event.type == pygame.KEYDOWN:
            if  event.key == ButtonKeys["FixedSupportKey"]:
                Ans = AskForInputs(ButtonQuestions["FixedSupport"])
                NewOb = Support("fixed",side=Ans[0])
                objects["supports"].append(NewOb)
            if event.key == ButtonKeys["PinnedSupportKey"]:
                Ans = AskForInputs(ButtonQuestions["PinnedSupport"])
                NewOb = Support("pinned",float(Ans[0]))
                objects["supports"].append(NewOb)
            if event.key == ButtonKeys["RollerSupportKey"]:
                Ans = AskForInputs(ButtonQuestions["RollerSupport"])
                NewOb = Support("roller",float(Ans[0]))
                objects["supports"].append(NewOb)
            if event.key == ButtonKeys["ForceKey"]:
                Ans = AskForInputs(ButtonQuestions["Force"])
                NewOb = Force(float(Ans[0]),float(Ans[1]),float(Ans[2]))
                objects["forces"].append(NewOb)
            if event.key == ButtonKeys["DistributedLoadKey"]:
                Ans = AskForInputs(ButtonQuestions["DistributedLoad"])
                NewOb = Distload(float(Ans[1]),float(Ans[3]),float(Ans[2]),float(Ans[4]),str(Ans[0]))
                objects["distloads"].append(NewOb)          
            if event.key == ButtonKeys["MomentKey"]:
                Ans = AskForInputs(ButtonQuestions["Moment"])
                NewOb = Moment(float(Ans[0]),float(Ans[1]))
                objects["moments"].append(NewOb)
            if event.key == ButtonKeys["ShowDiagramsKey"]:
                PlotDiagrams(objects,beam_length)
            if event.key == pygame.K_b:
                GetUserInput(win)
            t = 0

    pos = pygame.mouse.get_pos()
    for button in buttons:
        button.isHovering(pos)
    sol = CalculateSupportReactions(objects)
    draw(win,objects,buttons,sol)
    
pygame.quit()


