import os, sys, ctypes, math, json, pygame
from re import S
from . import state, files, audio, input, variables, errors

menus = {}

def display_is_ready():
    return variables.display is not None

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
    def __init__(self, config_file: None | str=None, pos: pygame.Vector2 = None, width=0, height=0, **kwargs):
        if type(config_file) == str and config_file[-4:].lower() == 'json':
            if os.path.isfile(config_file):
                self.config_file = config_file
                self.is_ready = False
                self.config = object()
                return
        self.position = pos if pos else pygame.Vector2(0, 0)
        self.surface: pygame.Surface = variables.display
        self.size = list(kwargs["size"]) if 'size' in kwargs else [128, 64]
        self.rect = pygame.Rect(self.pos, self.size)
        if 'text' in kwargs:
            self.font = pygame.font.SysFont(pygame.font.get_default_font(), 28)
            self.text = kwargs['text']
            self.size = [size + 10.0 for size in self.font.size(self.text)]
            self.base_text_color = pygame.Color(kwargs.get('fgc', 'black'))
            self.center_text = False
        self.base_background_color = pygame.Color(kwargs.get('bgc', 'red'))
        self.can_click = 'function' in kwargs
        self.function = kwargs.get('function', None)
        self.hover = kwargs.get('can_hover', False)
        if 'hover' in kwargs:
            self.hover_text_color = pygame.Color(kwargs.get('hfgc', 'white'))
            self.hover_background_color = pygame.Color(kwargs.get('hbgc', 'green'))
        self.hovering = False
    def load(self):
        try:
            with open(self.config_file, mode="r") as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            sys.exit(errors.FILE_DELETED_WHILE_OPEN)

    def update(self):
        if not self.is_ready:
            self.load()
        if self.surf is None:
            self.surf = variables.display if display_is_ready() else None
            return
        self.hovering = self.rect.collidepoint(pygame.mouse.get_pos())
        self.clicked = self.can_click and pygame.event.peek(pygame.MOUSEBUTTONUP, False)
        self.bgc = self.hover_background_color if self.hovering else self.base_background_color
        self.fgc = self.hover_text_color if self.hovering else self.base_text_color
    def draw(self):
        pygame.draw.rect(self.surf, self.bgc, self.rect)
        if self.text is not None:
            label = self.font.render(self.text, True, self.fgc)
            lRect = label.get_rect()
            self.surf.blit(label, lRect)
        self.function() if self.clicked else None

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
        self.background = pygame.Color(bg) if type(bg) == str and "." not in bg else bg if type(bg) in [tuple, list] else bg
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
        state.create(f"menu-{self.name}", buttons=self.buttons)
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
        state.set_state(f"menu-{self.name}")
    def draw(self):
        for row in self.buttons:
            for button in row:
                button.draw()

def create_menu(name, bg="cyan", bgm=None, buttons=None):
    menus.update({name: Menu(pygame.display.get_surface(), name, bg, bgm, buttons)})

def open_menu(menu_number: ctypes.c_uint8):
    menus[menu_number].open()