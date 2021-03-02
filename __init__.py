import os, sys, math, pygame, PIL, PIL.Image
import pyhog.graphics as graphics
curmnu = None
const = {'github': "xXLarryTFVWXx"}

const['acc'] = 0.046875
const['dec'] = 0.5
const['frc'] = const['acc']
const['top'] = 6
const['slpfac'] = 0.125
const['slprlup'] = 0.078125
const['slprldn'] = 0.3125
const['fall'] = 2.5
const['air'] = 0.09375
const['jmp'] = 6.5
const['knxjmp'] = 6
const['grv'] = 0.21875

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

def PREP():
    pygame.mixer.pre_init(48001, -16)

def ON():
    pygame.init()
    pygame.mixer.init()
def OFF():
    pygame.quit()
class Window:
    def __init__(self, height, width, bgcolor="black", title="pyhog-engine"):
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
    def display(self):
        self.surf = pygame.display.set_mode((self.h, self.w))
        self.x, self.y, self.w, self.h = self.surf.get_rect()
        self.t = pygame.display.set_caption(self.title)
    def clear(self):
        self.surf.fill(self.bgcolor)
    def update(self):
        pygame.display.flip()
        pygame.event.clear()

def key_pressed(k=""):
    global kdict
    do_play = True
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if sum(keys) > 0:
        if k.lower() in kdict:
            return k == "" or bool(keys[kdict[k.lower()]])
    
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

class Character:
    def __init__(self, surf, xpos, yposimg="", bwidthr=9, bheightr=16, name="Sonic", images=[]):
        self.name = name
        self.xpos = 0
        self.ypos = 0
        self.xsp = 0
        self.ysp = 0
        self.gsp = 0
        self.slp = 0
        self.ang = (256-0)*1.40625
        self.bwr = bwidthr
        self.bhr = bheightr
        self.surf = surf
        self.fRight = True
        """This is to make sure that the character will fall when not on the ground"""
        self.jumping = True
        if self.name == "Knuckles":
            self.jmp = 6
        else:
            self.jmp = 6.5
        self.sprites = {"images": [graphics.load_image(img) for img in images]}
        self.sprites["rects"] = [img.get_rect() for img in self.sprites["images"]]
        self.sensors = self.get_sensors()
        self.curimg = self.sprites["images"][0]
        self.rect = self.sprite["rects"][0]
    def add_img(self, title, imgname):
            self.imgs[title].append(imgname)
    def get_sensors(self):
        self.sensors = {}
        self.sensors['ceil'] = self.sprites['rects'][0].centery-self.bhr
        self.sensors['wall'] = self.sprites['rects'][0].centery
        self.sensors['floor'] = self.sprites['rects'][0].centery+self.bhr
        self.sensors['left'] = self.sprites['rect'][0].centerx-self.bwr
        self.sensors['right'] = self.sprites['rect'][0].centerx+self.bwr
    def set_pos(self, x, y):
        self.curimg.center = (x,y)
        #temporary, this will have the code for the different characters in the game
    def get_collide(self):
        if abs(xsp) >= abs(ysp):
            self.sensact['ceil'] = {'left': True, 'right': True}
            self.sensact['floor'] = {'left': True, 'right': True}
            if xsp > 0:
                self.sensact['wall'] = {'left': True, 'right': True}
            else:
                self.sensact['wall'] = {'left': True, 'right': False}
        else:
            self.sensact['wall'] = {'left': True, 'right': True }
            if ysp > 0:
                self.sensact['floor'] = {'left': True, 'right': True}
                self.sensact['ceil'] = {'left': False, 'right': False}
            else:
                self.sensact['floor'] = {'left': False, 'right': False}
                self.sensact['ceil'] = {'left': True, 'right': True}
    def to_img(self, idx):
        self.curimg = self.sprites['images'][idx]
    def show(self):
        self.surf.blit(self.curimg, self.rect.topleft)
    def activate_sensors(self):
        
                
    def move(self, ang, kpressed={"dir":{"v":0,"h":0},"j":0,"k":0,"l":0}):
        global const
        if kpressed['dir']['h'] == 1:
            if self.gps < 0:
                self.gsp += const['acc']
                if self.gsp > 0:
                    self.gsp = 0.5
                elif self.gsp > top:
                    self.gsp = top
        elif kpressed['dir']['h'] == -1:
            if self.gps >0:
                self.gsp -= const['dec']
                if self.gsp < 0:
                    self.gsp = -0.5
                elif self.gsp < -top:
                    self.gsp = -top
        else:
            self.gsp = min(abs(self.gsp), const['frc']) * math.sin(self.gsp)
        
        self.xsp = self.gsp*math.cos(ang)
        self.ysp = self.gsp*(-math.sin(ang))
        if not self.jumping:
            if self.ysp < 0 and self.ysp > -4:
                if abs(self.xsp) >= 0.125:
                    self.xsp -= (self.xsp % 0.125 / 256)
            self.ysp += grv
        if self.ysp > 16:
            self.ysp = 16
        else:
            if kpressed['j']:
                self.ysp -= self.jmp
        return None
        
        
class Level:
    def __init__(self, surf, layout, zname="Testing", actnum=1, bgm=None, bg=None, x=0, y=0):
        self.layout = layout
        self.vec = pygame.math.Vector2()
        self.zname = zname
        self.actnum = actnum
        if not bgm == None:
            self.bgm = bgm
        self.surf = surf
        self.x = x
        self.y = y
        self.bg = bg
        self.started = False
        print(self.bgm)
        self.surfRect = self.surf.get_rect()
    def load(self):
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
        
        self.pygimg = graphics.load_image(self.layout)
        self.x, self.y, self.width, self.height = self.pygimg.get_rect()
        self.PILimg = PIL.Image.open(self.layout)
        self.collision = self.PILimg.getdata()
        self.PILimg.close()
        Hbtns = True
        curlvl = self
    def add_decor(self, image):
        self.decor = graphics.load_image(image)
        self.drect = self.decor.get_rect()
        self.drect.center = self.pygimg.center
    def scroll(self, ang, vel):
        self.vec.from_polar((vel,ang))
        self.x -= self.vec[0]
        self.y -= self.vec[1]
        if self.x > 0:
            self.x = 0
        elif self.x < -self.width+self.surfRect.width:
            self.x = -self.width+self.surfRect.width
        if self.y < -self.height+self.surfRect.height:
            self.y = -self.height+self.surfRect.height
            
    def start(self):
        global curlvl
        if pygame.mixer.get_busy() == 0:
            play_music()
        self.started = True
        curlvl = self
        print(curlvl.started)
    def draw(self):
        self.surf.blit(self.pygimg, (self.x, self.y))
    def unload(self):
        global Hbtns, curlvl
        Hbtns = False
        curlvl = None
    def stop(self):
        stop_music()
    

class Box:
    def __init__(self, surf, x, y, bgc, text=None, fgc="black", canHover=False, hfgc="white", hbgc="limegreen", canClick=False, function=None):
        self.surf = surf
        self.x = x
        self.y = y
        self.sbgc = pygame.Color(bgc)
        self.bgc = self.sbgc
        self.rect = pygame.rect.Rect(x,y,0,0)
        self.hovering = False
        self.cFrames = 0
        """Is there text present?"""
        if not text == None:
            self.text = text
            """Since there is text present, it is also safe to assume that there is a foreground color"""
            self.fgc = pygame.Color(fgc)
            self.sfgc = self.fgc
            self.font = pygame.font.SysFont("Noto Mono", 24)
        """Will this box respond to the mouse?"""
        if canHover:
            self.canHover = canHover
            """If it is true, then there must be a hover color"""
            self.hbgc = pygame.Color(hbgc)
            """This will check to see if there has been text assigned to this box"""
            if self.text:
                    self.hfgc = pygame.Color(hfgc)
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
        """This block makes sure that there is a function assigned to the box, before making it a button"""
        if canClick and not function == None:
            self.canClick = canClick
            self.function = function
    def hover(self):
        self.bgc = self.hbgc
        if self.text:
            self.fgc = self.hfgc
        self.hovering = True
    def unhover(self):
        self.bgc = self.sbgc
        if self.text:
            self.fgc = self.sfgc
        self.hovering = False
    def click(self):
        try:
            self.function()
        except AttributeError as ae:
            print(ae)
    def draw(self, mpos):
        if self.cFrames >= 1:
            self.cFrames -= 1
        elif self.cFrames < 0:
            self.cFrames = 0
            print("somehow the cFrames value went below 0")
            global dbgmsg
            dbgmsg = f"""If you see this message in your console, please contact me here github.com/{github}"""
        try:
            if self.text:
                if self.canHover:
                    mouseOver = pygame.rect.Rect(pygame.mouse.get_pos(), (1,1)).colliderect(self.rect)
                    if mouseOver and not self.hovering:
                        self.hover()
                    elif not mouseOver and self.hovering:
                        self.unhover()
                mclick = pygame.mouse.get_pressed(3)[0]
                if self.hovering and mclick and not self.cFrames:
                    self.click()
                    self.cFrames = 15
                elif self.hovering and mclick and self.cFrames:
                    print(f"please wait for {self.cFrames} frames to pass")
                r = self.font.render(self.text, 0, self.fgc)
                rRect = r.get_rect()
                self.rect = pygame.draw.rect(self.surf, self.bgc, (self.x-10, self.y-5, rRect.width+20, rRect.height+15))
                self.surf.blit(r, (self.x,self.y))
        except AttributeError as ae:
            print(ae)
            pygame.draw.rect(self.surf, self.bgc, (self.x, self.y, 128, 64))

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
def get_mouse_pos():
    return pygame.mouse.get_pos()
def get_click(buttonNum=1):
    return pygame.mouse.get_pressed(3)
