import pygame
from components.support import FixedSupport, PinnedSupport, RollerSupport
from components.force import Force
from components.distributed_load import Distload
from components.moment import Moment


class QuestionAsker:
    def __init__(self,):
        self.button_map = {  pygame.K_F1: FixedSupport
                            ,pygame.K_F2: PinnedSupport
                            ,pygame.K_F3: RollerSupport
                            ,pygame.K_F4: Force
                            ,pygame.K_F5: Distload
                            ,pygame.K_F6: Moment}

    def handle_key_inputs(self, key):
        if key in self.button_map:
            return self.button_map[key]