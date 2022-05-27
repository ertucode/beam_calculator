import pygame
import ui

from vars import WIDTH, FULLHEIGHT, HEIGHT
from vars import BEAM_LEFT, BEAM_RIGHT, BEAM_MID, BEAM_HEIGHT, BEAM_BOTTOM, BEAM_TOP, beam_length
from vars import UIX


from components import Component, Demo
from components.force import Force
from components.support import Support, FixedSupport, PinnedSupport, RollerSupport
from components.distributed_load import Distload
from components.moment import Moment
pygame.init()

class BeamCalculator:
    NOT_SOLVABLE_RECT = pygame.Rect(WIDTH/2-50,HEIGHT-50,100,20)
    NOT_SOLVABLE_FONT = pygame.font.SysFont(ui.mainfont,12)
    NOT_SOLVABLE_SURF = NOT_SOLVABLE_FONT.render("The system has no solution",True,(255,0,0))

    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, FULLHEIGHT))
        pygame.display.set_caption("Beam Calculator")
        self.objects = []
        self.solvable = True

        self.run = True

        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.objects.append(Force(5, 100000, 250, 11))
        self.objects.append(Moment(10, 100, 11))
        self.objects.append(Distload(1,10,10,100,"down",11))


    def draw(self):
        self.win.fill("white")

        ui.draw_rect_at_center(self.win,(173,216,230),BEAM_MID,BEAM_TOP,BEAM_RIGHT-BEAM_LEFT,BEAM_HEIGHT,0)
        ui.draw_rect_at_center(self.win,"black",BEAM_MID,BEAM_TOP,BEAM_RIGHT-BEAM_LEFT,BEAM_HEIGHT,1)

        ui.print_text(self.win,UIX,15,f"Beam length: {beam_length} m")

        if self.objects:
            ui.print_text(self.win, UIX, HEIGHT-45, u"Click to delete \u21e9", font="cambria")
            x = 20
            for i, obj in enumerate(self.objects):
                obj.draw(self.win)
                obj.draw_demo(self.win, (x + (x+Demo.OUTLINE_WIDTH) * i, HEIGHT - 25))

        if not self.solvable:
            self.win.blit(self.NOT_SOLVABLE_SURF, self.NOT_SOLVABLE_RECT)

        pygame.display.update()

    def mainloop(self):
        while self.run:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break

            self.draw()

b = BeamCalculator()
b.mainloop()