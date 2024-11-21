import os, math, random, functools, pygame, json
from numpy import sign

from .game_time import *
from . import graphics, audio, files, variables, level_handler, events, state
from .CONSTANTS import *
from . import level_handler
from .game_time import get_delta_time

BASE_CONFIG_PATH = "config"

atkdur = 0

class Character(pygame.sprite.Sprite):
    def __init__(self, characterName):
        self._layer = graphics.layers.index("front player")
        super().__init__()
        self.name = characterName
        self.surface = pygame.display.get_surface()
        self.config = {}
        self.config_path = os.path.abspath(os.path.join(BASE_CONFIG_PATH, f"characters/{self.name}.json"))
        self.surf = pygame.display.get_surface()
        self.forward_velocity = 0
        self.up = -90 # this is in degrees
        self.position = pygame.Vector2(20)
        self.rect = pygame.Rect(self.position, (7, 9))
        self.coll_anchor = pygame.Vector2(self.rect.center)
        self.angle = 0
        self.load_config()
        self.setup_flags()
        self.player_control = True

    def load_config(self):
        self.hits = 1
        with open(self.config_path, mode="r") as config_file: 
            self.config = json.load(config_file)
    def load_art(self):
        self.sheet = graphics.load_image(f"Art/Character/{self.name}.png")

    def setup_flags(self):
        self.invulnerable: bool = False
        self.loaded = False
        self.top_speed_override = False
        self.grounded = False
        self.is_ball = False
        self.active_sensors = 0b000000
        self.location = "in air"

    def _update_sensors(self):
        # bits are 0: front_ceiling, 1: left_wall, 2: right_wall, 3: back_ceiling, 4: back_wall, 5: front_floor, 6: back_floor
        self.active_sensors = 0b000000
        self.sensor_positions = [
            self.position + pygame.Vector2(getattr(self.config, "width_radius", 7), 0).rotate(self.angle),
            self.position + pygame.Vector2(getattr(self.config, "width_radius", 7), 0).rotate(self.angle),
            self.position + pygame.Vector2(getattr(self.config, "width_radius", 7), 0).rotate(self.angle),
            self.position + pygame.Vector2(getattr(self.config, "width_radius", 7), 0).rotate(self.angle),
            self.position + pygame.Vector2(getattr(self.config, "width_radius", 7), 0).rotate(self.angle),
            self.position + pygame.Vector2(getattr(self.config, "width_radius", 7), 0).rotate(self.angle)
        ]

    
    def load_into_level(self, level_name):
        self.position = state.query().get("position", pygame.Vector2(20))
        self.loaded = True

    
    def change_velocity(self, direction_held:int):
        delta_time = pygame.time.Clock().get_time()
        prior_velocity_sign = sign(self.forward_velocity)
        if direction_held == 0:
            self.forward_velocity -= min(abs(self.forward_velocity), GROUND_FRICTION) * math.sin(self.forward_velocity) * delta_time
        else:
            if not self.top_speed_override:
                self.forward_velocity += self.config.get("acceleration", ACCELERATION) * direction_held if prior_velocity_sign == 1 else GROUND_FRICTION * direction_held
                new_forward_velocity_sign = sign(self.forward_velocity)
                self.forward_velocity = 0.5 * direction_held if new_forward_velocity_sign != prior_velocity_sign else self.forward_velocity
            else:
                self.forward_velocity *= 1.02
        if not self.top_speed_override:
            self.forward_velocity = pygame.math.clamp(self.forward_velocity, -self.config.get("top speed", 6), self.config.get("top speed", 6))
        self.x_velocity, self.y_velocity = pygame.Vector2(self.forward_velocity, 0).rotate(self.angle)
        self._update_sensors()


    def update(self, direction_held: int):
        """
        Updates the state of the object based on the given direction_held and delta time.
        Only handles input if this has the player tag.
        Args:
            direction_held (int): The direction_held of movement -1 for left, 1 for right and 0 for none.

        Returns:
            None
        """
        if not self.loaded:
            self.load()
        self.delta_time = get_delta_time()
        self.change_velocity(direction_held) if self.player_control else ...
        self.activate_sensors()
        self.move()
        self.process_collision()
        self.up = self.angle - 90
        self.location, self.angle_pre_equation = level_handler.curlvl.collide(self)
        self.angle = (
            math.floor((256-self.angle_pre_equation)*GENESIS_TO_MODERN) % 360
            if not self.angle_pre_equation == 255
            else round(self.angle / 90) % 4 * 90) % 360 # this should ensure
        # Should I do this?  It doesn't call self.surf.flip so it should be alright.
        self.render()

    def process_collision(self):
        location, self.angle_pre_equation = level_handler.curlvl.collide(self)
        self.top_speed_override = location.lower() == "underground"
        self.grounded = location.lower() == "on surface"

    def move(self):
        self.position += pygame.Vector2(self.forward_velocity*self.direction_held, 0)
        self.rect = pygame.Rect(self.position.xy, (10, 10))
        self.rect.center = (int(self.position.x), int(self.position.y))
        self.process_collision()
        self.top_speed_override = self.location == "underground"
        self.grounded = self.location == "on surface"
        if not self.grounded or self.top_speed_override:
            self.y_velocity += GRAVITY
            self.y_velocity = pygame.math.clamp(self.y_velocity, -16, self.config.get("top speed", 6))
            self.yvel = min(self.yvel, self.config.get("top speed", 6))
            self.position += pygame.Vector2(0, self.yvel)
        else:
            self.yvel = 0
    def hurt(self):
        if not self.invulnerable: self.hits -= 1
        if self.hits == 0: pygame.event.post(pygame.event.Event(events.PLAYER_DEATH))
    def load(self):
        self.load_art()
        self.loaded = True

    def render(self):
        self.surface.blit(self.surf, self.rect)

def make_projectile(starting_position, angle, velocity, hurt_player=True):
    variables.projectiles.append({
        "position": starting_position,
        "angle": angle,
        "velocity": velocity,
        "hurts player": hurt_player
    })

def make_character(name):
    return Character(name)

__all__ = [
    "make_character",
    "make_projectile"
]