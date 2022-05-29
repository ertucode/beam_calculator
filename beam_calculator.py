import pygame
import ui
import inspect
import json
from tkinter import filedialog, simpledialog

from variables import WIDTH, FULLHEIGHT, HEIGHT
from variables import BEAM_LEFT, BEAM_RIGHT, BEAM_MID, BEAM_HEIGHT, BEAM_TOP
from user_interaction.entry import Entry
from user_interaction.entry_handler import EntryHandler


from components import Component, DemoWithInfo
from components.force import Force
from components.support import FixedSupport, PinnedSupport, RollerSupport, Support
from components.distributed_load import Distload
from components.moment import Moment
from user_interaction.question_asker import QuestionAsker

import calculate

pygame.init()

class BeamCalculator:
    # İnitializing the text to show when solution is not possible
    NOT_SOLVABLE_RECT = pygame.Rect(WIDTH/2-50,HEIGHT-50,100,20)
    NOT_SOLVABLE_FONT = pygame.font.SysFont(ui.mainfont,12)
    NOT_SOLVABLE_SURF = NOT_SOLVABLE_FONT.render("The system has no solution",True,(255,0,0))

    # Start of the location of the entries
    ENTRY_START_X = WIDTH * 0.5 -100
    ENTRY_START_Y = 20
    ENTRY_SPACING = 10

    # Rectangle to use for error messages
    ERROR_MESSAGE_RECT = (WIDTH/2-50,HEIGHT-30,100,20)

    # Shortcuts to display
    SHORTCUTS = ("F1 - Fixed Support",
                "F2 - Pinned Support",
                "F3 - Roller Support",
                "F4 - Force",
                "F5 - Distributed Load",
                "F6 - Moment",
                "F7 - Show Diagrams",
                "F8 - Change beam length",
                "F9 - Save components to a file",
                "F10 - Load components from a file")
    # Start of the shortcuts ui Y
    SHORTCUT_TEXT_YSTART = 40

    # Start of the ui X
    UIX = 50

    # Start of the ui at the bottom X
    BOTTOM_DEMO_START_X = 20

    def __init__(self, beam_length):
        self.beam_length = beam_length

        self.win = pygame.display.set_mode((WIDTH, FULLHEIGHT))
        pygame.display.set_caption("Beam Calculator")
        self.components = []
        self.solvable = False

        self.run = True

        self.FPS = 60
        self.clock = pygame.time.Clock()
        
        # Ask for beam length at the start
        if not self.components:
            self.ask_for_beam_length()
        
        self.question_asker = QuestionAsker()

        self.index_of_changing = -1 # Variable to hold which item is changing


    def draw(self):
        """Draw everything on the screen"""

        #Drawing the beam
        ui.draw_rect_at_center(self.win,(173,216,230),BEAM_MID,BEAM_TOP,BEAM_RIGHT-BEAM_LEFT,BEAM_HEIGHT,0)
        ui.draw_rect_at_center(self.win,"black",BEAM_MID,BEAM_TOP,BEAM_RIGHT-BEAM_LEFT,BEAM_HEIGHT,1)

        # Show beam length
        ui.print_text(self.win,self.UIX,15,f"Beam length: {self.beam_length} m")

        #Drawing the objects and their demos at the bottom
        if self.components:
            ui.print_text(self.win, self.UIX, HEIGHT-45, u"Left Click to delete \u21e9", font="cambria")
            ui.print_text(self.win, self.UIX + 200, HEIGHT-45, u"Right Click to change \u21e9", font="cambria")

            for i, obj in enumerate(self.components):
                obj.draw(self.win)
                obj.draw_shape_and_info(self.win, (self.BOTTOM_DEMO_START_X + (self.BOTTOM_DEMO_START_X+DemoWithInfo.OUTLINE_WIDTH) * i, HEIGHT - 25))

        # If the system is not solvable, warn user
        if not self.solvable:
            self.win.blit(self.NOT_SOLVABLE_SURF, self.NOT_SOLVABLE_RECT)

        # Show user inputs and questions
        if self.entry_handler:
            self.entry_handler.draw(self.win)

        # Display shortcut keys
        self.display_shortcuts()

        pygame.display.update()

    def mainloop(self):
        while self.run:
            self.clock.tick(self.FPS)
            self.win.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if self.entry_handler:
                        self.entry_handler.handle_mouse_down(pos) # Change active input if mouse collides
                    self.handle_mouse_pressed(pos, event.button) # Delete or change component
                
                elif event.type == pygame.MOUSEMOTION:
                    if self.entry_handler:
                        self.entry_handler.handle_mouse_hover(pygame.mouse.get_pos()) # Change cursor if mouse collides

                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_F8:
                        self.ask_for_beam_length() # Change beam length
                    elif key == pygame.K_F7: 
                        if self.solvable:
                            calculate.plot_diagrams(self.group_components(), self.beam_length)  # Show plots

                    elif key == pygame.K_F9:self.save_to_json()
                    elif key == pygame.K_F10: self.load_from_json()
                    
                    new_component = self.question_asker.handle_key_inputs(key)
                    if new_component:  # If relevant key is pressed, ask the questions to construct new component
                        self.index_of_changing = -1
                        self.entry_handler = EntryHandler(self.get_entry_fields(new_component, new_component.CONSTRUCT_QUESTIONS), self.ENTRY_START_X, self.ENTRY_START_Y, ySpacing=10, asking_for=new_component) 
                    
                    # If the entry fields exist handle key presses
                    if self.entry_handler:
                        self.entry_handler.handle_key_inputs(event)
                        self.handle_entry_handler_output()

            self.draw()

    def get_entry_fields(self, component_type, questions, answers = None):
        """
        Get entry fields to get user input.
        Can contain default answers
        """
        entry_fields = []
        letter_input = False
        first_input = True # First input will be the active field

        if answers is None:
            answers = tuple("" for _ in range(len(questions)))

        if component_type == FixedSupport or component_type == Distload:
            # First input should be a string
            letter_input = True
        for question, inp in zip(questions, answers):
            entry_fields.append(Entry(25,prompt=(question,200,(255,255,255),(0,0,200)),inp=[str(inp),100,(255,255,255),(0,0,200)],getLetter=letter_input,active = first_input,component_type=component_type))
            letter_input = False
            first_input = False

        return entry_fields

    def handle_entry_handler_output(self):
        """If enter is pressed at the last input field, handle the input"""
        if self.entry_handler.inputs_are_complete:
            if self.index_of_changing != -1:
                del self.components[self.index_of_changing]
            self.handle_component_input(self.entry_handler.asking_for, self.entry_handler.results)

    def handle_component_input(self, asking_for, results):
        """If input is valid, construct a component or change beam length"""
        if inspect.isclass(asking_for) and issubclass(asking_for, Component):
            cls = asking_for
            if cls is FixedSupport:
                if results[0]=="left" or results[0]=="right":
                    NewOb = FixedSupport(results[0], self.beam_length)
                    self.insert_component(NewOb)
                    self.entry_handler = None 
                else:
                    ui.display_message(self.win,"Invalid entry", self.ERROR_MESSAGE_RECT) 
            elif cls is PinnedSupport or cls is RollerSupport:
                if float(results[0])>=0 and float(results[0])<=self.beam_length:
                    NewOb = cls(float(results[0]), self.beam_length)
                    self.insert_component(NewOb)
                    self.entry_handler = None
                else:
                    ui.display_message(self.win,"Invalid entry", self.ERROR_MESSAGE_RECT)
            elif cls is Force:
                if float(results[0])>=0 and float(results[0])<=self.beam_length and float(results[1])>0:
                    NewOb = Force(float(results[0]),float(results[1]),float(results[2]), self.beam_length)
                    self.insert_component(NewOb)
                    self.entry_handler = None
                else:
                    ui.display_message(self.win,"Invalid entry", self.ERROR_MESSAGE_RECT)
            elif cls == Distload:
                if str(results[0])=="up" or str(results[0])=="down" and float(results[1])>=0 and float(results[1])<=self.beam_length and float(results[3])>=0 and float(results[3])<=self.beam_length and float(results[2])>=0 and float(results[4])>=0 and float(results[1])<float(results[3]):
                    NewOb = Distload(float(results[1]),float(results[3]),float(results[2]),float(results[4]),str(results[0]), self.beam_length)
                    self.insert_component(NewOb)
                    self.entry_handler = None 
                else:
                    ui.display_message(self.win,"Invalid entry", self.ERROR_MESSAGE_RECT)
            elif cls == Moment:
                if float(results[0])>=0 and float(results[0])<=self.beam_length:
                    NewOb = Moment(float(results[0]),float(results[1]), self.beam_length)
                    self.insert_component(NewOb)
                    self.entry_handler = None  
                else:
                    ui.display_message(self.win,"Invalid entry", self.ERROR_MESSAGE_RECT)
        elif asking_for == "beam":
            self.change_beam_length(float(results[0]))
            self.entry_handler = None

    def ask_for_beam_length(self):
        """Create the entry field to ask for beam length"""
        self.entry_handler = EntryHandler(self.get_entry_fields(None, ("Beam Length",)), self.ENTRY_START_X, self.ENTRY_START_Y, ySpacing=self.ENTRY_SPACING, asking_for="beam") 

    def change_beam_length(self, beam_length):
        """Change component locations according to the new beam length"""
        for obj in self.components:
            obj.set_location_according_to_beam_length(beam_length)
        
        self.beam_length = beam_length

    def display_shortcuts(self):
        """Display shortcuts"""
        for i, text in enumerate(self.SHORTCUTS):
            ui.print_text(self.win, self.UIX, self.SHORTCUT_TEXT_YSTART + i * 30, text)

    def insert_component(self, component):
        """Insert a component and check if the system is solvable"""
        component.setup_demo()
        self.components.append(component)
        self.components.sort(key = lambda comp: comp.x)
        self.solvable = calculate.calculate_support_reactions(self.group_components())

    def remove_component(self, ind):
        """Remove a component and check if the system is solvable"""
        del self.components[ind]
        if self.index_of_changing >= 0: # If a component was changing, get out of that state
            self.index_of_changing = -1
            self.entry_handler = None
        self.solvable = calculate.calculate_support_reactions(self.group_components())

    def change_component(self, ind):
        """
        Ask the questions for the component at the index, with default answers being that components values
        If the state is not interrupted until an output is given that component is replaced with a new one
        """
        comp = self.components[ind]
        class_name = type(comp)
        
        if isinstance(comp, Distload):
            answers = (comp.direction, comp.startx, comp.startmag, comp.endx, comp.endmag)
        elif isinstance(comp, FixedSupport):
            answers = (comp.side,)
        elif isinstance(comp, (PinnedSupport, RollerSupport)):
            answers = (comp.x,)
        elif isinstance(comp, Force):
            answers = (comp.x, comp.mag, comp.angle_in_degrees)
        elif isinstance(comp, Moment):
            answers = (comp.x, comp.mag)

        self.entry_handler = EntryHandler(self.get_entry_fields(class_name, class_name.CONSTRUCT_QUESTIONS, answers), self.ENTRY_START_X, self.ENTRY_START_Y, ySpacing=10, asking_for=class_name) 
        self.index_of_changing = ind


    def group_components(self):
        """Group components to improve calculation speed"""
        dct = {"distloads": [], "supports": [], "forces": [], "moments": []}
        for comp in self.components:
            if isinstance(comp, Distload):
                dct["distloads"].append(comp)
            elif isinstance(comp, Support):
                dct["supports"].append(comp)
            elif isinstance(comp, Force):
                dct["forces"].append(comp)
            elif isinstance(comp, Moment):
                dct["moments"].append(comp)

        return dct

    def save_to_json(self):
        """
        Save components to a json file
        .json is added to the user input
        """
        dct = {"distloads": [], "supports": [], "forces": [], "moments": []}
        for comp in self.components:
            if isinstance(comp, Distload):
                dct["distloads"].append((type(comp).__name__, comp.direction, comp.startx, comp.startmag, comp.endx, comp.endmag))
            elif isinstance(comp, FixedSupport):
                dct["supports"].append((type(comp).__name__, comp.side))
            elif isinstance(comp, (PinnedSupport, RollerSupport)):
                dct["supports"].append((type(comp).__name__, comp.x))
            elif isinstance(comp, Force):
                dct["forces"].append((type(comp).__name__, comp.x, comp.mag, comp.angle_in_degrees))
            elif isinstance(comp, Moment):
                dct["moments"].append((type(comp).__name__, comp.x, comp.mag))

        file_name = simpledialog.askstring("Getting file name", "Please give file name")

        if file_name:
            with open(file_name + ".json", 'w') as json_file:
                json.dump(dct, json_file)

    def load_from_json(self, file_name = None):
        """
        Load from a json file, 
        if file_name is given use that file_name 
        else ask for file_name with Windows screen
        """
        if file_name is None:
            file_name = filedialog.askopenfilename(filetypes=[("JSON files", ".json")])

        try:
            with open(file_name) as json_file:
                dct = json.load(json_file)


                for subclass in dct:
                    for comp in dct[subclass]:
                        class_name, inputs= comp[0], comp[1:]
                        self.handle_component_input(globals()[class_name], inputs)
        except FileNotFoundError:
            self.load_from_json()

    def handle_mouse_pressed(self, pos, button):
        """Handle when mouse is pressed at the bottom demos"""
        for i in range(len(self.components)):
            if ui.point_in_rect(pos, (self.BOTTOM_DEMO_START_X + (self.BOTTOM_DEMO_START_X+DemoWithInfo.OUTLINE_WIDTH) * i, HEIGHT - 25, DemoWithInfo.OUTLINE_WIDTH, DemoWithInfo.OUTLINE_HEIGHT)):
                if button == 1:
                    self.remove_component(i)
                elif button == 3:
                    self.change_component(i)

   






    