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
img = image.load("buttonnn.png")

ButtonKeys = ([K_F1,"fixed"]
            ,[K_F2,"pinned"]
            ,[K_F3,"roller"]
            ,[K_F4,"force"]
            ,[K_F5,"distload"]
            ,[K_F6,"moment"]
            ,[K_F7,None])

ButtonQuestions = (("Location[left/right]: ",)
                , ("Location[m]: ",)
                , ("Location[m]: ",)
                , ("Location[m]: ","Magnitude[N]:","Angle[deg]:")
                , ("Direction[up/down]:","Starting Location[m]: ","Starting Magnitude[N/m]: ","Ending Location[m]: ","Ending Magnitude[N⋅m]: ")
                , ("Location[m]: ","Magnitude[N⋅m][""+"" for CCW ""-""CW]: "))

ButtonTexts = {"FixedSupport":"1-Fixed Support"
            ,"PinnedSupport":"2-Pinned Support"
            ,"RollerSupport":"3-Roller Support"
            ,"Force":"4-Force"
            ,"DistributedLoad":"5-Distributed Load"
            ,"Moment":"6-Moment"
            ,"ShowDiagrams":"7-Show Diagrams"}

ButtonFont = "ComicSans"
ButtonFontSize = 15
ButtonWidth = img.get_width()
ButtonHeight = 30
ButtonX = 100
ButtonYStart = 35
NOfButtons = len(ButtonTexts)
ButtonYEnd = HEIGHT - ButtonYStart
ButtonYInc = (((ButtonYEnd - ButtonYStart) - NOfButtons * ButtonHeight) / (NOfButtons-1)) + ButtonHeight




