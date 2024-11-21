from typing import Any
import json
import pygame
from .events import *

states = {
    "current": None
}

DEBUG_STATE = {
    "name": "debug",
    "close": lambda: None,
    "on_open": lambda: pygame.event.post()
}

def query() -> None | dict[str, Any]:
    return states.get(states.get("current", None), None)

def create(name: str, **information):
    states[name] = information
    print(states[name])

def queue(name:str):
    states.update(next_state=name)

def set_state(name):
    states['current'] = name
    pygame.event.post

def end():
    state = query()
    if state is not None:
        state['close']()

__all__ = ('query', 'create', 'set_state', 'end')