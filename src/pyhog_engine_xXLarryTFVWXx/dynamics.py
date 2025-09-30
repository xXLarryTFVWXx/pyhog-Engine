import json # pyright: ignore[reportUnusedImport]
from pygame import math as game_math
from .game_math import hex_to_degrees
from . import levels, graphics, files # pyright: ignore[reportUnusedImport]
from .game_input import *
from .type_definitions import *


air_friction = 1

actors: dict[str, Character] = {}

class Actor(Character):


    def __init__(self, filename:str):
        files.verify_path(filename, "asset")
        self.move = player_movement if self.is_player else robot_movement
        self.collide = player_collide if self.is_player else robot_collide
        self.control_method = KeyboardControls


    def hurt(self):
        self.health -= 1

    def update(self):
        self.move(self)


enemies: list[Actor]


def robot_movement(actor: Actor):
    return NotImplemented


def robot_collide(actor: Actor):
    return NotImplemented


def player_collide(player: Actor):
    colliding_enemy: Actor | None = player.collision_box.collideobjects(enemies)
    if colliding_enemy is not None:
        _ = 1 + 1
        # TODO: implement section [PVE collision]

    for collider in (
        player.collision_box.bottomright,
        player.collision_box.bottomleft,
        (player.collision_box.centerx, player.collision_box.bottom),
    ):
        chunk: ChunkCollision = levels.current.collision_data[
            int(collider[0] // 128 + collider[1] // 128 * levels.current.level_size.x)
        ]
        if chunk == EMPTY_CHUNK:
            break
        tile: TileCollision = chunk[COLLISION_LAYERS[player.collision_layer]][
            collider[0] % 16 + (collider[1] % 16) * 16
        ]
        if tile == EMPTY_TILE:
            break
        player.angle = int(hex_to_degrees(tile["angle"]))


def player_movement(actor: Actor):
    if get_key_pressed("right"):
        actor.velocity += game_math.Vector2D(1)
    elif get_key_pressed("left"):
        actor.velocity -= game_math.Vector2D(1)
    actor.velocity.clamp_magnitude(actor.top_speed)
    return None


# Should we create a character by manually passing in each attribute
# Or should we load from a config file?
# If we do a config file should it be JSON, YAML, INI or Markup based?
def new_character(name:str):
    Actor(name)


__all__ = ["new_character"]

