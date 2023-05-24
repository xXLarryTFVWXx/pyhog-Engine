import ctypes, math, pygame
from . import files
from . import audio
from . import input

menus = {
    "current": None
}

class Window:
    def __init__(self, height, width, bgcolor="black", title="pyhog-engine", fullscreen=False):
        self.h = height
        self.w = width
        if type(bgcolor) == str:
            self.bgcolor = pygame.Color(bgcolor)
        elif type(bgcolor) in [tuple, list]:
            if len(bgcolor) <= 4 or len(bgcolor) <= 2:
                raise ValueError("The color is of the wrong size")
            else:
                self.bgcolor = bgcolor
        self.title = title
        self.fullscreen = fullscreen
    def display(self):
        if not self.fullscreen:
            self.surf = pygame.display.set_mode((self.h, self.w))
        else:
            self.surf = pygame.display.set_mode((self.h, self.w), pygame.FULLSCREEN|pygame.SCALED)
            
        self.x, self.y, self.w, self.h = self.surf.get_rect()
        self.renderorigin = pygame.Vector2(self.w//2,self.h//2)
        self.t = pygame.display.set_caption(self.title)
    def clear(self):
        self.surf.fill(self.bgcolor)
    def update(self):
        pygame.display.flip()
        pygame.event.clear()

class Box:
    def __init__(self, surf, pos=None, width=0, height=0, **kwargs):
        if pos is None:
            pos = [0,0]
        self.surf = surf
        self.pos = [axis * 1.0 for axis in pos]
        self.size = list(kwargs["size"]) if 'size' in kwargs else [128, 64]
        if 'text' in kwargs:
            self.font = pygame.font.SysFont(pygame.font.get_default_font(), 28)
            self.text = kwargs['text']
            self.size = [size + 10.0 for size in self.font.size(self.text)]
            self.rect = pygame.Rect(self.pos, self.size)
            if 'fgc' not in kwargs:
                self.fgc = pygame.Color('black')

            else:
                self.fgc = pygame.Color(kwargs['color'])

        if 'bgc' in kwargs:
            self.bgc = pygame.Color(kwargs['bgc'])

        else:
            self.bgc = pygame.Color('red')
        self.hover = False

        if 'function' in kwargs:
            self.function = kwargs['function']
            if 'hover' in kwargs:
                self.hover = True
                if 'hfgc' in kwargs:
                    self.hfgc = pygame.Color(kwargs['hfgc'])
                else:
                    self.hfgc = pygame.Color('white')
                if 'hbgc' in kwargs:
                    self.hbgc = pygame.Color(kwargs['hbgc'])
                else:
                    self.hbgc = pygame.Color('green')
        else:
            self.function = None
        self.rect = pygame.Rect(self.pos, self.size) # type: ignore
        self.hovering = False
    def draw(self):
        if self.hover:
            self.hovering = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.hovering:
            pygame.draw.rect(self.surf, self.hbgc, self.rect)
            if self.text is not None:
                label = self.font.render(self.text, True, self.hfgc)
                lRect = label.get_rect()
                lRect.center = self.rect.center
                self.surf.blit(label, lRect)
            if get_click(0):
                if self.function is not None:
                    self.function()
        else:
            pygame.draw.rect(self.surf, self.bgc, self.rect)
        if self.text is not None:
            label = self.font.render(self.text, True, self.fgc)
            lRect = label.get_rect()
            lRect.center = self.rect.center
            self.surf.blit(label, lRect)

class Menu:
    bformat =  """format for buttons
            Whether there are multiple buttons or not, just use a 2d matrix (e.g. [[BUTTON_OBJ]])
            
        """
    def __init__(self, name, mnu_id, bg="cyan", bgm=None, buttons=None):

        if buttons is None:
            buttons = [[]]
        self.btns = buttons
        if type(bg) == str:
            if "." not in bg:
                self.bgc = pygame.Color(bg)
            else:
                self.bgimg = bg
        elif type(bg) in [tuple, list]:
            self.bgc = bg
        if bgm is not None:
            self.bgm = bgm
        global menus, mnu
        self.mnu_ID = mnu_id
        new_id = ctypes.c_uint16(mnu_id)
        if new_id.value not in menus:
            menus[new_id.value] = self
            
    def open(self):
        try:
            audio.load_music(self.bgm)
            if not audio.get_busy():
                audio.play_music()
        except AttributeError:
            print("there is no music")
        except Exception as e:
            print(e)
        menus['current'] = self
        files.set_state(0x00, self.mnu_ID)
