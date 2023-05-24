import sys, pygame, pyjoycon as pyjc

kdict = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "jump": pygame.K_j,
    "action": pygame.K_k,
    "boost": pygame.K_l,
    "esc": pygame.K_ESCAPE,
    "dbg": pygame.K_o,
    "rotate_left": pygame.K_LEFTBRACKET,
    "rotate_right": pygame.K_RIGHTBRACKET
}

def key_pressed(k=""):
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit() #Failsafe for win7x64py3.3
            pygame.quit()
            sys.exit()
    if sum(keys) > 0:
        if k.lower() in kdict:
            return k == "" or bool(keys[kdict[k.lower()]])

class JoyControllerSingle(pyjc.GyroTrackingJoyCon,pyjc.PythonicJoyCon):
    def update(self):
        if self.battery_level < 2:
            print("Battery is low")

def get_click(button=0, sprite=None):
    buttons = pygame.mouse.get_pressed(3)
    if button == 0:
        return bool(sum(buttons))
    elif button in range(4):
        return bool(buttons[button-1])
    else:
        raise TypeError(f"expected for button to be between 0 and 2 got: {button}")