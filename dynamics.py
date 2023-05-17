import ctypes, math, random, functools, pygame
from . import graphics, audio, files, variables

curlvl = None
atkdur = 0
grv = 0.25
BLANK = (0,0,0,0)

class Character(graphics.Spritesheet):
    def __init__(self, surf, characterName, cells:dict={"stand": [0,0,64,64]}, pos=()):
        super().__init__(f"Art/Characters/{characterName}/sheet.png", cells)
        self.surf = surf
        self.gsp = 0
        self.up = -90 # this is in degrees
        self.pos = pygame.Vector2(20)
        self.xvel = self.yvel = 0
        self.frc = self.acc = 0.046875
        self.layer = 0
        self.rect = pygame.Rect(self.pos, (7, 9))
        self.coll_anchor = pygame.Vector2(self.rect.center)
        self.ang = 0
        self.top = 6
        self.acc = 0.046875
        self.dec = 0.5
        self.frc = self.acc
        self.height_radius = 19
        self.width_radius = 9
        self.loaded = False
        self.grounded = False
        self.is_ball = False
        self.active_sensors = [True for _ in range(6)]
        self.location = "in air"
    def activate_sensors(self):
        self.active_sensors = [True for _ in range(6)]
        if self.gsp > 0:
            self.active_sensors[4] = False
        elif self.gsp < 0:
            self.active_sensors[5] = False
        if self.grounded:
            self.active_sensors[2:2] = [False, False]
        else:
            if self.yvel > 0:
                self.active_sensors[2:4] = [False, False]
            else:
                self.active_sensors[0:2] = [False, False]

        
    def update(self, drc: int):
        if not self.loaded:
            self.load()
        self.up = self.ang - 90
        if drc > 0:
            if self.gsp <= 0:
                self.gsp += self.dec
                if self.gsp >= 0:
                    self.gsp = 0.5
            elif self.gsp >= 0:
                self.gsp += self.acc
                if self.gsp > self.top:
                    self.gsp = self.top
        elif drc < 0:
            if self.gsp >= 0:
                self.gsp -= self.dec
                if self.gsp <= 0:
                    self.gsp = -0.5
            elif self.gsp <= 0:
                self.gsp -= self.acc
                if abs(self.gsp) > self.top:
                    self.gsp = -self.top
        else:
            self.gsp -= min(abs(self.gsp), self.frc) * math.sin(self.gsp)
        """Change Radii depending if we are in a ball or not"""
        self.height_radius = 7 if self.is_ball else 19
        self.width_radius = 14 if self.is_ball else 9
        self.activate_sensors()
        self.pos += pygame.Vector2(self.gsp, 0).rotate(self.ang)
        self.up = self.ang - 90
        self.rect = pygame.Rect(*self.pos, 10, 10)
        self.rect.center = tuple(int(axis) for axis in self.pos)
        self.location, angle_pre_equation = curlvl.collide(self)
        self.ang = (256-angle_pre_equation)*1.40625
        while self.location == "underground":
            self.pos += pygame.Vector2(1,0).rotate(self.up)
            self.location, angle_pre_equation = curlvl.collide(self)
        else:
            self.grounded = self.location == "on surface"
            if not self.grounded:
                self.yvel += grv
                if self.yvel > self.top:
                    self.yvel = self.top
                self.pos += pygame.Vector2(0, self.yvel)
        self.render()
class Boss(Character):
    def __init__(self, surf, name, cells, hits, spawn, behaviors=()):
        super().__init__(surf, name, cells)
        self.spawn = spawn
        self.htis = hits
        self.behaviors = behaviors
        self.atkdur = 256
        
    def update(self):
        global atkdur
        if len(self.behaviors) >= 2:            
            if self.atkdur == 0:
                targetPos = None
                atk = random.choice(self.behaviors).lower()
                if atk['name'] == "moveleft":
                    distance = self.pos.distance_to(pygame.Vector2(-150,self.y))
                elif atk['name'] == "moveright":
                    distance = self.pos.distance_to(pygame.Vector2(self.surf.width + 150, self.y))
                elif atk['name'] == "movedown":
                    self.targetPos = self.x, self.surf.height+150
                    distance = self.pos.distance_to(pygame.Vector2(self.x, self.surf.height+150))
                elif atk['name'] == "moveup":
                    distance = self.pos.distance_to(pygame.Vector2(self.x, -150))
                elif atk['name'] == "hover":
                    atkdur = 120
                elif atk['name'] == "fireleft":
                    self.fire(180)
                    atkdur = 180
                elif atk['name'] == "fireright":
                    self.fire()
                    atkdur = 180
                elif atk['name'] == "firedown":
                    self.fire(90)
                    atkdur = 180
                elif atk['name'] == "fireup":
                    self.fire(-90)
                    atkdur = 180
                elif atk['name'] == "fireto":
                    self.fire(pygame)
                if not targetPos == None:
                    atkdur = self.pos.distance_to(pygame.Vector2(*targetPos)/6)
    def fire(self, target):
        """This will eventually create an object"""
        if type(target) == int:
            """Create the projectile and send it in that direction"""
            ...
        elif type(target) == Character:
            """Create the projectile and send it in the direction of the target."""
            ...

    
class Level:
    def __init__(self, surf, fg, colliders, name, lvl_id=1, bgm=None, bg=None, x=0, y=0):
        self.surf, self.fg, self.colFiles, self.name, self.lvl_id, self.bgm, self.bg, self.x, self.y = surf, fg, colliders, name, ctypes.c_int8(lvl_id).value, bgm, bg, x, y
    def load(self):
        self.collision = {}
        if len(self.colFiles) == 2:
            for num, file in enumerate(self.colFiles):
                self.collision[num] = graphics.load_image(file)
        else:
            raise NotImplementedError("I have yet to code in support for anything but 2 layers.")
        if self.bg:
            self.bgIMG = graphics.load_image(self.bg)
        else:
            self.bgIMG = None
        if self.bgm:
            audio.load_music(self.bgm)
        self.pixel = (0,0,0,0)
        self.fgIMG = graphics.load_image(self.fg)
        self.start()
    def start(self):
        global curlvl
        files.set_state(1, self.lvl_id)
        if audio.get_busy():
            audio.stop_music()
        if self.bgm:
            audio.play_music(-1)
        self.started = True
        curlvl = self
    def unload(self):
        """This only for sure unloads the music right now, I am currently working on code to "unload" everything else that is created in the load method"""
        pygame.mixer.music.unload()
        self.started = False
        del self.fgIMG, self.pixel, self.bgIMG, self.collision
    def collide(self, caller):
        if not caller.layer == 0:
            collision_layer = self.collision[caller.layer]
        else:
            collision_layer = self.collision[0]
        caller_pos = int(caller.pos.x), int(caller.pos.y)
        air_detector_base = pygame.Vector2(caller_pos) + pygame.Vector2(0,1).rotate(caller.up)
        self.pixel = collision_layer.get_at(caller_pos)
        air_detector = int(air_detector_base[0]), int(air_detector_base[1])
        air_pixel = collision_layer.get_at(air_detector)
        at_surface = air_pixel == BLANK
        grounded = not self.pixel == BLANK
        location = "underground" if grounded and not at_surface else "on surface" if at_surface and grounded else "in air"
        return (location, self.pixel[3])
    def draw(self):
        if self.bgIMG:
            self.surf.blit(self.bgIMG, (self.x, 0))
        self.surf.blit(self.fgIMG, (self.x, self.y))