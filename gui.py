import ctypes, math, pygame
from . import files
from . import audio

menus = {
    "current": None
}

def get_mouse():
    return pygame.Rect(pygame.mouse.get_pos(), (1,1))
def get_click(button=0):
    buttons = pygame.mouse.get_pressed()
    if button == 0:
        return bool(sum(buttons))
    elif button in range(4):
        return bool(buttons[button-1])
    else:
        raise TypeError(f"expected for button to be between 0 and 2 got: {button}")

class Window:
    def __init__(self, height, width, bgcolor="black", title="pyhog-engine", fullscreen=False):
        self.h = height
        self.w = width
        if type(bgcolor) == str:
            self.bgcolor = pygame.Color(bgcolor)
        elif type(bgcolor) == tuple or type(bgcolor) == list:
            if not len(bgcolor) > 4 or not len(bgcolor) > 2:
                raise ValueError("The color is of the wrong size")
            else:
                self.bgcolor == bgcolor
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
    def __init__(self, surf, pos=[0,0], width=0, height=0, **kwargs):
        self.surf = surf
        self.pos = pos
        if 'size' in kwargs:
            self.size = list(kwargs["size"])
        else:
            self.size = [128, 64]
        if 'text' in kwargs:
            self.font = pygame.font.SysFont(pygame.font.get_default_font(), 28)
            self.text = kwargs['text']
            self.size = list(self.font.size(kwargs['text']))
            self.size[0] += 10
            self.size[1] += 10
            self.rect = pygame.Rect(self.pos, self.size)
            if not 'fgc' in kwargs:
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
        self.rect = pygame.Rect(self.pos, self.size)
        self.hovering = False
    def draw(self):
        if self.hover:
            self.hovering = get_mouse().colliderect(self.rect)
        if self.hovering:
            pygame.draw.rect(self.surf, self.hbgc, self.rect)
            if not self.text == None:
                label = self.font.render(self.text, True, self.hfgc)
                lRect = label.get_rect()
                lRect.center = self.rect.center
                self.surf.blit(label, lRect)
            if not self.function == None:
                if get_click(0):
                    self.function()
        else:
            pygame.draw.rect(self.surf, self.bgc, self.rect)
        if not self.text == None:
            label = self.font.render(self.text, True, self.fgc)
            lRect = label.get_rect()
            lRect.center = self.rect.center
            self.surf.blit(label, lRect)

class Menu:
    bformat =  """format for buttons
            Whether there are multiple buttons or not, just use a 2d matrix (e.g. [[BUTTON_OBJ]])
            
        """
    def __init__(self, name, mnu_id, bg="cyan", bgm=None, buttons=[[]]):

        self.btns = buttons
        if type(bg) == str:
            if not "." in bg:
                self.bgc = pygame.Color(bg)
            else:
                self.bgimg = bg
        elif type(bg) == tuple or type(bg) == list:
            self.bgc = bg
        if not bgm==None:
            self.bgm = bgm
        global menus, mnu
        self.mnu_ID = mnu_id
        new_id = ctypes.c_uint16(mnu_id)
        if not new_id.value in menus:
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
        
        
    
def openMenu(mnu_id):
    new_id = ctypes.c_uint16(mnu_id).value
    if new_id in menus:
        menus[new_id].open()