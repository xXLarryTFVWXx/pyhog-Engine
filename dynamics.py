import ctypes, math, random, functools, pygame, json
from numpy import sign
from . import graphics, audio, files, variables, level_handler, events, state
from .CONSTANTS import *
from . import level_handler

BASE_CONFIG_PATH = "config/Characters"

atkdur = 0
grv = 0.25

class Character(graphics.Spritesheet):
    def __init__(self, surf, characterName, cells:None|dict[str, list[list[int]]]=None, pos:pygame.Vector2=pygame.Vector2(20)):
        """
            cells format:
            {
                "name": [pygame.Rect, ...]
            }
        """
        self.name = characterName
        super().__init__(f"Art/Characters/{self.name}/sheet.png", cells)
        """If someone can collapse this code to improve readability please do."""
        self.config = {}
        self.config_path = f"{BASE_CONFIG_PATH}/{self.name}-config.json"
        self.load_config()
        self.surf = surf
        self.forward_velocity = 0
        self.up = -90 # this is in degrees
        self.layer = 0
        self.position = pygame.Vector2(20)
        self.rect = pygame.Rect(self.position, (7, 9))
        self.coll_anchor = pygame.Vector2(self.rect.center)
        self.angle = 0
        self.setup_flags()

    def load_config(self):
        with open(self.config_path, mode="r") as config_file: 
            self.config = json.load(config_file)
            
    def setup_flags(self):
        self.invulnerable: bool = False
        self.loaded = False
        self.top_speed_override = False
        self.grounded = False
        self.is_ball = False
        self.active_sensors = [True for _ in range(6)]
        self.location = "in air"

    def activate_sensors(self):
        # bits are 0: front_ceiling, 1: left_wall, 2: right_wall, 3: back_ceiling, 4: front_floor, 5: back_floor
        self.active_sensors = 0b000000
        

    
    def load_into_level(self, level_name):
        self.position = level_handler.get_level_by_name(level_name).get("position", pygame.Vector2(20))
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


    def update(self, direction_held: int):
        """
        Updates the state of the object based on the given direction_held and delta time.
        Only handles input if this has the player tag.
        Args:
            direction_held (int): The direction_held of movement (-1, 0, or 1).
            delta_time (float): The time elapsed since the last update.

        Returns:
            None
        """
        if not self.loaded:
            self.load()
        self.change_velocity(direction_held)
        self.activate_sensors()
        self.move()
        self.up = self.angle - 90
        self.location, self.angle_pre_equation = level_handler.curlvl.collide(self)
        self.angle = math.floor((256-self.angle_pre_equation)*GENESIS_TO_MODERN) % 360 # this should ensure
        # Should I do this?  It doesn't call self.surf.flip so it should be alright.
        self.render()

    def process_collision(self):
        self.location, self.angle_pre_equation = level_handler.curlvl.collide(self)

    def move(self):
        self.position += pygame.Vector2(self.forward_velocity*self.direction_held, 0)
        self.rect = pygame.Rect(self.position.xy, (10, 10))
        self.rect.center = (int(self.position.x), int(self.position.y))
        self.top_speed_override = self.location == "underground"
        self.grounded = self.location == "on surface"
        if not self.grounded:
            self.y_velocity += grv
            self.y_velocity = pygame.math.clamp(self.y_velocity, -16, self.config.get("top speed", 6))
            self.yvel = min(self.yvel, self.config.get("top speed", 6))
            self.position += pygame.Vector2(0, self.yvel)
        else:
            self.yvel = 0
    def hurt(self):
        if not self.invulnerable:
            self.hits -= 1
        if self.hits == 0:
            pygame.event.post(pygame.event.Event(events.PLAYER_DEATH))

def make_projectile(starting_position, angle, velocity, hurt_player=True):
    variables.projectiles.append({
        "position": starting_position,
        "angle": angle,
        "velocity": velocity,
        "hurts player": hurt_player
    })