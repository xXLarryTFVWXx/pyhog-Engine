import os, sys, ctypes, math, json, pygame, pygame_gui
from re import S

from . import state, files, audio, input, variables, errors, game_time, graphics
quit_confirm = False

menus = {}

manager: pygame_gui.UIManager | None = None

class Menu:
    bformat =  """format for buttons
            Whether there are multiple buttons or not, just use a 2d matrix (e.g. [[BUTTON_OBJ]])
            
        """
    def __init__(self, name, bg="cyan", bgm=None, buttons=None):
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
        self.buttons = buttons
        self.background = pygame.Color(bg) if type(bg) == str and "." not in bg else bg if type(bg) in [tuple, list] else bg
        menu_number = len(menus.keys())
        print(menu_number)
        menus.update({menu_number: self})
        state.create(f"menu-{self.name}", buttons=self.buttons)
    def load(self):
        if "." in self.background:
            self.background = graphics.load_image(self.background)
    def open(self):
        self.surface = pygame.surface.Surface(pygame.display.get_window_size())
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
        assert manager is not None, "gui manager isn't set."
        display_surface = pygame.display.get_surface()
        if not isinstance(self.background, pygame.Surface):
            pygame.draw.rect(display_surface, self.background)
        manager.draw_ui(display_surface)
        display_surface.blit(self.surface)


def update():
    assert manager is not None, "gui manager has not been initialized, please set the mode of the window then call init_manager"
    manager.update(game_time.get_delta_time())

def create_button(position, text, background_color, text_color):
    assert manager is not None, "gui manager has not been initialized, please set the mode of the window then call init_manager"
    pygame_gui.elements.UIButton(position, text, manager, text_kwargs={"color": text_color})

def create_menu(name, bg="cyan", bgm=None, buttons=None):
    menus.update({name: Menu(pygame.display.get_surface(), name, bg, bgm, buttons)})

def open_menu(menu_name: str):
    state.set_state(f"menu-{menu_name}")

def display_is_ready():
    return variables.display is not None

def init_manager():
    if pygame.display.get_active():
        globals().update(manager=pygame_gui.UIManager(pygame.display.get_window_size()))
    else:
        raise NameError("Display is not active")


__all__ = [
    "create_button",
    "update",
    "create_menu",
    "open_menu",
    "display_is_ready",
    "init_manager"
]
