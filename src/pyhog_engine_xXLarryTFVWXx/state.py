from typing import Any, Optional, TypedDict
from . import events # pyright: ignore[reportUnusedImport]
from pygame import event as evt

event = evt


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
class Game_state(TypedDict):
    objects: list[object]
    transition: Optional[dict[str, Any]]
    next: Optional[str]


def set_state(new_state: str):
    states.update(
        active=states.get(
            new_state,
            Game_state({"next": None, "objects": [object()], "transition": None}),
        )
    )

states: dict[str, Game_state] = {}

def new(name: str, state_information: Game_state):
    states[name] = state_information


def get_active() -> Game_state:
    return states.get("active", NULL_STATE)


def step():
    next_state = states.get("active", NULL_STATE).get("next", NULL_STATE)
    if next_state is not None:
        states.update(active=states.get(next_state, NULL_STATE))



NULL_STATE: Game_state = {"objects": [], "next": None, "transition": None}
new("NULL_STATE", NULL_STATE)
zero_error_state: Game_state = {
    "objects": [object()],
    "next": "NULL_STATE",
    "transition": None,
}
new("ERR-ZDE", zero_error_state)
QUIT: Game_state = {"objects": [], "next": None, "transition": None}


__all__ = ["get_active", "step", "new", "set_state"]
