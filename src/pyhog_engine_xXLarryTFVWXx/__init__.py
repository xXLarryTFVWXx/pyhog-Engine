"""This is a rewrite of the library without the use of AI due to potential copyright and license concerns."""

import os, sys
import pygame
if not hasattr(pygame, "IS_CE"):
    raise ImportError("Wrong edition of pygame installed, please install pygame-ce.")

from .state import *
from .files import *

def main_loop():
    surface = pygame.display.get_surface()
    while True:
        active_state = get_active()
        state_name: str = active_state.get("name")
        match state_name[:state_name.index('-')]:
            case _:
                state.set_state("DBG-invalid-state")
        if active_state.get("name") == "QUIT":
            handle_IO("None", "Test", "{'Player': 'None'}")