from typing import BinaryIO
from warnings import warn
import pygame

from .game_math import Vector2D
from . import files, type_definitions

Window: pygame.Window


class Background(type_definitions.Background):

    def __init__(
        self,
        source: BinaryIO | pygame.Color | type_definitions.typing.Sequence[int] | str | int,
        parent: pygame.Surface | None = None,
        position: Vector2D | None = None,
        scroll_data: type_definitions.ScrollContainer = {"direction": "None", "data": [type_definitions.NO_SCROLL]}
    ) -> None:
        super().__init__(source, parent)
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

__all__ = ["load_image", "make_window", "get_window", "get_color"]
