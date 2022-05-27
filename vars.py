from pygame import *

WIDTH, HEIGHT = 1000, 400
WHITE = (255, 255, 255)
BLACK = (0,0,0)
FULLHEIGHT = HEIGHT + 200


BEAM_LEFT = 400
BEAM_RIGHT = WIDTH-100
BEAM_MID = (BEAM_RIGHT+BEAM_LEFT)/2
beam_length = 11
BEAM_HEIGHT = 15
BEAM_TOP = 5* HEIGHT / 8
BEAM_BOTTOM = BEAM_TOP + BEAM_HEIGHT / 2







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

UIX = 50


