import os
from typing import TypedDict
from pygame import Rect, surface, sprite
from pygame.math import clamp, Vector2
from pygame.display import get_surface as get_display
from . import graphics, files, game_math 

class ViewOverflow(TypedDict):
    horizontal: int
    vertical: int

class CollisionData(TypedDict):
    front: list[int]
    back: list[int]

class Level(surface.Surface):
    def __init__(
        self,
        foreground_source,
        colliders,
        background_art_or_colorLike,
        music=None,
        wrapping: tuple[bool, bool] = (False, False),
    ):
        self.music = music
        self.foreground_source = foreground_source
        self.collider_source = colliders
        self.display = get_display()
        self.display_size = self.display.get_size()
        self.background_source = background_art_or_colorLike
        self.camera = Vector2(0, 0)
        self.wrapping = wrapping

    def __setattr__(self, name: str, value) -> None:
        return super().__setattr__(name, value)

    def load(self):
        background = None
        if files.verify_path(self.background_source):
            self.background = graphics.load_image(
                os.path.abspath(os.path.join(self.background_source))
            )
        self.image = graphics.load_image(self.foreground_source)
        self.rect = self.image.get_rect()
        self.level_bounds = Vector2(self.rect.bottomright)
        self.load_collision()

    def load_collision(self):
        if files.verify_path(self.collider_source):
            with open(self.collider_source, 'rb') as file:
                raw_data = file.read()
            self.collision_data = CollisionData(front=raw_data[::2], back=raw_data[1::2])
            print(self.collision_data)
    
    def get_visual_areas(self) -> list[Rect]:
        areas: list[Rect] = []
        viewport = Rect(self.camera, self.display_size)
        overflows: ViewOverflow = {
            'horizontal': viewport.right - self.image.width,
            'vertical': viewport.bottom - self.image.height
        }
        
        if overflows['horizontal'] <= 0 and overflows['vertical'] <= 0:
            areas.append(viewport)
            return areas
        corner = Rect(0,0, overflows['horizontal'], overflows['vertical'])
        horizontal = Rect(0, self.camera.y, overflows['horizontal'], max(overflows['vertical'], viewport.height))
        vertical = Rect(0, self.camera.y, max(overflows['horizontal'], viewport.width), overflows['vertical'])
        
        if overflows['horizontal'] and overflows['vertical']:
            areas.append(corner)
        
        if overflows['horizontal']:
            viewport.width -= overflows['horizontal']
            areas.append(horizontal)
        
        if overflows['vertical']:
            viewport.height -= overflows['vertical']
            areas.append(vertical)
        
        areas.append(viewport)
        return areas

    def render(self):
        # Preventing a possible RuntimeError
        areas = self.get_visual_areas()
        for rect in areas:
            self.display.blit(self, rect)
        """TODO: add rendering logic"""

    def scroll(self, delta_x=0, delta_y=0) -> None:
        self.camera += Vector2(delta_x, delta_y)
        self.camera.update(
            self.camera.x % self.image.width, self.camera.y % self.image.height
        )
    
    def parallax(self, rows:int, speed:int):
        """TODO: Add parallax scrolling"""
    def get_at(self, position:Vector2):
        """TODO: Add collision after creating format"""


current: Level | None = None
