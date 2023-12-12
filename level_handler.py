import ctypes, pygame
from . import graphics, audio, input, state
from .CONSTANTS import *

class Level:
    def __init__(self, surf, fg, colliders, name, lvl_id=1, bgm=None, bg=None, x=0, y=0):
        self.surf, self.fg, self.colFiles, self.name, self.lvl_id, self.bgm, self.bg, self.x, self.y = surf, fg, colliders, name, ctypes.c_int8(lvl_id).value, bgm, bg, x, y
        state.create(f"level-{self.name}-{self.lvl_id}")
    def load(self):
        self.collision = {}
        if len(self.colFiles) != 2:
            raise NotImplementedError("I have yet to code in support for anything but 2 layers.")
        for num, file in enumerate(self.colFiles):
            self.collision[num] = graphics.load_image(file)
        self.bgIMG = graphics.load_image(self.bg) if self.bg else None
        if self.bgm:
            audio.load_music(self.bgm)
        self.pixel = (0,0,0,0)
        self.fgIMG = graphics.load_image(self.fg)
        self.start()
    def start(self):
        global curlvl
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
    def collide(self, caller) -> tuple[str, int]:
        """
            This method uses a custom format using the 4 channels available
            Red Channel: Angle for Layer A
            Blue Channel: Angle for Layer B
            Green Channel: Used for Object Classification
            Alpha Channel: Used for Object Identifier
        """
        collision_layer = (
            self.collision[caller.layer]
            if caller.layer != 0
            else self.collision[0]
        )
        caller_pos = pygame.Vector2(int(caller.position.x), int(caller.position.y))
        air_detector_base = pygame.Vector2(caller_pos) + pygame.Vector2(0,1).rotate(caller.angle)
        self.pixel = collision_layer.get_at([int(axis) for axis in caller_pos.xy])
        air_detector = int(air_detector_base[0]), int(air_detector_base[1])
        air_pixel = collision_layer.get_at(air_detector)
        at_surface = air_pixel == BLANK
        grounded = self.pixel != BLANK
        location = "underground" if grounded and not at_surface else "on surface" if at_surface and grounded else "in air"
        return (location, self.pixel[3])
    def draw(self):
        if self.bgIMG:
            self.surf.blit(self.bgIMG, (self.x, 0))
        self.surf.blit(self.fgIMG, (self.x, self.y))

def create_level(name):
    state.create(f"level-{name}", level_name=name)


curlvl: Level