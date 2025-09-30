import pygame
from . import state, type_definitions

STATE_CHANGE_ID: int = pygame.event.custom_type()
ACTOR_DEATH_ID: int = pygame.event.custom_type()
HANDLER_INITIALIZE: int = pygame.event.custom_type()
ACTOR_INITIALIZE = 0



def process(active_actors: list[type_definitions.Character]):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.set_state("QUIT")
        if event.type == HANDLER_INITIALIZE:
            if len(active_actors) == 10:
                continue
            