import os
import json
from typing import Any
from uuid import UUID

from . import dynamics, files, type_definitions # pyright: ignore[reportUnusedImport]

BASE_PATH: str = (
    os.path.curdir
    if os.path.curdir.startswith(os.path.expanduser("~"))
    else os.path.expanduser("~")
)

required_game_data: list[UUID] = []


def load_game(game_name: str) -> Any:
    mod_path = os.path.join(BASE_PATH, "games", game_name.lower())
    assert (
        files.verify_path(mod_path) == True
    ), "Trying to access folder outside of allowed location."

    try:
        with open(f"{mod_path}/manifest.json") as manifest_file:
            raw_game_data: type_definitions.GameDataManifest = json.load(manifest_file)
            for required_uuid in raw_game_data["metadata"]["extends"] + list(
                raw_game_data["metadata"]["uses"].keys()
            ):
                if not (required_uuid.int in required_game_data):
                    required_game_data.append(required_uuid)
            for using_uuid in raw_game_data["metadata"]["uses"]:
                if not using_uuid.int in required_game_data:
                    required_game_data.append(using_uuid)

    except FileNotFoundError:
        raise RuntimeError("Fatal Error occured.")
