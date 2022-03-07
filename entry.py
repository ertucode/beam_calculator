from vars import EntryFont


class Entry:
    def __init__(self,height,font=EntryFont,fontsize=12,Prompt = None,Input = None,Active = False,getLetter=False,type=None):
        self.height = height
        self.font = font
        self.fontsize = fontsize
        self.Active = Active
        self.getLetter = getLetter
        
        self.hoveringprompt = False
        self.hoveringinput = False
        self.type = type

        if Prompt != None:
            self.PromptText = Prompt[0]
            self.PromptWidth = Prompt[1]
            self.PromptTextColor = Prompt[2]
            self.PromptBackgroundColor = Prompt[3]

        if Input != None:
            self.InputText = Input[0]
            self.InputWidth = Input[1]
            self.InputTextColor = Input[2]
            self.InputBackgroundColor = Input[3]    

    def Activate(self):
        self.Active = True

    def Deactivate(self):
        self.Active = False
  
