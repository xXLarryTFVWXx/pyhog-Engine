import ctypes, math, random, pygame
from .graphics import *
atkdur = 0

class Character(Spritesheet):
    def __init__(self, pos, surf, characterName, cells:dict={"stand": [0,0,64,64]}):
        super().__init__( f"Art/Characters/{characterName}/sheet.png", cells)
        self.surf = surf
        self.gsp = 0
        self.up = -90 # this is in degrees
        self.x = self.y = 20
        self.width = 7*2+1
        self.height = 9*2+1
        self.vec = pygame.Vector2((self.x, self.y))
        self.xvel = self.yvel = 0
        self.frc = self.acc = 0.046875
        self.layer = 0
        self.rect = pygame.Rect(self.vec, (self.width, self.height))
        self.ang = 0
        self.top = 6
    def update(self, drc: str):
        self.up = self.ang - 90
        if drc > 0:
            if self.gsp < 0:
                self.gsp += dec
                if self.gsp >= 0:
                    self.gsp = 0.5
            elif self.gsp > 0:
                self.gsp += acc
                if self.gsp > self.top:
                    self.gsp = self.top
        elif drc < 0:
            if self.gsp > 0:
                self.gsp -= dec
                if self.gsp <= 0:
                    gsp = -0.5
            elif self.gsp < 0:
                self.gsp -= acc
                if abs(self.gsp) > top:
                    self.gsp = -top
        else:
            self.gsp = min(abs(self.gsp), self.frc) * math.sin(self.gsp)
        self.vec.from_polar((self.gsp, self.ang))
        self.rect = pygame.Rect(*self.vec, self.width, self.height)
        if self.layer in (0,1):
            while curlvl["colA"][self.rect.bottom][self.rect.right][3] > 0:
                self.vec.from_polar((1, self.up))
                self.rect = pygame.Rect(*self.vec, self.width, self.height)
            else:
                while curlvl['colA'][self.rect.bottom][self.rect.left][3] > 0:
                    self.vec.from_polar((1, self.up))
                    self.rect = pygame.Rect(*self.vec, self.width, self.height)
        elif self.layer in (0,2):
            while curlvl["colB"][self.rect.bottom][self.rect.right][3] > 0:
                self.vec.from_polar((1, self.up))
                self.rect = pygame.Rect(*self.vec, self.width, self.height)
            else:
                while curlvl['colB'][self.rect.bottom][self.rect.left][3] > 0:
                    self.vec.from_polar()
                    self.rect = pygame.Rect(*self.vec, self.width, self.height)

class Boss(Character):
    def __init__(self, surf, name, cells, hits, spawn, behaviors=()):
        super().__init__(surf, name, cells)
        self.spawn = spawn
        self.htis = hits
        self.behaviors = behaviors
        self.atkdur = 256
        
    def update(self):
        global atkdur
        if len(behaviors) >= 2:            
            if self.atkdur == 0:
                targetPos = None
                atk = random.choice(behaviors).lower()
                if atk['name'] == "moveleft":
                    distance = self.vec.distance_to(pygame.Vector2(-150,self.y))
                elif atk['name'] == "moveright":
                    distance = self.vec.distance_to(pygame.Vector2(self.surf.width + 150, self.y))
                elif atk['name'] == "movedown":
                    self.targetPos = self.x, self.surf.height+150
                    distance = self.vec.distance_to(pygame.Vector2(self.x, self.surf.height+150))
                elif atk['name'] == "moveup":
                    distance = self.vec.distance_to(pygame.Vector2(self.x, -150))
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
                    atkdur = self.distance_to(pygame.Vector2(*targetPos)/6)
    # def fire(self, ang):
    
class Level:
    def __init__(self, surf, fg, colliders, name, act=1, bgm=None, bg=None, x=0, y=0):
        self.surf, self.fg, self.name, self.act, self.bgm, self.bg, self.x, self.y = surf, fg, naem, act, bgm, bg, x, yield
        self.colFiles = *colliders
    def load(self):
        self.collision = {"colA":[], "colB": []}
        if not len(self.colFiles) > 2
        for num, file in enumerate(self.colFiles):
            if num == 0:
                self.collision["colA"] = graphics.load_image(file)
            else:
                self.collision["colB"] = graphics.load_image(file)
    def unload(self):
        pygame.mixer.music.unload()
    def collide(self, caller)
        while self.collision[caller.layer].get_at(caller.pos)[3] == 255:
            caller.pos.from_polar(1, caller.up)