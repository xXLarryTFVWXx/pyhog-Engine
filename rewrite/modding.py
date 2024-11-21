import os
from typing import Any
from . import dynamics

BASE_PATH: str = os.path.curdir if os.path.curdir.startswith(os.path.expanduser("~")) else os.path.expanduser("~")

def verify_location(path:str) -> bool:
    return path.startswith() # type: ignore The method supports a string but type checker is fussing.

def load_mod(mod_name:str) -> Any:
    assert verify_location(os.path.join(BASE_PATH, "mods", mod_name.lower())) == True, "Trying to access folder outside of scope."

    return None