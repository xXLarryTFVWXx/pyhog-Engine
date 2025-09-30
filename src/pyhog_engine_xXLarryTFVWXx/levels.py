import io

import pygame
from . import graphics, type_definitions, files


class Level(type_definitions.LevelContainer):

    def load(self):
        if hasattr(self.background_source, "readable"):
            assert isinstance(self.background_source, io.BufferedIOBase)
            if self.background_source.closed is not True:
                raise AttributeError(
                    f"Attribute background_source should never be an open file!"
                )
            if isinstance(self.background_source, str):
                if files.verify_path(self.background_source):
                    with open(self.background_source, "rb") as source_file:
                        self.background = graphics.Background(source_file)
            elif isinstance(self.background_source, (tuple, list)):
                self.background = pygame.Color(self.background_source)


current: Level
