import pygame


PAUSE_GAME = pygame.event.Event(pygame.event.custom_type())
STATE_OF_LOADING = pygame.event.Event(pygame.event.custom_type())
NEXT_STATE = pygame.event.Event(pygame.event.custom_type())
PAUSE_GAME = pygame.event.Event(pygame.event.custom_type())
PLAYER_INVULNERABLE_EXPIRE = pygame.event.Event(pygame.event.custom_type())
PLAYER_DEATH = pygame.event.Event(pygame.event.custom_type())

DEBUG_STATE_EVENT = pygame.event.Event(pygame.event.custom_type(), {"objects": [
    {"Text": "Welcome to Secret!", "position": (20, 20), "color": (255, 0, 0), "size": 20, "font": "Arial"},
]})


def verify_event(event):
    match type(event):
        case pygame.event.Event:
            return True
        case _:
            raise TypeError(f"Although pygame{'-ce' if getattr(pygame, 'IS_CE', False) else ''} allows events as ints, I don't")

