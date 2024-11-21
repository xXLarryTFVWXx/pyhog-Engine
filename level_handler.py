import ctypes, pygame
from . import graphics, audio, input, state
from .CONSTANTS import *

class Level:
    def __init__(self, name, act_number=1, x=0, y=0):
        self.surface = pygame.display.get_surface()
        self.name = name
        self.act_number = act_number
        state.create(f"level-{self.name}-{self.act_number}")
    def load(self):
        self.sprite_mask = pygame.mask.from_surface(graphics.load())
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
    def collide(self, caller:pygame.sprite.Sprite) -> tuple[str, int]:
        """
            This method uses a custom format using the 4 channels available
            Red Channel: Angle for Layer A
            Blue Channel: Angle for Layer B
            Green Channel: Used for Object Classification
            Alpha Channel: Used for Object Identifier
        """
        # check if the caller's sensors are overlapping
    def draw(self):
        if self.bgIMG:
            self.surf.blit(self.bgIMG, (self.x, 0))
        self.surf.blit(self.fgIMG, (self.x, self.y))

def create_level(name):
    state.create(f"level-{name}", level_name=name)


__all__ = [
    "create_level"
]