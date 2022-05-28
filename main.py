import pygame
import ui
import inspect

from vars import WIDTH, FULLHEIGHT, HEIGHT
from vars import BEAM_LEFT, BEAM_RIGHT, BEAM_MID, BEAM_HEIGHT, BEAM_BOTTOM, BEAM_TOP, beam_length
from vars import UIX
from entry import Entry
from entry_handler import EntryHandler


from components import Component, DemoWithInfo
from components.force import Force
from components.support import Support, FixedSupport, PinnedSupport, RollerSupport
from components.distributed_load import Distload
from components.moment import Moment
from question_asker import QuestionAsker

pygame.init()

class BeamCalculator:
    NOT_SOLVABLE_RECT = pygame.Rect(WIDTH/2-50,HEIGHT-50,100,20)
    NOT_SOLVABLE_FONT = pygame.font.SysFont(ui.mainfont,12)
    NOT_SOLVABLE_SURF = NOT_SOLVABLE_FONT.render("The system has no solution",True,(255,0,0))

    ENTRY_START_X = WIDTH/2-100
    ENTRY_START_Y = 20
    ENTRY_SPACING = 10

    ERROR_MESSAGE_RECT = (WIDTH/2-50,HEIGHT-30,100,20)

    def __init__(self, beam_length):
        self.beam_length = beam_length

        self.win = pygame.display.set_mode((WIDTH, FULLHEIGHT))
        pygame.display.set_caption("Beam Calculator")
        self.objects = []
        self.solvable = True

        self.run = True

        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.objects.append(Force(5, 100000, 250, self.beam_length))
        self.objects.append(Moment(10, 100, self.beam_length))
        self.objects.append(Distload(1,10,10,100,"down",self.beam_length))

        # Ask for beam length at the start
        self.ask_for_beam_length()

        self.question_asker = QuestionAsker()


    def draw(self):
        """Draw everything on the screen"""

        #Drawing the beam
        ui.draw_rect_at_center(self.win,(173,216,230),BEAM_MID,BEAM_TOP,BEAM_RIGHT-BEAM_LEFT,BEAM_HEIGHT,0)
        ui.draw_rect_at_center(self.win,"black",BEAM_MID,BEAM_TOP,BEAM_RIGHT-BEAM_LEFT,BEAM_HEIGHT,1)

        ui.print_text(self.win,UIX,15,f"Beam length: {self.beam_length} m")

        #Drawing the objects and their demos at the bottom
        if self.objects:
            ui.print_text(self.win, UIX, HEIGHT-45, u"Click to delete \u21e9", font="cambria")
            x = 20
            for i, obj in enumerate(self.objects):
                obj.draw(self.win)
                obj.draw_shape_and_info(self.win, (x + (x+DemoWithInfo.OUTLINE_WIDTH) * i, HEIGHT - 25))

        #If the system is not solvable, warn user
        if not self.solvable:
            self.win.blit(self.NOT_SOLVABLE_SURF, self.NOT_SOLVABLE_RECT)

        try:
            self.entry_handler.draw(self.win)
        except AttributeError:
            pass

        pygame.display.update()

    def mainloop(self):
        while self.run:
            self.clock.tick(self.FPS)
            self.win.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break

                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_F8: self.ask_for_beam_length()
                    elif key == pygame.K_F7: self.show_plots()

                    new_component = self.question_asker.handle_key_inputs(key)
                    if new_component:
                        self.entry_handler = EntryHandler(self.get_entry_fields(new_component, new_component.CONSTRUCT_QUESTIONS), self.ENTRY_START_X, self.ENTRY_START_Y, ySpacing=10, asking_for=new_component) 

                    try:
                        self.entry_handler.handle_key_inputs(event)
                        self.handle_entry_handler_output()
                    except AttributeError:
                        pass

            self.draw()

    def get_entry_fields(self, component_type, questions):
        """Get entry fields to get user input."""
        entry_fields = []
        letter_input = False
        first_input = True #First input will be the active field

        if component_type == FixedSupport or component_type == Distload:
            #First input should be a string
            letter_input = True
        for question in questions:
            entry_fields.append(Entry(25,Prompt=(question,200,(255,255,255),(0,0,200)),Input=["",100,(255,255,255),(0,0,200)],getLetter=letter_input,Active = first_input,component_type=component_type))
            letter_input = False
            first_input = False

        return entry_fields

    def handle_entry_handler_output(self):
        if self.entry_handler.inputs_are_complete:
            self.handle_component_input(self.entry_handler.asking_for, self.entry_handler.results)
            self.entry_handler = None

    def handle_component_inputs(self, inputs):
        for i in inputs:
            self.handle_component_input(*i)

    def handle_component_input(self, asking_for, results):
        if inspect.isclass(asking_for) and issubclass(asking_for, Component):
            cls = asking_for
            if cls is FixedSupport:
                if results[0]=="left" or results[0]=="right":
                    NewOb = FixedSupport(results[0], self.beam_length)
                    self.objects.append(NewOb) 
                else:
                    ui.display_message(self.win,"Invalid entry", self.ERROR_MESSAGE_RECT)
                    ### Add printing previous invalid results  
            elif cls is PinnedSupport or cls is RollerSupport:
                try:
                    if float(results[0])>=0 and float(results[0])<=self.beam_length:
                        NewOb = cls(float(results[0]), self.beam_length)
                        self.objects.append(NewOb)
                    else:
                        ui.display_message(self.win,"Invalid entry", self.ERROR_MESSAGE_RECT)
                except:
                    pass
            elif cls is Force:
                try:
                    if float(results[0])>=0 and float(results[0])<=self.beam_length and float(results[1])>0:
                        NewOb = Force(float(results[0]),float(results[1]),float(results[2]), self.beam_length)
                        self.objects.append(NewOb)
                    else:
                        ui.display_message(self.win,"Invalid entry", self.ERROR_MESSAGE_RECT)
                except:
                    pass
            elif cls == Distload:
                try:
                    if str(results[0])=="up" or str(results[0])=="down" and float(results[1])>=0 and float(results[1])<=self.beam_length and float(results[3])>=0 and float(results[3])<=self.beam_length and float(results[2])>=0 and float(results[4])>=0 and float(results[1])<float(results[3]):
                        NewOb = Distload(float(results[1]),float(results[3]),float(results[2]),float(results[4]),str(results[0]), self.beam_length)
                        self.objects.append(NewOb) 
                    else:
                        ui.display_message(self.win,"Invalid entry", self.ERROR_MESSAGE_RECT)
                except:
                    pass  
            elif cls == Moment:
                try:
                    if float(results[0])>=0 and float(results[0])<=self.beam_length:
                        NewOb = Moment(float(results[0]),float(results[1]), self.beam_length)
                        self.objects.append(NewOb)  
                    else:
                        ui.display_message(self.win,"Invalid entry", self.ERROR_MESSAGE_RECT)
                except:
                    pass 
        elif asking_for == "beam":
            self.change_beam_length(float(results[0]))

    def ask_for_beam_length(self):
        self.entry_handler = EntryHandler(self.get_entry_fields(None, ("Beam Length",)), self.ENTRY_START_X, self.ENTRY_START_Y, ySpacing=self.ENTRY_SPACING, asking_for="beam") 

    def change_beam_length(self, beam_length):
        for obj in self.objects:
            obj.set_location_according_to_beam_length(beam_length)
        
        self.beam_length = beam_length

    def show_plots(self):
        pass


b = BeamCalculator(20)
b.mainloop()