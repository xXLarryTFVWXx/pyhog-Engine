import sys, pygame#, pyjoycon as pyjc

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
    if any(keys):
        return bool(keys[kdict[k.lower()]]) if k.lower() in kdict else False
"""
class JoyControllerSingle(pyjc.GyroTrackingJoyCon,pyjc.PythonicJoyCon):
    def update(self):
        if self.battery_level < 2:
            print("Battery is low")
"""


def get_click(button=0):
    buttons = pygame.mouse.get_pressed(5)
    if button not in range(4):
        raise ValueError(f"button must be in a range of 0 to 5 inclusive, currently {button=}")
    return bool(sum(buttons)) if button == 0 else bool(buttons[button-1])