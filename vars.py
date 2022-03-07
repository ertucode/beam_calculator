from pygame import *

WIDTH, HEIGHT = 1000, 400
WHITE = (255, 255, 255)
BLACK = (0,0,0)
FULLHEIGHT = HEIGHT + 200


beam_left = 400
beam_right = WIDTH-100
beam_mid = (beam_right+beam_left)/2
beam_length = 11
beam_height = 15
sup_height = 35
beam_y = 5* HEIGHT / 8
beam_below = beam_y + beam_height / 2
tırtık_height = 5
tırtık_count = 6
forcelen = 75
momentw = 30
fixed_width = 10
fixed_height = 100
distload_h = 50

ButtonKeys = ([K_F1,"fixed"]
            ,[K_F2,"pinned"]
            ,[K_F3,"roller"]
            ,[K_F4,"force"]
            ,[K_F5,"distload"]
            ,[K_F6,"moment"]
            ,[K_F7,None]
            ,[K_F8,"beam"])

ButtonQuestions = (("Location[left/right]: ",)
                , ("Location[m]: ",)
                , ("Location[m]: ",)
                , ("Location[m]: ","Magnitude[N]:","Angle[deg]:")
                , ("Direction[up/down]:","Starting Location[m]: ","Starting Magnitude[N/m]: ","Ending Location[m]: ","Ending Magnitude[N/m]: ")
                , ("Location[m]: ","Magnitude[Nm][""+"" for CCW ""-""CW]: ")
                , ("Beam Length[m]:",))

ButtonTexts = (("Fixed Support","F1")
            ,("Pinned Support","F2")
            ,("Roller Support","F3")
            ,("Force","F4")
            ,("Distributed Load","F5")
            ,("Moment","F6")
            ,("Show Diagrams","F7")
            ,("Change beam length","F8"))

ButtonFont = "berlinsansfbdemikalın"
EntryFont = "berlinsansfbdemikalın"
mainfont = "berlinsansfbdemikalın"
ButtonFontSize = 15
ButtonWidth = 220
ButtonHeight = 50
ButtonX = 50
ButtonYStart = 35
NOfButtons = len(ButtonTexts)
ButtonYEnd = HEIGHT - ButtonYStart
ButtonYInc = (((ButtonYEnd - ButtonYStart) - NOfButtons * ButtonHeight) / (NOfButtons-1)) + ButtonHeight

# import os
#allfonts = (os.listdir(r'C:\Windows\fonts'))
#allfonts = (font.get_fonts())




