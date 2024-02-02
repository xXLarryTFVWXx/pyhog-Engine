from pygame import display, image, Surface

from pygame import surface


def load_image(filename):
    return image.load(filename)

def make_window(width:int = 600, height: int = 600, fullscreen: int = 0%2) -> Surface:
    return display.set_mode((width, height))