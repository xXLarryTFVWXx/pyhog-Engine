import os, functools, pygame
class Spritesheet:
    def __init__(self, filename, cells:dict={"stand":[(0,0,64,64)]}):
        """Surface must be provided by the inheriting """
        self.cells = cells
        self.filename = filename
        self.frame = 0
        self.cycle = 'stand'
        self.cycleTimer = 120
        self.x = self.y = 0
    def load(self):
        self.sheet = pygame.image.load(self.filename).convert_alpha()
        self.loaded = True
    def changeCycle(self, cycle, cycleTimer):
        self.cycle = self.cells[cycle]
        self.cycleTimer = cycleTimer
    @functools.cache
    def nextFrame(self):
        if self.cycleTimer == 0:
            self.frame += 1
            if self.frame >= len(self.cells[self.cycle]):
                self.frame = 0
        self.cycleTimer -= 1
    def render(self):
        self.surf.blit(self.sheet, (self.pos.x, self.pos.y), self.cells[self.cycle][self.frame])
        self.nextFrame()

imgext = ["png", "jpeg", "jpg", "jpe", "jfif", "bmp", "gif", "dip", "tiff", "tif", "heic"]

def load_image(filename=None, convert=True):
    if filename is None:
        raise TypeError("You forgot to supply a filename for the image")
    if "." not in filename[-4:-2]:
        raise NameError(f"file string {filename} is invalid. There must be a period in the file name")
    try:
        image = pygame.image.load(os.path.join(filename))
        if convert:
            image = image.convert_alpha()
    except FileNotFoundError:
        raise FileNotFoundError(f"Please ensure the file at {filename} exists")
    return image

def get_palette(image):
    return image.get_palette()

class sky_mod:
    def __init__(self, surf, art):
        self.surf = surf
        self.art = art
        self.loaded = False
    def load(self):
        self.drawer = load_image(self.art)
        self.loaded = True
    def draw(self):
        self.surf.blit(self.drawer, (0,0))