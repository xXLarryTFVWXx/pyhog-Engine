# pyright: ignore[reportUnusedImport]
# Why can't I just do the above line once at the top of the file and be done?
from pygame import ( 
    # keyboard map
    # WASD
    K_w as WASD_UP, # pyright: ignore[reportUnusedImport]
    K_a as WASD_DOWN, # pyright: ignore[reportUnusedImport]
    K_s as WASD_LEFT, # pyright: ignore[reportUnusedImport]
    K_d as WASD_RIGHT, # pyright: ignore[reportUnusedImport]
    K_SPACE as WASD_JUMP, # pyright: ignore[reportUnusedImport]
    K_RCTRL as KEY_ATTACK, # pyright: ignore[reportUnusedImport]
    K_RSHIFT as KEY_ENERGY, # pyright: ignore[reportUnusedImport]
    K_RALT as KEY_GROUND, # pyright: ignore[reportUnusedImport]
    K_RETURN as KEY_PAUSE, # pyright: ignore[reportUnusedImport]
    # ARROWS
    K_UP as ARR_UP, # pyright: ignore[reportUnusedImport]
    K_DOWN as ARR_DOWN, # pyright: ignore[reportUnusedImport]
    K_LEFT as ARR_LEFT, # pyright: ignore[reportUnusedImport]
    K_RIGHT as ARR_RIGHT, # pyright: ignore[reportUnusedImport]
    # controller map
    CONTROLLER_AXIS_LEFTX as MAIN_HORIZONTAL, # pyright: ignore[reportUnusedImport]
    CONTROLLER_AXIS_LEFTY as MAIN_VERTICAL, # pyright: ignore[reportUnusedImport]
    CONTROLLER_AXIS_RIGHTX as AUX_HORIZONTAL, # pyright: ignore[reportUnusedImport]
    CONTROLLER_AXIS_RIGHTY as AUX_VERTICAL, # pyright: ignore[reportUnusedImport]
    CONTROLLER_BUTTON_A as JOY_JUMP, # pyright: ignore[reportUnusedImport]
    CONTROLLER_BUTTON_X as JOY_ATTACK, # pyright: ignore[reportUnusedImport]
    CONTROLLER_BUTTON_Y as JOY_ENERGY, # pyright: ignore[reportUnusedImport]
    CONTROLLER_BUTTON_START as JOY_PAUSE, # pyright: ignore[reportUnusedImport]
    CONTROLLER_BUTTON_B as JOY_GROUND, # pyright: ignore[reportUnusedImport]
    # DEBUG mode controls
    K_ESCAPE as FORCE_QUIT, # pyright: ignore[reportUnusedImport]
    K_KP0 as VIEW_FPS, # pyright: ignore[reportUnusedImport]
    K_KP1 as VIEW_COLLISION, # pyright: ignore[reportUnusedImport]
    K_KP2 as VIEW_SENSORS, # pyright: ignore[reportUnusedImport]
    K_KP3 as PLACE_OBJECT, # pyright: ignore[reportUnusedImport]
    K_KP_ENTER as LEVEL_SAVE # pyright: ignore[reportUnusedImport]
) # These are the default controls
# NOTE: Pyright can be a pain in the butt more times than it is helpful
# But it is still helpful, so I don't think I can live without it...  Too Bad!