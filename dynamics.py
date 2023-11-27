import ctypes, math, random, functools, pygame, json
from numpy import sign
from . import graphics, audio, files, variables, level_handler, events
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
        super().__init__(f"Art/Characters/{self.name}/sheet.png", cells) # type: ignore Temporarily ignoring type to get rid of red squiggly
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
        # modify active_sensors based on x_velocity and y_velocity which are from
    def load_config(self):
        with open(self.config_path, mode="r") as config_file: 
            self.config = json.load(config_file)
    
    def load_into_level(self):
        self.position = pygame.Vector2(20)
        self.loaded = True
    
    def change_velocity(self, drc:int, delta_time:float):
        if drc == 0:
            self.forward_velocity -= min(abs(self.forward_velocity), GROUND_FRICTION) * math.sin(self.forward_velocity) * delta_time
        else:
            prior_velocity_sign = sign(self.forward_velocity)
            if not self.top_speed_override:
                self.forward_velocity += self.config.get("acceleration", ACCELERATION) * drc if prior_velocity_sign == 1 else GROUND_FRICTION * drc
                new_forward_velocity_sign = sign(self.forward_velocity)
                self.forward_velocity = 0.5 * drc if new_forward_velocity_sign != prior_velocity_sign else self.forward_velocity
            else:
                self.forward_velocity *= 1.02
        if self.top_speed_override:
            self.forward_velocity = pygame.math.clamp(self.forward_velocity, -self.config.get("top speed", 6), self.config.get("top speed", 6))
        self.x_velocity, self.y_velocity = pygame.Vector2(self.forward_velocity, 0).rotate(self.angle)


    def update(self, drc: int, delta_time:float):
        """
        Updates the state of the object based on the given direction and delta time.

        Args:
            drc (int): The direction of movement (-1, 0, or 1).
            delta_time (float): The time elapsed since the last update.

        Returns:
            None
        """
        if not self.loaded:
            self.load()
        self.up = self.angle - 90
        self.change_velocity()
        self.activate_sensors()
        self.rect = pygame.Rect(self.position.xy, (10, 10))
        self.rect.center = (int(self.position.x), int(self.position.y))
        self.up = self.angle - 90
        self.location, angle_pre_equation = level_handler.curlvl.collide(self)
        # Magic conversion number do not touch
        self.angle = pygame.math.clamp((256-angle_pre_equation)*GENESIS_TO_MODERN, 0, 359)
        # TODO: Instead of practically teleporting to the top of whatever surface you are on,
        # Keep adding velocity to self until we are out of the wall.
        self.process_collision()
        if self.location == "underground":
            self.position += pygame.Vector2(-self.forward_velocity*drc, 0)
            self.location, angle_pre_equation = level_handler.curlvl.collide(self) # type: ignore
            self.top_speed_override = True
        else:
            self.top_speed_override = False
            self.grounded = self.location == "on surface"
            if not self.grounded:
                self.yvel += grv
                self.yvel = min(self.yvel, self.config.get("top speed", 6))
                self.position += pygame.Vector2(0, self.yvel)
            else:
                self.yvel = 0
        # Should I do this?  It doesn't call self.surf.flip so it should be alright.
        self.render()
    def process_collision(self):
        self.level_collision = level_handler.curlvl.collide(self)
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
class Boss(Character):
    def __init__(self, surf, name, cells, spawn, hits=8, behaviors=(), on_destruct = None): # added default hits value, on_destruct is unused.
        super().__init__(surf, name, cells)
        self.spawn = spawn
        self.hits = hits # TYPO fixed.
        self.behaviors = behaviors
        self.atkdur = 256
    def update(self):
        global atkdur
        if len(self.behaviors) >= 2:
            if self.atkdur == 0:
                targetPos = None
                atk = random.choice(self.behaviors).lower()
                if atk['name'] == "moveleft":
                    distance = self.position.distance_to(pygame.Vector2(-150,self.y))
                elif atk['name'] == "moveright":
                    distance = self.position.distance_to(pygame.Vector2(self.surf.width + 150, self.y))
                elif atk['name'] == "movedown":
                    self.targetPos = self.x, self.surf.height+150
                    distance = self.position.distance_to(pygame.Vector2(self.x, self.surf.height+150))
                elif atk['name'] == "moveup":
                    distance = self.position.distance_to(pygame.Vector2(self.x, -150))
                elif atk['name'] == "hover":
                    atkdur = 120
                elif atk['name'] == "fireleft":
                    self.fire(180)
                    atkdur = 180
                elif atk['name'] == "fireright":
                    self.fire(0)
                    atkdur = 180
                elif atk['name'] == "firedown":
                    self.fire(90)
                    atkdur = 180
                elif atk['name'] == "fireup":
                    self.fire(-90)
                    atkdur = 180
                elif atk['name'] == "fireto":
                    self.fire(variables.character) # type: ignore
                # if not targetPos == None:
                #     atkdur = self.position.distance_to(pygame.Vector2(*targetPos)/6) # Still figuring out how long this should take.
                
    def fire(self, target: Character | float | int=0):
        """This will eventually create an object"""
        if not isinstance(target, (Character, float, int)):
            raise TypeError("Target of Boss must be either an int or a Character.")
        position = self.position
        angle = 0
        attack_speed = 60
        if isinstance(target, Character):
            angle = self.position.angle_to(target.position)
            """Create the projectile and send it in the direction of the target."""
        if isinstance(target, float):
            angle = int(target)
        
        make_projectile(self.position, angle, attack_speed)
        

    
