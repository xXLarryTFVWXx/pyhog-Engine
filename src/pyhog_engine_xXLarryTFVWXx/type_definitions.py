from dataclasses import dataclass
import typing
from uuid import UUID
import pygame
import pygame.typing as game_types
import pygame.event as game_event  # pyright: ignore[reportUnusedImport]
from pygame.joystick import JoystickType
from . import game_math

# Controller and input type definitions

controllers: list[JoystickType]
CONTROLLER_METHODS = (
    typing.Literal["WASD"]
    | typing.Literal["ARROWS"]
    | typing.Literal["CONTROLLER"]
    | typing.Literal["DEBUG"]
)


class KeyboardMovement(typing.TypedDict):
    up: int
    down: int
    left: int
    right: int


class ControllerMovement(typing.TypedDict):
    vertical: int
    horizontal: int


class GeneralControls(typing.TypedDict):
    jump: int
    energy: int
    attack: int
    ground: int


class KeyboardControls(GeneralControls):
    movement: KeyboardMovement


class JoystickControls(GeneralControls):
    movement: ControllerMovement


class DebugControls(typing.TypedDict):
    quit: int
    fps: int
    level: int
    actors: int
    placer: int
    save: int


class ControlContainer(typing.TypedDict):
    method: CONTROLLER_METHODS
    WASD: KeyboardControls
    ARROWS: KeyboardControls
    DEBUG: DebugControls
    CONTROLLER: JoystickControls


# Game information type definitions


class MetaDataContainer(typing.TypedDict):
    engine_version: int
    game_id: UUID
    game_version: tuple[int, int, int, int, str]
    author: dict[str, UUID]
    display_name: str
    extends: list[UUID]
    uses: dict[UUID, list[str]]

class GameDataManifest(typing.TypedDict):
    metadata: MetaDataContainer
    main_data: dict[str, typing.Any]

# Level type Definitions





class ViewOverflow(typing.TypedDict):
    horizontal: int
    vertical: int


class WrappingData(typing.TypedDict):
    horizontal: bool
    vertical: bool


class ScrollData(typing.TypedDict):
    speed: float
    size: int


class ScrollContainer(typing.TypedDict):
    direction: str
    data: list[ScrollData]


class TileCollision(typing.TypedDict):
    angle: int
    heightOffsets: list[int]
    widthOffsets: list[int]


class ChunkCollision(typing.TypedDict):
    frontTiles: list[TileCollision]
    backTiles: list[TileCollision]


# Default Values

EMPTY_TILE: TileCollision = {"angle": 0, "heightOffsets": [0], "widthOffsets": [0]}
EMPTY_CHUNK: ChunkCollision = {"backTiles": [EMPTY_TILE], "frontTiles": [EMPTY_TILE]}
NO_SCROLL: ScrollData = {"size": 0, "speed": 0}
NO_WRAP: WrappingData = {"horizontal": False, "vertical": False}
HORIZONTAL_WRAP: WrappingData = {"horizontal": True, "vertical": False}
VERTICAL_WRAP: WrappingData = {"horizontal": False, "vertical": True}
ALL_WRAP: WrappingData = {"horizontal": True, "vertical": True}

@dataclass
class Displayable:
    source: typing.BinaryIO | pygame.Color | game_types.SequenceLike[int] | str | int
    parent: typing.Optional[pygame.Surface]

    def __post_init__(self) -> None:
        self.position: game_math.Vector2D = game_math.Vector2D(0)
        self.area = pygame.Vector2(4)

COLLISION_LAYERS: list[typing.Literal["frontTiles"] | typing.Literal["backTiles"]] = [
    "frontTiles",
    "backTiles",
]

# JSON Type hinting NOTE: Only recommended when using strict with a type checker

class Rect(typing.TypedDict):
    x: int
    y: int
    width: int
    height: int


class Cell(typing.TypedDict):
    rect: Rect


CELL_CONTAINER = list[Cell]
SPRITESHEET_HINT = dict[str, CELL_CONTAINER]

# Character types


class Character(Displayable):
    name: str = ""
    top_speed: int = 6
    angle: int = 0
    collision_box: pygame.Rect = pygame.Rect(0, 0, 0, 0)
    collision_layer: int = 0
    health: int = 1
    velocity: game_math.Vector2D = game_math.Vector2D(0)
    # flags
    is_player: bool = False
    is_invincible: bool = False
    is_spinning: bool = False
    # TODO: Figue out how to have the typing callable


class CharacterJSON(typing.TypedDict):
    name: str
    sprite_file: str
    is_player: bool



# Level Type Definitions


class Background(Displayable):
    scroll_data: ScrollContainer = {"direction": "None", "data": [NO_SCROLL]}


class LevelContainer(Displayable):
    name: str = ""
    background_source: typing.Optional[
        game_types.FileLike | typing.BinaryIO | game_types.ColorLike
    ]
    camera: game_types.IntPoint | pygame.Vector2 | None = None
    wrapping: WrappingData = NO_WRAP
    objects: typing.Optional[list[Displayable]] = None
    background: typing.Optional[Background | game_types.ColorLike] = None
    music_file: typing.Optional[game_types.FileLike] = None
    level_size: game_math.Vector2D = game_math.Vector2D(64, 24)
    collision_data: list[ChunkCollision] = [EMPTY_CHUNK]
