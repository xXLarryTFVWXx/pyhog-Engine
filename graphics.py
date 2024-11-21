import os, functools, pygame
from . import variables

layers = [
    "background",
    "rear enemy",
    "rear player",
    "rear level",
    "front level",
    "front enemy",
    "front player"
]

PLACEHOLDER = pygame.sprite.Sprite()

render_updates = pygame.sprite.LayeredUpdates([PLACEHOLDER for _ in range(len(layers))])

class sky_mod:
    def __init__(self, art):
        self.surf = pygame.display.get_surface()
        self.art = art
        self.loaded = False
    def load(self):
        self.drawer = load_image(self.art)
        self.loaded = True
    def draw(self):
        self.surf.blit(self.drawer, (0,0))

class Spritesheet:
    def __init__(self, filename, cells:dict={"stand":[(0,0,64,64)]}):
        """Surface must be provided by the inheriting """
        self.cells = cells
        self.filename = filename
        self.frame = 0
        self.cycle = 'stand'
        self.cycleTimer = 120
        self.xpos = self.ypos = 0
    def load(self):
        self.sheet = pygame.image.load(self.filename).convert_alpha()
        self.loaded = True
    def changeCycle(self, cycle):
        self.cycle = self.cells[cycle]["frames"]
        self.cycleTimer = self.cells[cycle]["timer"]
    @functools.cache
    def nextFrame(self):
        if self.cycleTimer == 0:
            self.frame += 1
            self.frame %= len(self.cycle)
        self.cycleTimer -= 1
    def render(self):
        self.surf.blit(self.sheet, (self.position.x, self.position.y), self.cells[self.cycle][self.frame]) # type: ignore
        self.nextFrame()

imgext = ["png", "jpeg", "jpg", "jpe", "jfif", "bmp", "gif", "dip", "tiff", "tif", "heic"]

def set_display(size, fullscreen):
    variables.display = pygame.display.set_mode(size, 0 if not fullscreen else pygame.FULLSCREEN)

def load_image(filename=None, convert=True):
    if filename is None:
        raise TypeError("You forgot to supply a filename for the image")
    if "." not in filename[-4:-2]:
        raise NameError(f"file string {filename} is invalid. There must be a period in the file name")
    try:
        image = pygame.image.load(os.path.join(filename))
        if convert:
            image = image.convert_alpha()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Please ensure the file at {filename} exists") from e
    return image

def get_palette(image):
    return image.get_palette()