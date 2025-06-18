import os
from warnings import warn
import pygame
import pygame_gui as gui
from . import files

Window: pygame.Window
Manager: gui.UIManager


def genesis_to_color(color_data: bytes) -> pygame.Color:
    """
    pixel format: 0000 RRR0 GGG0 BBB0
    We ignore the first byte, which is removed in load_genesis_image_binary
    """
    print("{color start}")
    print([bin(color)[2:] for color in color_data])
    new_color = pygame.Color(
        (color_data[1] & 0b1110) / 0b1110 * 255,
        (color_data[1] >> 4) / 0b1110 * 255,
        (color_data[0]) / 0b1110 * 255,
    )
    return new_color

def color_to_genesis(color:tuple) -> bytes:
    red = int(color[0] / 255 * 0b1110)
    green = int(color[1] / 255 * 0b1110) << 4
    blue = int(color[2] / 255 * 0b1110)
    print(f"{color=}")
    print(f"{red=}{green=}{blue=}")
    result = f"{chr(blue)}{chr(red+green)}".encode("ISO 8859-1")
    print(result)
    return result


def load_genesis_palette(palette_source):
    with open(palette_source, 'rb') as source:
        raw_data = source.read()
    data = []
    for index in range(0, len(raw_data), 2): 
        data.append([raw_data[index], raw_data[index+1]])
    return [genesis_to_color(color) for color in data]

def load_genesis_image_binary(filename: str | bytes) -> list[pygame.Color]:
    with open(filename, "rb") as source:
        raw_data: list[bytes] = [b"0"]
    data: list[pygame.Color] = [genesis_to_color(color_data) for color_data in raw_data]

    if __debug__:
        from pprint import pprint

        pprint(data)
    return data


def load_image(filename) -> pygame.Surface:
    files.verify_path(filename)
    return pygame.image.load(filename).convert_alpha()


def make_window(title: str = "Pyhog-Engine", size: tuple[int, int] = (680, 420)):
    g = globals()
    g["Window"] = win = pygame.Window(title, size, pygame.WINDOWPOS_CENTERED)
    g["Manager"] = gui.UIManager(size)
    return win


def get_window():
    try:
        return Window
    except KeyError:
        warn(
            "Window was not created before attempting to access, default window created."
        )
        return make_window()


def get_manager():
    try:
        return Manager
    except NameError:
        warn(
            "UIManager was not created before attempting to access, default Manager created."
        )


def get_color(color):
    return pygame.Color(color)


def test_palette(palette_file):
    surface = pygame.Surface(
        (16, 4)
    )
    palette_data = load_genesis_palette(palette_file)
    for index, pixel_color in enumerate(palette_data):
        surface.set_at((index%16, int(index//16)), pixel_color)
    pygame.init()
    win = pygame.display.set_mode((16,4), pygame.FULLSCREEN|pygame.SCALED)
    print(len(palette_data))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
        win.blit(surface)
        pygame.display.flip()


__all__ = ["load_image", "make_window", "get_window", "get_color"]
