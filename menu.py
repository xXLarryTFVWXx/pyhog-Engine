import math
import pygame
from . import audio, input, __helpers
from .gui import *

menus = {"current": None}

surface: Window
class Menu:
    bformat =  """format for buttons
            Whether there are multiple buttons or not, just use a 2d matrix (e.g. [[BUTTON_OBJ]])
            
        """
    def __init__(self, surface, name, bg="cyan", bgm=None, buttons=None):

        if buttons is None:
            buttons = [Box(surface, (20,20), 10, 10, text="Hi!")]
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
    def open(self):
        global curmnu
        try:
            audio.load_music(self.bgm)
            if not audio.get_busy():
                audio.play_music()
        except AttributeError:
            print("there is no music")
        curmnu = self
    def render(self):
        for button in self.btns:
            button.draw()

def openMenu(mnu_id):
    new_id = ctypes.c_uint16(mnu_id).value
    if new_id in menus:
        menus[new_id].open()