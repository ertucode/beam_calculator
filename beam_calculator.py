import pygame
from vars import mainfont, FULLHEIGHT, sup_height
from entry_handler import draw_dashed_line
from time import sleep

from math import pi, sin,cos
from force import Force
from support import Support
from distributed_load import Distload
from moment import Moment
from button import Button

from entry import Entry
from entry_handler import EntryHandler
from numpy import array, linalg
import numpy as np
import myfuncs
import copy
import matplotlib.pyplot as plt


from vars import beam_left, beam_right, beam_mid, beam_length, beam_height,\
     beam_below,beam_y,WIDTH,HEIGHT,BLACK,WHITE,ButtonKeys,ButtonQuestions,ButtonTexts,\
         ButtonFont, ButtonFontSize, ButtonWidth, ButtonX, ButtonHeight, ButtonYStart, ButtonYInc

objects = {
    "supports": [],
    "forces": [],
    "distloads": [],
    "moments": []
}


imgpath = "button1.png"
pygame.init()

win = pygame.display.set_mode((WIDTH, FULLHEIGHT))
pygame.display.set_caption("Beam Calculator")

buttons = []
TextColor = (50,50,200)
TextColor = (200,50,50)
fontsize = 17
j=0
for i, button in enumerate(ButtonKeys):
    if i == 6:
        buttons.append(Button(ButtonX,ButtonYStart+i*ButtonYInc,width=ButtonWidth,height=ButtonHeight,imgloc=imgpath,text=ButtonTexts[i],fontsize=fontsize,fontcolor=TextColor,type=ButtonKeys[i][1]))
    else:
        buttons.append(Button(ButtonX,ButtonYStart+i*ButtonYInc,width=ButtonWidth,height=ButtonHeight,imgloc=imgpath,text=ButtonTexts[i],fontsize=fontsize,fontcolor=TextColor,questions=ButtonQuestions[j],type=ButtonKeys[i][1]))
        j+=1

def PrintText(win,x,y,text,font=mainfont,fontsize=15,color=(0,0,0)):
    pos = (x,y)
    myfont = pygame.font.SysFont(font,fontsize)
    text_sur = myfont.render(text,True,color)
    win.blit(text_sur,pos)

def PrintTextatCenter(win,text_rect,text,font=mainfont,fontsize=15,color=(0,0,0)):
    xc = text_rect[0] + text_rect[2]/2
    yc = text_rect[1] + text_rect[3]/2
    myfont = pygame.font.SysFont(font,fontsize)
    text_sur = myfont.render(text,True,color)
    text_rect = text_sur.get_rect(center=(xc, yc))
    win.blit(text_sur,text_rect)

def RemoveDuplicates(lst):
    out_list = []
    for val in lst:
        if not val in out_list:
            out_list.append(val)
    return out_list

def draw(win,objects,buttons,sol,handler=None,exists=False,beam_length=beam_length,offset=0):
    win.fill(WHITE)
    myfuncs.draw_at_center(win,(173,216,230),beam_mid,beam_y,beam_right-beam_left,beam_height,0)
    myfuncs.draw_at_center(win,BLACK,beam_mid,beam_y,beam_right-beam_left,beam_height,1)


    
    PrintText(win,ButtonX,15,f"Beam length: {beam_length} m")
    for subclass in objects:
        if len(objects[subclass])>0:
            text = u"Click to delete \u21e9"
            PrintText(win,ButtonX,HEIGHT-45,text,font="cambria")
            
            break

    rects = ShowObjects(win,objects,(20,HEIGHT - 20),20,100,FULLHEIGHT-HEIGHT+10,(220,220,255),offset)
    if not sol:
        if len(rects) > 0:
            text_rect = pygame.Rect(WIDTH/2-50,HEIGHT-50,100,20)
            myfont = pygame.font.SysFont(mainfont,12)
            text_sur = myfont.render("The system has no solution",True,(255,0,0))
            win.blit(text_sur,text_rect)

    if len(rects)>8:
        PrintText(win,WIDTH - 270 ,HEIGHT-45,f"Use arrow keys to access later objects")
    if exists:
        handler.draw(win)

    for button in buttons:
        button.draw(win)
    for subclass in objects:
        for object in objects[subclass]:
            object.draw(win,beam_length)
    
    

    pygame.display.update()
    return rects




def DrawDemoOutline(win,outlinecolor,orect):
    draw_dashed_line(win,outlinecolor,orect.topright,orect.topleft,2)
    draw_dashed_line(win,outlinecolor,orect.bottomleft,orect.bottomright,2)
    draw_dashed_line(win,outlinecolor,orect.topleft,orect.bottomleft,2)
    draw_dashed_line(win,outlinecolor,orect.bottomright,orect.topright,2)

def ShowObjects(win,objects,startpos,xoff,width,height,outlinecolor,offset):
    rects = []
    i = 0
    x = startpos[0] + offset*width
    y = startpos[1]
    txth = 15
    
    for subclass in objects:
        for object in objects[subclass]:
            orect = pygame.Rect(x+i*(width+xoff),y,width,height)
            rects.append(orect)
            i += 1
            if object.type == "fixed" or object.type == "pinned" or object.type == "roller" or object.type == "force" or object.type == "distload" or object.type == "moment":
                DrawDemoOutline(win,outlinecolor,orect)
            if object.type == "fixed":
                demo = Support("fixed",side=object.side,demo=True,demox = orect.centerx,demoy = orect.centery - height/4 - 30)
                datas = (f"type = {demo.type}",f"side = {demo.side}")
                for ind,data in enumerate(datas):
                    text_rect = orect.x,orect.y+ind*txth,width,height
                    PrintTextatCenter(win,text_rect,data,font="javanesetext",fontsize=14)

            elif object.type == "pinned" or object.type == "roller":
                demo = Support(object.type,x=object.x,demo=True,demox = orect.centerx,demoy = orect.top + sup_height - 20)
                datas = (f"type = {demo.type}",f"x = {demo.x}")
                for ind,data in enumerate(datas):
                    text_rect = orect.x,orect.y+ind*txth,width,height
                    PrintTextatCenter(win,text_rect,str(data),font="javanesetext",fontsize=14)
            elif object.type == "force":
                desy = orect.top + 40
                mag = object.forcelen/2
                posx = orect.centerx - cos(object.angle)*mag / 2
                posy = desy +sin(object.angle)*mag /2
                demo = Force(object.x,object.mag,object.deg,demo=True,demox=posx,demoy=posy)
                datas = (f"x = {demo.x}",f"Mag = {demo.mag}",f"Ang = {demo.deg}")
                for ind,data in enumerate(datas):
                    text_rect = orect.x,orect.y+ind*txth,width,height
                    PrintTextatCenter(win,text_rect,str(data),font="javanesetext",fontsize=14)
            elif object.type == "distload":
                xxoff = 10
                if object.dir == "down":
                    disy = orect.top + object.h
                elif object.dir == "up":
                    disy = orect.top + object.h/2
                demo = Distload(orect.left + xxoff,orect.right - xxoff,object.startmag,object.endmag,object.dir,demo=True,demoy=disy)
                datas = (f"Dir = {object.dir}",f"x_i = {object.startx}",f"x_f = {object.endx}",f"Mag_i = {object.startmag}",f"Mag_f = {object.endmag}")
                for ind,data in enumerate(datas):
                    text_rect = orect.x,orect.y+ind*txth,width,height
                    PrintTextatCenter(win,text_rect,str(data),font="javanesetext",fontsize=14)

            elif object.type == "moment":
                demo = Moment(orect.centerx,object.mag,demo=True,demoy=orect.top + object.momentw )
                datas = (f"x = {object.x}",f"Mag = {object.mag}",f"Dir = {object.dir}")
                for ind,data in enumerate(datas):
                    text_rect = orect.x,orect.y+ind*txth,width,height
                    PrintTextatCenter(win,text_rect,str(data),font="javanesetext",fontsize=14)
            else:
                demo = None
                orect.w = orect.w * 1.1
                orect.h = orect.h * 1.1
                pygame.draw.rect(win,(255,255,255),orect)
            if demo:
                demo.draw(win,1)
    return rects

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
    
    if nmat.shape[0] == nmat.shape[1]:
        if linalg.det(nmat) != 0:
            ans = linalg.solve(nmat,cons)
        else:
            return False
    else:
        return False
        
    
    for ind, support in enumerate(objects["supports"]):
        support.ReactionForce = ans[ind]

    for support in objects["supports"]:
        if support.type == "fixed":
            support.ReactionMoment = ans[-fixedcount]
            fixedcount -= 1
    
    return True


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

def CheckCollisionAtBottom(objects,rects):
    for ind,rct in enumerate(rects):
        if rct[0]<=pos[0] and rct[0]+rct[2]>=pos[0]:
            if rct[1]<=pos[1] and rct[1]+rct[3]>=pos[1]:
                i = 0
                for subclass in objects:
                    if len(objects[subclass])>0:
                        for ii,object in enumerate(objects[subclass]):
                            if i==ind:
                                return (ii, subclass)
                            i+=1

        
def GetEntryFields(type,questions):
    entries = []
    getLetter = False
    First = True
    if type == "fixed" or type == "distload":
        getLetter = True
    for question in questions:
        entries.append(Entry(25,Prompt=(question,200,(255,255,255),(0,0,200)),Input=["",100,(255,255,255),(0,0,200)],getLetter=getLetter,Active = First,type=type))
        getLetter = False
        First = False
    return entries

def DisplayErrorMessage(win,message):
    text_rect = pygame.Rect(WIDTH/2-50,HEIGHT-30,100,20)
    myfont = pygame.font.SysFont(mainfont,12)
    text_sur = myfont.render(message,True,BLACK)
    win.blit(text_sur,text_rect)
    pygame.display.update()
    sleep(1)


exists = False
deleted = True
run = True

####
entries = GetEntryFields(None,["Beam Length"])
handler = EntryHandler(entries,WIDTH/2-100,20,ySpacing=10,type="beam")
deleted = False
handler.Exist = True
exists = True


clock = pygame.time.Clock()
rects = []
tbr = 0
offset=0


while run:
    FPS = 60
    clock.tick(FPS)
    if exists:
        exists = handler.Exist
        if not exists:
            deleted = False

    if exists == False and deleted == False:
        del handler
        deleted = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if exists:
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                handler.HandleHovering(pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # deleting from downside
            tbr = CheckCollisionAtBottom(objects,rects)
            if tbr:
                del objects[tbr[1]][tbr[0]]
                tbr = 0


            if exists:
                handler.HandleMouseDown(pos)
            for button in buttons:
                button.isHovering(pos)
                if button.big:
                    if button.type == "fixed" or button.type == "pinned" or button.type == "roller" or button.type == "force" or button.type == "distload" or button.type == "moment":
                        entries= GetEntryFields(button.type,button.questions)
                        handler = EntryHandler(entries,WIDTH/2-100,20,ySpacing=10,type=button.type)
                        deleted = False
                        handler.Exist = True
                        exists = True
                    elif button.type == "show":
                        PlotDiagrams(objects,beam_length)

        if event.type == pygame.KEYDOWN:
            if exists:
                handler.HandleKeyInputs(event.key)
            if len(rects)>8:
                if event.key == pygame.K_RIGHT:
                    if offset > 6-len(rects):
                        offset -= 1
                elif event.key == pygame.K_LEFT:
                    if offset != 0:
                        offset +=1
            for i,keys in enumerate(ButtonKeys):
                if i==6:
                    if event.key == ButtonKeys[i][0]:
                        PlotDiagrams(objects,beam_length)
                else:
                    if event.key == ButtonKeys[i][0]:
                        type = ButtonKeys[i][1]
                        if i==7:
                            i=6
                        entries= GetEntryFields(type,ButtonQuestions[i])
                        handler = EntryHandler(entries,WIDTH/2-100,20,ySpacing=10,type=type)
                        # handler = copy.deepcopy(handler)
                        deleted = False
                        handler.Exist = True
                        exists = True
            
            if event.key == pygame.K_ASTERISK:
                print(objects)
            else:
                if exists: 
                    handler.TypeToActive(event)

    if not deleted:
        if handler.results:
            type = handler.type
            Ans = handler.results
            if type == "fixed":
                if Ans[0]=="left" or Ans[0]=="right":
                    NewOb = Support("fixed",side=Ans[0])
                    objects["supports"].append(NewOb) 
                else:
                    DisplayErrorMessage(win,"Invalid entry")
                    ### Add printing previous invalid results  
            elif type == "pinned" or type=="roller":
                try:
                    if float(Ans[0])>=0 and float(Ans[0])<=beam_length:
                        NewOb = Support(type,float(Ans[0]))
                        objects["supports"].append(NewOb)
                    else:
                        DisplayErrorMessage(win,"Invalid entry")
                except:
                    pass
            elif type == "force":
                try:
                    if float(Ans[0])>=0 and float(Ans[0])<=beam_length and float(Ans[1])>0:
                        NewOb = Force(float(Ans[0]),float(Ans[1]),float(Ans[2]))
                        objects["forces"].append(NewOb)
                    else:
                        DisplayErrorMessage(win,"Invalid entry")
                except:
                    pass
            elif type == "distload":
                try:
                    if str(Ans[0])=="up" or str(Ans[0])=="down" and float(Ans[1])>=0 and float(Ans[1])<=beam_length and float(Ans[3])>=0 and float(Ans[3])<=beam_length and float(Ans[2])>=0 and float(Ans[4])>=0 and float(Ans[1])<float(Ans[3]):
                        NewOb = Distload(float(Ans[1]),float(Ans[3]),float(Ans[2]),float(Ans[4]),str(Ans[0]))
                        objects["distloads"].append(NewOb) 
                    else:
                        DisplayErrorMessage(win,"Invalid entry")
                except:
                    pass  
            elif type == "moment":
                try:
                    if float(Ans[0])>=0 and float(Ans[0])<=beam_length:
                        NewOb = Moment(float(Ans[0]),float(Ans[1]))
                        objects["moments"].append(NewOb)  
                    else:
                        DisplayErrorMessage(win,"Invalid entry")
                except:
                    pass 
            elif type == "beam":
                beam_length = float(Ans[0])
    
    for subclass in objects:
        if len(objects[subclass])>1:
            objects[subclass] = RemoveDuplicates(objects[subclass])



    pos = pygame.mouse.get_pos()
    for button in buttons:
        button.isHovering(pos)
    if len(objects["supports"])>0:
        sol = CalculateSupportReactions(objects)
    else: sol=None
    if exists:
        rects = draw(win,objects,buttons,sol,handler,exists,beam_length=beam_length,offset=offset)
    else:
        rects = draw(win,objects,buttons,sol,beam_length=beam_length,offset=offset)
    
pygame.quit()


