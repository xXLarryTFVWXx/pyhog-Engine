import os
import json
from typing import Any
from . import dynamics, files

BASE_PATH: str = os.path.curdir if os.path.curdir.startswith(os.path.expanduser("~")) else os.path.expanduser("~")


def load_mod(mod_name:str) -> Any:
    mod_path = os.path.join(BASE_PATH, "mods", mod_name.lower())
    assert files.verify_path(mod_path) == True, "Trying to access folder outside of allowed location."
    
    try:
        with open(f"{mod_path}/manifest.json") as manifest_file:
            manifest = json.load(manifest_file)
    except FileNotFoundError:
        if mod_name.lower() == "base":
            raise RuntimeError("FatalERROR has occured!  Base game config files not found!")