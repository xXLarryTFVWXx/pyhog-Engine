from typing import Any
import json
import pygame
from .events import *

states = {
    "current": None
}

def query() -> None | dict[str, Any]:
    return states.get(states.get("current", None), None)

def create(name: str, **information):
    states[name] = information
    print(states[name])

def set_state(name):
    states['current'] = name

def end():
    state = query()
    if state is not None:
        state['close']()

__all__ = ('query', 'create', 'set_state', 'end')