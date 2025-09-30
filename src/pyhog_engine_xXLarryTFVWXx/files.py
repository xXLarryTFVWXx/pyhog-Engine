import os
from hashlib import sha256

print(f"files.py: {__file__}")

RELEASE = 0
FEATURE = 1

ENGINE_VERSION = (0, 0, 0, 0, "dev-0")
INVALID_VERSIONS: set[str] = set()

USER_DIRECTORY = os.path.expanduser("~")

BASE_PYHOG_PATH = os.path.join(USER_DIRECTORY, "pyhog")
BASE_GAME_PATH = os.path.join(BASE_PYHOG_PATH, "games")
BASE_SAVE_PATH = os.path.join(BASE_PYHOG_PATH, "saves")
os.makedirs(BASE_GAME_PATH, exist_ok=True)
os.makedirs(BASE_SAVE_PATH, exist_ok=True)


def verify_path(path: str, root: str = "save") -> bool:
    if root.lower() == "save":
        return os.path.abspath(path).startswith(BASE_SAVE_PATH)
    if root.lower() == "game" or root.lower() == "asset":
        return os.path.abspath(path).startswith(BASE_GAME_PATH)
    return False


def verify_version(engine_version_target: tuple[int, int, int, int, str]):
    return (
        not sha256(
            "".join((str(item) for item in engine_version_target)).encode(),
            usedforsecurity=False,
        )
        in INVALID_VERSIONS
    )


def handle_IO(
    game_name: str | bytes,
    save_name: str | bytes,
    save_data: str | bytes = "",
    mode: str = "save",
) -> str:
    path = os.path.join(BASE_SAVE_PATH, f"{game_name}{os.path.sep}{save_name}.sav")
    if not verify_path(path):
        raise Exception
    with open(path, f"{'w' if mode.lower() == 'save' else ''}b") as save_file:
        if save_file.writable() and mode.lower() == "save":
            save_file.write(save_data)
            return str("Success!")
        elif save_file.readable():
            return save_file.read().decode()
        else:
            raise RuntimeError("Umm, invalid mode?")


def save_game(game_name: str, save_name: str, save_data: bytes) -> int:
    try:
        handle_IO(game_name, save_name, save_data)
        return 0
    except PermissionError:
        print("Improper permissions.")
        return 1
    except RuntimeError:
        print("Incorrect mode")
        return 2
    except Exception:
        print("Unknown exception occurred.")
        return 3


def load_game(game_name: str, save_name: str) -> str:
    try:
        return handle_IO(game_name, save_name, mode="load")
    except Exception:
        print("Unknown error occured.")
        return "Read Failed!"
