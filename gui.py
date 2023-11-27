import ctypes, math, pygame

from . import state, files, audio, input

menus = {}

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
            self.base_text_color = self.fgc

        if 'bgc' in kwargs:
            self.bgc = pygame.Color(kwargs['bgc'])

        else:
            self.bgc = pygame.Color('red')
        self.base_background_color = self.bgc
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
            self.bgc = self.hbgc
            self.fgc = self.hfgc
        else:
            self.bgc = self.base_background_color
            self.fgc = self.base_text_color
        pygame.draw.rect(self.surf, self.hbgc, self.rect)
        if self.text is not None:
            label = self.font.render(self.text, True, self.fgc)
            lRect = label.get_rect()
            lRect.center = self.rect.center
            self.surf.blit(label, lRect)
        if input.get_click(0) and self.function is not None:
            self.function()

class Menu:
    bformat =  """format for buttons
            Whether there are multiple buttons or not, just use a 2d matrix (e.g. [[BUTTON_OBJ]])
            
        """
    def __init__(self, surface, name, bg="cyan", bgm=None, buttons=None):
        """
        Initializes a Menu instance.

        Args:
            surface (object): The surface object.
            name (str): The name of the menu.
            mnu_id (int): The menu ID.
            bg (str or tuple or list, optional): The background color or image filepath. Defaults to "cyan".
            bgm (object, optional): The background music filepath. Defaults to None.
            buttons (list, optional): The list of buttons. Defaults to None.
        """
        self.name = name
        if buttons is None:
            buttons = [[Box(surface, (20,20), 10, 10, text="Hi!")]]
        self.buttons = buttons
        if type(bg) == str:
            if "." not in bg:
                self.bgc = pygame.Color(bg)
            else:
                self.bgimg = bg
        elif type(bg) in [tuple, list]:
            self.bgc = bg
        if bgm is not None:
            self.bgm = bgm
        menu_number = len(menus.keys())
        print(menu_number)
        menus.update({menu_number: self})
        state.create("menu", menu_name=f"menu-"+self.name)
    def open(self):
        try:
            audio.load_music(self.bgm)
            if not audio.get_busy():
                audio.play_music()
        except AttributeError:
            print("there is no music")
        except Exception as e:
            print(e)
        menus.update({"current": self})
        state.set_state(self.name)
    def render(self):
        for row in self.buttons:
            for button in row:
                button.draw()


def open_menu(menu_number: ctypes.c_uint8):
    menus[menu_number].open()