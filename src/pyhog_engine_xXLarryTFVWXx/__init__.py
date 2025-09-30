"""This is a rewrite of the library without the use of AI due to potential copyright and license concerns."""

import json
import os, sys  # pyright: ignore[reportUnusedImport]
import pygame

if not hasattr(pygame, "IS_CE"):
    raise ImportError("Wrong edition of pygame installed, please install pygame-ce.")

from .state import *
from .files import *
from .events import *
from . import graphics

def preload(game_location: str):
    os.chdir(game_location)
    with open("manifest.json", "r") as manifest_file:
        manifest: type_definitions.GameDataManifest = json.load(manifest_file)
    targeted_engine_version = manifest["metadata"]["game_version"]
    match verify_version(targeted_engine_version): # pyright: ignore[reportMatchNotExhaustive]
        case False:
            raise RuntimeError(f"game's engine version {'.'.join((str(item) for item in targeted_engine_version))} is incompatible with engine's current version {'.'.join((str(item) for item in ENGINE_VERSION))}")



def on():
    pygame.init()
    graphics.Window = pygame.Window("Test", position=pygame.WINDOWPOS_CENTERED)


def off():
    pygame.quit()
    del graphics.Window
