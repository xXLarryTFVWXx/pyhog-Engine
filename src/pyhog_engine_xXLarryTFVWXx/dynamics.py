import pygame
from pygame import sprite, key, math as game_math
from . import events, levels
from .game_input import *


air_friction = 1

class Actor(sprite.Sprite):
    """Inheriting from pygame-ce's Sprite class for auto handling of the thing"""
    def __init__(self, name, sprite_sheet, is_player=False, *groups: sprite.AbstractGroup[sprite._SpriteSupportsGroup]) -> None:
        super().__init__(self)
        self.image = pygame.Surface((32, 32)).convert_alpha() # type: ignore
        self.image.fill("cyan")
        self.name = name
        self.move = player_movement if is_player else robot_movement
        self.velocity = pygame.Vector2(0,0)
        self.position = pygame.Vector2(0,0)
        self.activate_flags()
        self.rect = pygame.Rect(0,0,7,14)
        self.colliders: list[pygame.Vector2]
        self.max_velocity = 6
        super().__init__(*groups)
    def activate_flags(self):
        self.control_mode = 0 # 0 - disabled, 1 - normal, 2 - mashing, 3 - pattern, 4 - single button press.
        self.is_balancing = False
    def update(self):
        self.move(self)

def collide(actor:Actor):
    floor_colliders, wall_colliders, ceiling_colliders = actor.colliders
    for collider in floor_colliders:
        if isinstance(levels.current, levels.Level):
            return sprite.collide_mask(levels.current, actor)
    return (0,0)

def robot_movement(actor:Actor):
    pass

def player_movement(actor:Actor):
    if get_pressed("right"):
        actor.velocity += game_math.Vector2(1)
    elif get_pressed("left"):
        actor.velocity -= game_math.Vector2(1)
    actor.velocity.clamp_magnitude(actor.max_velocity)
    collide(actor)
    return None


# Should we create a character by manually passing in each attribute
# Or should we load from a config file?
# If we do a config file should it be JSON, YAML, INI or Markup based?
def create_character(name, sprite_sheet) -> Actor:
    return Actor(name, sprite_sheet)

def create_player(name, sprite_sheet) -> Actor:
    return Actor(name, sprite_sheet, True)

__all__ = ["create_character"]