from typing import BinaryIO
from warnings import warn
import pygame
import pygame_gui as gui

from pyhog_engine_xXLarryTFVWXx.game_math import Vector2D
from . import files, type_definitions

Window: pygame.Window
Manager: gui.UIManager


class Background(type_definitions.Background):

    def __init__(
        self,
        source: BinaryIO | pygame.Color | type_definitions.typing.Sequence[int] | str | int,
        parent: pygame.Surface | None = None,
        position: Vector2D | None = None,
        scroll_data: type_definitions.ScrollContainer = {"direction": "None", "data": [type_definitions.NO_SCROLL]}
    ) -> None:
        super().__init__(source, parent, position)
        self.scroll_data = scroll_data

    def scroll(self, dx: int = 0, dy: int = 0) -> None:
        if self.scroll_data["direction"].lower().strip() in ("None", ""):
            return
        if self.scroll_data["direction"].lower().strip() == "horizontal":
            self.position += pygame.Vector2(dx, 0)
            return
        if self.scroll_data["direction"].lower().strip() == "vertical":
            self.position += pygame.Vector2(0, dy)
            return

    def render(self) -> list[pygame.Rect]:
        if self.parent is None: # Should never hapen, but in case it does, blit to the screen directly
            try:
                self.parent = get_window().get_surface()
            except Exception:
                raise RuntimeError("OKay, no window was created, please try creating a window.")
        if self.scroll_data["direction"].lower().strip() in ("None", ""):
            return [pygame.Rect(self.position, self.area)]
        areas: list[pygame.Rect] = []
        if self.scroll_data["direction"].lower().strip() == "horizontal":
            vertical_offset = 0
            horizontal_offset = 0
            for scroll_section in self.scroll_data["data"]:
                if (
                    self.scroll_data["direction"].lower().strip() == "horizontal"
                    and vertical_offset >= self.area.y
                ) or (
                    self.scroll_data["direction"].lower().strip() == "vertical"
                    and horizontal_offset >= self.area.x
                ):
                    break
                if scroll_section["size"] < 1:
                    horizontal_overflow = pygame.math.clamp(
                        self.position.x
                        + (self.parent.width or get_window().get_surface().width)
                        - self.area.x,
                        0,
                        self.area.y,
                    )
                    vertical_overflow = pygame.math.clamp(
                        self.position.y + scroll_section["size"] - self.area.y,
                        0,
                        (self.parent.height or get_window().get_surface().height),
                    )
                    areas.append(
                        pygame.Rect(
                            self.position.x
                            + getattr(self.parent or Window.get_surface(), "x"),
                            vertical_offset,
                            getattr(self.parent or Window.get_surface(), "width")
                            - horizontal_overflow,
                            scroll_section["size"] - vertical_overflow,
                        )
                    )
                    if horizontal_overflow > 0:
                        areas.append(
                            pygame.Rect(
                                0,
                                vertical_offset,
                                horizontal_overflow,
                                scroll_section["size"],
                            )
                        )
                    if vertical_overflow > 0:
                        areas.append(
                            pygame.Rect(
                                horizontal_offset,
                                0,
                                scroll_section["size"],
                                vertical_overflow,
                            )
                        )
        return areas


def genesis_to_color(color_data: int) -> pygame.Color:
    """
    pixel format: BBB0 GGG0 RRR0
    We ignore the first nibble, which is removed in load_genesis_image_binary
    """
    print("{color start}")
    print([bin(color_data)[2:]])
    new_color = pygame.Color(
        (color_data & 0b1110) << 4,
        color_data & 0b1110_0000,
        (color_data & 0b1110_0000_0000) >> 4,
    )
    return new_color


def color_to_genesis(color: int | tuple[int, int, int] | pygame.Color) -> bytes:
    red = green = blue = 0
    if isinstance(color, int):
        red = int(color / 255 * 0b1110)
        green = int(color / 255 * 0b1110_0000)
        blue = int(color / 255 * 0b1110)
    elif isinstance(color, tuple):
        red = int(color[0] / 255 * 0b1110)
        green = int(color[1] / 255 * 0b1110_0000)
        blue = int(color[2] / 255 * 0b1110)
    elif isinstance(
        color, pygame.Color
    ):  # pyright: ignore[reportUnnecessaryIsInstance]
        red = int(color.r / 255 * 0b1110)
        green = int(color.g / 255 * 0b1110_0000)
        blue = int(color.b / 255 * 0b1110)
    print(f"{color=}")
    print(f"{red=}{green=}{blue=}")
    result = f"{chr(blue)}{chr(red+green)}".encode("ISO 8859-1")
    print(result)
    return result


def load_genesis_palette(palette_source: pygame.typing.FileLike):
    assert isinstance(palette_source, (str, bytes)), TypeError(
        "This muse be either a string or bytes object"
    )
    data: list[pygame.Color]
    with open(palette_source, "rb") as source:
        raw_data: bytes = source.read()
        color_word: int = 0
        data: list[pygame.Color] = []
        for index, raw_byte in enumerate(raw_data):
            color_word = raw_byte << (8 * (index + 1) & 1)
            if index & 1 == 1:
                data.append(genesis_to_color(color_word))
    return data


def load_genesis_image_binary(filename: str | bytes) -> list[pygame.Color]:
    with open(filename, "rb") as source:
        raw_data: bytes = source.read(4)
    data: list[pygame.Color] = [genesis_to_color(color_data) for color_data in raw_data]
    if __debug__:
        from pprint import pprint

        pprint(data)
    return data


def load_image(filename: str) -> pygame.Surface:
    files.verify_path(filename)
    return pygame.image.load(filename).convert_alpha()


def make_window(title: str = "Pyhog-Engine", size: tuple[int, int] = (680, 420)):
    g = globals()
    g["Window"] = win = pygame.Window(title, size, pygame.WINDOWPOS_CENTERED)
    # g["Manager"] = gui.UIManager(size) # Will not use this until I know for certain how to use pygame-gui
    return win


def get_window():
    try:
        return Window
    except KeyError:
        warn(
            "Window was not created before attempting to access, default window created."
        )
        return make_window()


def get_color(color: str):
    return pygame.Color(color)


def test_palette(palette_file: pygame.typing.FileLike):
    surface = pygame.Surface((16, 4))
    palette_data = load_genesis_palette(palette_file)
    for index, pixel_color in enumerate(palette_data):
        surface.set_at((index % 16, int(index // 16)), pixel_color)
    pygame.init()
    win = pygame.display.set_mode((16, 4), pygame.FULLSCREEN | pygame.SCALED)
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
