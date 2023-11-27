from typing import Any
import json
import pygame
from .events import *

states = {
    "current": None
}

def query():
    return states["current"]

def create(name: str, **information):
    states[name] = information

def set_state(name):
    states['current'] = states[name]

def end():
    state = query()
    if state is not None:
        state['close']()