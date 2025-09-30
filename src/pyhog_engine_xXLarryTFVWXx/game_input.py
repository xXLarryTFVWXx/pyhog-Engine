# pyright: ignore[reportUnknownVariableType]
from pygame import (
    key as key_input,
    mouse,  # pyright: ignore[reportUnusedImport]
)
from .type_definitions import *
from .constants import *
from . import default_map

input_enabled: bool = False

controls: ControlContainer = {
    "method": "WASD",
    "ARROWS": {
        "attack": default_map.KEY_ATTACK,
        "energy": default_map.KEY_ENERGY,
        "ground": default_map.KEY_GROUND,
        "jump": default_map.WASD_LEFT,
        "movement": {
            "up": default_map.ARR_UP,
            "left": default_map.ARR_LEFT,
            "down": default_map.ARR_DOWN,
            "right": default_map.ARR_RIGHT
        },
    },
    "WASD": {
        "attack": default_map.KEY_ATTACK,
        "energy": default_map.KEY_ENERGY,
        "ground": default_map.KEY_GROUND,
        "jump": default_map.WASD_JUMP,
        "movement": {
            "up": default_map.WASD_UP,
            "left": default_map.WASD_LEFT,
            "down": default_map.WASD_DOWN,
            "right": default_map.WASD_RIGHT,
        }
    },
    "CONTROLLER": {
        "attack": default_map.JOY_ATTACK,
        "energy": default_map.JOY_ENERGY,
        "ground": default_map.JOY_GROUND,
        "jump": default_map.JOY_JUMP,
        "movement": {
            "horizontal": default_map.MAIN_HORIZONTAL,
            "vertical": default_map.MAIN_VERTICAL
        }
    },
    "DEBUG": {
        "fps": default_map.VIEW_FPS,
        "level": default_map.VIEW_COLLISION,
        "actors": default_map.VIEW_COLLISION,
        "placer": default_map.PLACE_OBJECT,
        "save": default_map.LEVEL_SAVE,
        "quit": default_map.FORCE_QUIT
    }
}


def get_key_pressed(key: str = "", method: CONTROLLER_METHODS = "WASD") -> bool:
    keys: key_input.ScancodeWrapper = key_input.get_pressed()
    any_down: bool = len(keys) > 1

    if not any_down:
        return False
    # something is held down
    if key == "": # Just looking for a button press?
        return True

    # I don't know if this is hacky or not.
    for key_name, key_code in controls[method].items():
        if isinstance(key_code, int):
            if keys[key_code] and key.lower() == key_name:
                return True
            continue
        if isinstance(key_code, dict):
            for move_key, move_code in key_code.items(): # pyright: ignore[reportUnknownVariableType]
                if keys[move_code] and key.lower() == move_key:
                    return True
    return False


__all__ = ["get_key_pressed"]
