"""
            If you are reading this, you are a code digger.
            Now, I want to congratulate you,
            but I can't, not without letting you in on secrets.

            Please just go back to enjoying the game,
            This has taken literal years of my starting, changing and giving up,
            I don't want to see my project ruined
            because someone wanted to either see the code and reveal secrets
            or make their own modded version of this game.

            Yes, I am well aware of the possibility that you might be making your own modded version of the game.
            Please hear me out on this, go ahead and make your own version of the game,
            I only ask you to not change the core features, go ahead and add your own.
            Small tweaks to the core features are fine, but something that can end up being overpowered isn't.
            Keep things balanced, if you find that something in the core game is overpowered,
            please contact me via github, or maybe tumblr if I get one
            If you do end up making your own modded version of this game, you may show your friends,
            but please don't redistribute it to the general public,
            I don't want this to go crazy and become something different than my vision.
            I literally just want to share this with you.

            If you do show this to your friends, please tell them it is an unauthorized mod of this game.
            I really don't want someone to think that someone's morrally wrong game is attributed to this game.
            Official mods may be a possibility in the future, but that is going to be a long ways off.
            Mostly because I have no clue how I can make a way to import information to my game securely.
            I might have an idea or two, but I want this game to be the best game it can be before I release this into the wilds.

            I have been literally writing *just* this comment for over an hour, pouring my heart on this subject out to you.
            
        """
import os, sys, math, functools, pygame
import pyhog.graphics as graphics
import pyhog.physics as physics
curmnu = None
github = "xxlarytfvwxx"

phi = (1/math.sqrt(5)) / 2
acc = 0.046875
dec = 0.5
frc = acc
top = 6
slpfac = 0.125
slprlup = 0.078125
slprldn = 0.3125
fall = 2.5
air = 0.09375
jmp = 6.5
knxjmp = 6
grv = 0.21875

Hbtns = False
curlvl = None

kdict = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "jump": pygame.K_j,
    "action": pygame.K_k,
    "boost": pygame.K_l,
    "esc": pygame.K_ESCAPE,
    "dbg": pygame.K_o
}

def ON():
    pygame.mixer.pre_init(48000, -16, channels=4)
    pygame.init()
    pygame.mixer.init()
def OFF():
    pygame.quit()
    
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

def key_pressed(k=""):
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if sum(keys) > 0:
        if k.lower() in kdict:
            return k == "" or bool(keys[kdict[k.lower()]])
def get_mouse_pos():
    return pygame.mouse.get_pos()

def load_Music(file):
    pygame.mixer_music.load(file)
def play_music(loop=0, t=0.0):
    pygame.mixer_music.play(loop)
def pause_music():
    pygame.mixer_music.pause()
def stop_music():
    pygame.mixer_music.stop()
def get_busy():
    return bool(pygame.mixer_music.get_busy())
def clock():
    return pygame.time.Clock()


class Spritesheet:
    def __init__(self, filename, cells:dict={"stand":[(0,0,64,64)]}):
        self.cells = cells
        self.filename = filename
        self.frame = 0
        self.cycle = 'stand'
        self.cycleTimer = 120
        self.x = self.y = 0
    def load(self):
        self.sheet = pygame.image.load(filename).convert_alpha()
    def changeCycle(self, cycle, cycleTimer):
        self.cycle = self.cells[cycle]
        self.cycleTimer = cycleTimer
    @functools.lru_cache(10)
    def nextFrame(self):
        if self.cycleTimer == 0:
            self.frame += 1
            if self.frame >= len(self.cells[self.cycle]):
                self.frame = 0
        self.cycleTimer -= 1
    def render(self):
        self.surf.blit(self.sheet, (self.x, self.y), self.cells[self.cycle][self.frame])
        self.nextFrame()
        


class Character(Spritesheet):
    def __init__(self, surf, characterName, cells:dict={"stand": [0,0,64,64]}):
        super().__init__( f"Art/Characters/{characterName}/sheet.png", cells)
        self.surf = surf
        self.gsp = 0
        self.up = -90 # this is in degrees
        self.x = self.y = 20
        self.vec = pygame.Vector2((self.x, self.y))
        self.xvel = self.yvel = 0
        self.layer = 0
        self.ang = 0
        self.top = top
    def update(self, drc: str):
        if drc > 0:
            if self.gsp < 0:
                self.gsp += dec
                if self.gsp >= 0:
                    self.gsp = 0.5
            elif self.gsp > 0:
                self.gsp += acc
                if self.gsp > self.top:
                    self.gsp = self.top
        elif drc < 0:
            if self.gsp > 0:
                self.gsp -= dec
                if self.gsp <= 0:
                    gsp = -0.5
            elif self.gsp < 0:
                self.gsp -= acc
                if abs(self.gsp) > top:
                    self.gsp = -top
        else:
            self.gsp = min(abs(self.gsp), frc) * math.sin(self.gsp)
                

class Level:
    def __init__(self, surf, layout, layerA, layerB, zname="Testing", actnum=1, bgm=None, bg=None, x=0, y=0):
        self.layout = layout
        self.vec = pygame.math.Vector2()
        self.zname = zname
        self.actnum = actnum
        self.bgm = bgm
        self.BG = bg
        self.surf = surf
        self.x = x
        self.y = -y
        self.bg = bg
        self.started = False
        self.layerA = layerA
        self.layerB = layerB
        print(self.bgm)
        self.surfRect = self.surf.get_rect()
    def load(self, characters=({}), enemies=({})):
        global Hbtns, curlvl
        if not self.bg == None:
            if type(self.bg) == str:
                if "." in self.bg:
                    self.bgimg = graphics.load_image(self.bg)
                else:
                    self.bgc = pygame.Color(self.bg)
            elif type(bg) == list or type(bg) == tuple:
                self.bgc = self.bg
        else:
            print("There is no backround")
        try:
            load_Music(self.bgm)
            print("music loaded")
        except AttributeError:
            print("There is no music to load")
        except pygame.error:
            if os.path.exists(self.bgm):
                print(f"The file {self.bgm} can not be recognised by pygame.")
            else:
                raise FileNotFoundError(f"the file {self.bgm} is not found.")
        
        self.FG = graphics.load_image(self.layout)
        self.rect = self.FG.get_rect()
        self.colA = graphics.load_image(self.layerA, False)
        if not self.layerB is None:
            self.colB = graphics.load_image(self.layerB, False)
        self.characters, self.enemies = characters, enemies
        
            
        self.start()
        curlvl = self
    def add_decor(self, image):
        self.decor = graphics.load_image(image)
        self.drect = self.decor.get_rect()
        self.drect.center = self.FG.get_rect()
    def switchLayer(self, character=("Enemy", "characterObject"), fromLayer=None, toLayer=None):
        if character == None or fromLayer == None or toLayer == None:
            raise TypeError("One or more arguments are None Character:{character} FromLayer:{FromLayer} toLayer:{toLayer}")
        else:
            if character[0].lower() == "enemy":
                self.enemies[fromLayer].remove(character[1])
                self.enemies[toLayer].append(character[1])
            elif character[0].lower() == "characters":
                self.characters[fromLayer].remove(character[1])
                self.characters[toLayer].append(character[1])
    def scroll(self, ang, vel):
        self.vec.from_polar((vel,ang))
        self.x -= self.vec[0]
        self.y -= self.vec[1]
        if self.x > 0:
            self.x = 0
        elif self.x < -self.rect.width+self.surfRect.width:
            self.x = -self.rect.width+self.surfRect.width
        if self.y < -self.rect.height+self.surfRect.height:
            self.y = -self.rect.height+self.surfRect.height
        
            
    def start(self):
        global curlvl, Hbtns
        if pygame.mixer.get_busy() == 0:
            play_music()
        self.started = True
        curlvl = self
        Hbtns = True
        print(curlvl.started)
    def draw(self):
        if not self.BG == None:
            self.surf.blit(self.bgimg, (0,0))
        for character in self.characters[2]:
            if self.renderorigin.distance_to(pygame.Vector2(character.rect.center)) <= 300:
                character.render()
        for enemy in self.enemies[2]:
            if self.renderorigin.distance_to(pygame.Vector2(enemy.rect.center)) <= 300:
                enemy.render()
        self.surf.blit(self.FG, (self.x, self.y))
        for enemy in self.enemies[1]:
            if self.renderorigin.distance_to(pygame.Vector2(enemy.rect.center)) <= 300:
                enemy.render()
        for character in self.characters[1]:
            if self.renderorigin.distance_to(pygame.Vector2(character.rect.center)) <= 300:
                character.render()
        for enemy in self.enemies[0]:
            if self.renderorigin.distance_to(pygame.Vector2(enemy.rect.center)) <= 300:
                enemy.render()
        for character in self.characters[0]:
            if self.renderorigin.distance_to(pygame.Vector2(character.rect.center)) <= 300:
                character.render()
        
    def unload(self):
        global Hbtns, curlvl
        Hbtns = False
        curlvl = None
    def stop(self):
        stop_music()
    

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
        
            
class sky_mod:
    def __init__(self, surf, img):
        self.img = graphics.load_image(img)
        self.surf = surf
    def draw(self):
        self.surf.blit(self.img, self.surf.get_rect())