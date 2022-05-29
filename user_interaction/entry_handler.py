import pygame
from variables import WIDTH
import ui

import inspect
from components import Component


    
class EntryHandler:
    
    DEMO_RECT = pygame.Rect(WIDTH-140, 20, 200, 200)
    def __init__(self,entries, x, y, xSpacing=0, ySpacing=0, asking_for=None):
        self.entries = entries
        self.x = x
        self.y = y
        self.xSpacing = xSpacing
        self.ySpacing = ySpacing
        self.inputs_are_complete = False
        self.results = None
        self.asking_for = asking_for
        self.arrowimg = pygame.image.load("images/arrow.png")

        if inspect.isclass(self.asking_for) and issubclass(self.asking_for, Component):
            self.demo = self.asking_for.create_demo()
            self.demo.setup_demo()

        else:
            self.demo = None
        

    def draw_prompts(self,win):
        """Draw questions"""
        if self.ySpacing:
            for i,entry in enumerate(self.entries):
                if i!=0:
                    text_rect = pygame.Rect(self.x,self.y+i*(self.ySpacing+self.entries[i-1].height),entry.prompt_width,entry.height)
                else:
                    text_rect = pygame.Rect(self.x,self.y,entry.prompt_width,entry.height)
                text_rect = ui.scale_rect(text_rect,0.95)
                myfont = pygame.font.SysFont(entry.font,entry.fontsize)
                text_sur = myfont.render(entry.prompt_text,True,entry.prompt_text_color)
                win.blit(text_sur,text_rect)
                
                if entry.active:
                    #pygame.draw.circle(win,(255,0,0),(text_rect.left-10,text_rect.centery),5)
                    #DrawArrow(win,entry.prompt_background_color,(text_rect.left-40,text_rect.centery),(text_rect.left-10,text_rect.centery),2)
                    win.blit(self.arrowimg,(text_rect.left-60,text_rect.top-7))

    def draw_entries(self,win):
        """Draw entries"""
        if self.ySpacing:
            for i,entry in enumerate(self.entries):
                if i!=0:
                    text_rect = pygame.Rect(self.x+entry.prompt_width,self.y+i*(self.ySpacing+entry.height),entry.input_width,entry.height)
                else:
                    text_rect = pygame.Rect(self.x+entry.prompt_width,self.y,entry.input_width,entry.height)
                text_rect = ui.scale_rect(text_rect,0.95)
                myfont = pygame.font.SysFont(entry.font,entry.fontsize)
                text_sur = myfont.render(entry.input_text,True,entry.input_text_color)
                win.blit(text_sur,text_rect)


    def draw_background(self,win):
        """Draw background"""
        if self.ySpacing:
            for i,entry in enumerate(self.entries):
                if i!=0:
                    PromptBg = pygame.Rect(self.x,self.y+i*(self.ySpacing+self.entries[i-1].height),entry.prompt_width,entry.height)
                else:
                    PromptBg = pygame.Rect(self.x,self.y,entry.prompt_width,entry.height)
                if i!=0:
                    InputBg = pygame.Rect(self.x+entry.prompt_width,self.y+i*(self.ySpacing+entry.height),entry.input_width,entry.height)
                else:
                    InputBg = pygame.Rect(self.x+entry.prompt_width,self.y,entry.input_width,entry.height)
                pygame.draw.rect(win,entry.prompt_background_color,PromptBg)
                pygame.draw.rect(win,entry.input_background_color,InputBg)

    def draw_demo_for_component(self,win):
        """Draw demo if a component is getting constructed"""
        if self.demo:
            self.demo.draw_demo_shape(win, self.DEMO_RECT.topleft)


    def draw(self,win):
        self.draw_background(win)
        self.draw_prompts(win)
        self.draw_entries(win)
        self.draw_demo_for_component(win)


    def handle_key_inputs(self, event):
        key = event.key
        if key == pygame.K_DOWN:
            self.activate_next_entry()
        elif key == pygame.K_UP:
            self.activate_previous_one()  
        elif key == pygame.K_RETURN:
            if self.get_active_index() != len(self.entries)-1:
                self.activate_next_entry() 
            else: 
                self.return_results()

        elif key == pygame.K_TAB:
            if self.no_active_entry():
                self.activate_entry(0) 
            else:
                self.activate_next_entry() 
        elif key == pygame.K_ESCAPE:
            self.deactive_all_entries()
        else:
            self.type_to_active_field(event)

    def activate_entry(self,index):
        """Activate an entry at the specific index"""
        for ind, entry in enumerate(self.entries):
            if ind == index:
                entry.activate()
            else:
                entry.deactivate()

    def deactive_all_entries(self):
        for entry in self.entries:
            entry.deactivate()

    def activate_next_entry(self):
        """Activate the entry at the next index"""
        n = len(self.entries)
        for ind, entry in enumerate(self.entries):
            if entry.active:
                if ind == n-1:
                    self.activate_entry(0)
                    break
                else:
                    self.activate_entry(ind+1)
                    break

    def no_active_entry(self):
        """Return true if no entry is active"""
        for _, entry in enumerate(self.entries):
            if entry.active:
                return False
        return True  

    def activate_previous_one(self):
        """Activate the entry at the previous index"""
        n = len(self.entries)
        for ind, entry in enumerate(self.entries):
            if entry.active:
                if ind == 0:
                    self.activate_entry(n-1)
                    break
                else:
                    self.activate_entry(ind-1)
                    break
    
    def handle_mouse_hover(self,pos):
        """Change mouse cursor if it is at the correct location"""
        for i,entry in enumerate(self.entries):
            if i!=0:
                promptrect = pygame.Rect(self.x,self.y+i*(self.ySpacing+self.entries[i-1].height),entry.prompt_width,entry.height)
                inputrect = pygame.Rect(self.x+entry.prompt_width,self.y+i*(self.ySpacing+entry.height),entry.input_width,entry.height)
            else:
                promptrect = pygame.Rect(self.x,self.y,entry.prompt_width,entry.height)
                inputrect = pygame.Rect(self.x+entry.prompt_width,self.y,entry.input_width,entry.height)

            if promptrect.x<=pos[0] and promptrect.x+promptrect.width>=pos[0]:
                if promptrect.y<=pos[1] and promptrect.y+promptrect.height>=pos[1]:
                    entry.hoveringprompt = True
                else: entry.hoveringprompt = False
            else: entry.hoveringprompt = False
            
            if inputrect.x<=pos[0] and inputrect.x+inputrect.width>=pos[0]:
                if inputrect.y<=pos[1] and inputrect.y+inputrect.height>=pos[1]:
                    entry.hoveringinput = True
                else: entry.hoveringinput = False
            else: entry.hoveringinput = False
        self.change_cursor()

    def change_cursor(self):
        hovering_some_prompt, hovering_some_input = False, False
        for i,entry in enumerate(self.entries):
            if entry.hoveringprompt:
                hovering_some_prompt = True
                break
            if entry.hoveringinput:
                hovering_some_input = True
                break
        if hovering_some_prompt:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif hovering_some_input:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_mouse_down(self,pos):
        """Activate an entry if it is pressed"""
        for i,entry in enumerate(self.entries):
            if entry.hoveringprompt:
                self.activate_entry(i)
                break
            if entry.hoveringinput:
                self.activate_entry(i)
                break

    def get_active_index(self):
        """Get the index of active index"""
        for i,entry in enumerate(self.entries):
            if entry.active:
                return i
        return None

    def type_to_active_field(self,event):
        """Type to the active field"""
        ind = self.get_active_index()
        if isinstance(ind, int):
            if event.key == pygame.K_BACKSPACE:
                self.entries[ind].input_text = self.entries[ind].input_text[:-1]
            if self.entries[ind].getLetter:
                if event.unicode.isalpha():
                    if len(self.entries[ind].input_text)<=10:
                        self.entries[ind].input_text += event.unicode
            elif self.entries[ind].getLetter == False:
                try:
                    int(event.unicode) 
                    if len(self.entries[ind].input_text)<=10:
                        self.entries[ind].input_text += event.unicode
                except:
                    pass
                if str(event.unicode) == "." or str(event.unicode) == "-":
                   if len(self.entries[ind].input_text)<=10:
                        self.entries[ind].input_text += event.unicode 
            
    def return_results(self):
        """Show that the entries are complete"""
        self.results = []
        for i,entry in enumerate(self.entries):
            self.results.append(entry.input_text)
        self.inputs_are_complete = True
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)




