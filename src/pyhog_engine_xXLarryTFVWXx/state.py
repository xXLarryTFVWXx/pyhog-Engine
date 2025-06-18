from typing import Any, Optional, TypedDict
from . import events
from pygame import event as evt

event = evt

class Game_state(TypedDict):
    objects: list
    transition: Optional[dict[str, Any]]
    next: Optional[str]

null_state: Game_state = {
    "objects": []
}

states: dict[Game_state]
"""
    states follow the format
    "[state_name]": {
        "objects": [],
        "transition": {
            "in": [transition],
            "out": [transition]
        }
    }
    except the "active" state which has an additional "name": [state_name]

    [state_name] is the internal name of the state.
    [next] - Optional - The state to follow it.
    [transition] - a valid transition or None for use when entering or exiting the state.

    [state_name] can have one of the following valid prefixes:
        ERR - for when the game runs into an error that it can't recover from
        LVL - for the level states where the player has input.
        CUT - for cutscenes.
        MNU - for menus within the game.

    [state_name] has a few special names for the ERR prefix:
        ZDE - Zero Division Error - You tried to divide by zero?
        # TODO: get variable names from the traceback.
"""


def set_state(new_state: str):
    states.update(active=states.get(new_state))


def new(name, **kwargs):
    states.update((name, kwargs))


def get_active() -> dict[str, Any]:
    return states.get("active", {"name": None})


def step():
    next_state = states.get("active", {"name": None, "next": None}).get("next")
    if next_state is not None:
        states.update(active=states.get(next_state, {"name": None}))


__all__ = ["get_active", "step", "new", "set_state"]
