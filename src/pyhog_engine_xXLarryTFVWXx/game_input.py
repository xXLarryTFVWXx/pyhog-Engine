import pygame
from pygame import key as key_input, joystick, mouse
from . import events

controls = {
    "method": "WASD",
    "WASD": {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d,
        "jump": pygame.K_j,
        "attack": pygame.K_k,
        "boost": pygame.K_l,
        "stomp": pygame.K_m,
    },
    "ARROWS": {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "jump": pygame.K_s,
        "attack": pygame.K_d,
        "boost": pygame.K_f,
        "stomp": pygame.K_v,
    }
}

if __debug__:
    controls["DEBUG"] = {"quit": pygame.K_ESCAPE, "fps": pygame.K_KP1}


def get_pressed(key: str = "") -> bool:
    keys = key_input.get_pressed()
    any_down = False
    try:
        any_down = keys.index(True) >= 0
    except ValueError:
        return False

    if not any_down:
        return False

    if __debug__:
        for key_name, scancode in controls["DEBUG"].items:
            if keys[scancode]:
                return True
    if keys in controls.keys():
        for key_name, scancode in controls[controls.get("method", "WASD")]:
            if keys[scancode]:
                return True

    return False

__all__ = ["get_pressed"]