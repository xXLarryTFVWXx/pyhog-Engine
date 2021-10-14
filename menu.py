import math

class Box:
    def __init__(self, surf, pos=[0,0], width=0, height=0, **kwargs):
        self.surf = surf
        self.pos = pos
        if 'size' in kwargs:
            self.size = list(size)
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
            print(self.function)
            if 'hover' in kwargs:
                print('We can hover')
                self.hover = True
                if 'hfgc' in kwargs:
                    self.hfgc = pygame.Color(kwargs['hfgc'])
                else:
                    self.hfgc = pygame.Color('white')
                    print("Hover foreground color set")
                if 'hbgc' in kwargs:
                    self.hbgc = pygame.Color(kwargs['hbgc'])
                else:
                    self.hbgc = pygame.Color('green')
                    print("Hover background color set")
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
                    print("clicked")
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
    def __init__(self, name, bg="cyan", bgm=None, buttons=[[]]):

        self.btns = buttons
        if type(bg) == str:
            if not "." in bg:
                self.bgc = pygame.Color(bg)
            else:
                self.bgimg = bg
        elif type(bg) == tuple or type(bg) == list:
            self.bgc = bgc
        if not bgm==None:
            self.bgm = bgm
    def open(self):
        global curmnu
        try:
            load_Music(self.bgm)
            if not get_busy():
                play_music()
        except AttributeError:
            print("there is no music")
        curmnu = self