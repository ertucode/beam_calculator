

class Entry:
    def __init__(self,height,font="berlinsansfbdemikalın",fontsize=12,prompt = None,inp = None,active = False,getLetter=False,component_type=None):
        self.height = height
        self.font = font
        self.fontsize = fontsize
        self.active = active
        self.getLetter = getLetter  # Entry field that will only accept letter
        
        self.hoveringprompt = False
        self.hoveringinput = False
        self.component_type = component_type

        if prompt != None:  # Question part variables
            self.prompt_text = prompt[0]
            self.prompt_width = prompt[1]
            self.prompt_text_color = prompt[2]
            self.prompt_background_color = prompt[3]

        if inp != None:   # Input part variables
            self.input_text = inp[0]
            self.input_width = inp[1]
            self.input_text_color = inp[2]
            self.input_background_color = inp[3]    

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
  
