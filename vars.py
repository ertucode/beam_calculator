from pygame import *

WIDTH, HEIGHT = 1000, 400
WHITE = (255, 255, 255)
BLACK = (0,0,0)


beam_left = 400
beam_right = WIDTH-100
beam_mid = (beam_right+beam_left)/2
beam_length = 11
beam_height = 15
sup_height = 35
beam_y = HEIGHT / 2
beam_below = beam_y + beam_height / 2
tırtık_height = 5
tırtık_count = 6
forcelen = 75
momentw = 30
fixed_width = 10
fixed_height = 100
distload_h = 50

ButtonKeys = {"FixedSupportKey":K_1
            ,"PinnedSupportKey" : K_2
            ,"RollerSupportKey" : K_3
            ,"ForceKey" : K_4
            ,"DistributedLoadKey" : K_5
            ,"MomentKey" : K_6
            ,"ShowItemsKey" : K_7}

ButtonQuestions = {"FixedSupportQuestions":("Location[left/right]: ",)
                , "PinnedSupportQuestions":("Location[m]: ",)
                , "RollerSupportQuestions":("Location[m]: ",)
                , "ForceQuestions":("Location[m]: ","Magnitude[N]:","Angle[deg]:")
                , "DistributedLoadQuestions":("Direction[up/down]:","Starting Location[m]: ","Starting Magnitude[N/m]: ","Ending Location[m]: ","Ending Magnitude[N⋅m]: ")
                , "MomentQuestions":("Location[m]: ","Magnitude[N⋅m][""+"" for CCW ""-""CW]: ")}

ButtonTexts = {"FixedSupportText":"1-Fixed Support"
            ,"PinnedSupportText":"2-Pinned Support"
            ,"RollerSupportText":"3-Roller Support"
            ,"ForceText":"4-Force"
            ,"DistributedLoadText":"5-Distributed Load"
            ,"MomentText":"6-Moment"
            ,"ShowText":"7-Show Items"}

ButtonFont = "ComicSans"
ButtonFontSize = 13
ButtonWidth = 200
ButtonHeight = 30
ButtonXMid = 200
ButtonYStart = 50
NOfButtons = len(ButtonTexts)
ButtonYEnd = HEIGHT - ButtonYStart
ButtonYInc = (((ButtonYEnd - ButtonYStart) - NOfButtons * ButtonHeight) / (NOfButtons-1)) + ButtonHeight




