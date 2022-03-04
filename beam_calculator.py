import pygame
import math
from force import Force
from support import Support
from distributed_load import Distload
from moment import Moment
from numpy import AxisError, array, linalg
import numpy as np
import myfuncs
import copy
import matplotlib.pyplot as plt
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

    
    if linalg.det(nmat) != 0:
        ans = linalg.solve(nmat,cons)
        #print(ans)
    else:
        print(f"There is no independent solution")
    
    for ind, support in enumerate(objects["supports"]):
        support.ReactionForce = ans[ind]

    for support in objects["supports"]:
        if support.type == "fixed":
            support.ReactionMoment = ans[-fixedcount]
            fixedcount -= 1
    
    objects["forces"] = myfuncs.RemoveLastN(objects["forces"],distcount)
  
def plottt(objects,beam_length):
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
    subplot[1].fill(x, shears, facecolor='blue', alpha=0.1)
    subplot[1].axhline(y=0, color='r', linestyle='--')
    plt.xlim([0,beam_length])
    plt.show()
        



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
                print(NewOb)
                CalculateSupportReactions(objects)
            if event.key == ButtonKeys["PinnedSupportKey"]:
                Ans = AskForInputs(ButtonQuestions["PinnedSupportQuestions"])
                NewOb = Support("pinned",float(Ans[0]))
                objects["supports"].append(NewOb)
                CalculateSupportReactions(objects)
            if event.key == ButtonKeys["RollerSupportKey"]:
                Ans = AskForInputs(ButtonQuestions["RollerSupportQuestions"])
                NewOb = Support("roller",float(Ans[0]))
                objects["supports"].append(NewOb)
                CalculateSupportReactions(objects)
            if event.key == ButtonKeys["ForceKey"]:
                Ans = AskForInputs(ButtonQuestions["ForceQuestions"])
                NewOb = Force(float(Ans[0]),float(Ans[1]),float(Ans[2]))
                objects["forces"].append(NewOb)
                CalculateSupportReactions(objects)
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
            if event.key == pygame.K_8:
                CalculateSupportReactions(objects)
            if event.key == pygame.K_9:
                for support in objects["supports"]:
                    print(support)
            if event.key == pygame.K_a:
                plottt(objects,beam_length)

    draw(win,objects)
pygame.quit()


