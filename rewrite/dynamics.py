from pygame import sprite

class Character(sprite.Sprite):
    """Inheriting from pygame-ce's Sprite class for auto handling of the thing"""
    def __init__(self, name, *groups: sprite.AbstractGroup[sprite._SpriteSupportsGroup]) -> None:
        super().__init__(*groups)
        self.load_config()