import os

BASE_PATH = os.path.expandvars("%LOCALAPPDATA%") if os.name == "nt" else os.path.join(os.path.expanduser("~"), ".pyhog")

def verify_path(path):
    return os.path.abspath(path).startswith(BASE_PATH)
    

def handle_IO(game_name:str|bytes, save_name:str|bytes, save_data:str|bytes="", mode="save") -> str:
    path = os.path.join(BASE_PATH, f"{game_name}{os.path.sep}{save_name}.sav")
    if not verify_path(path):
        raise Exception
    with open(path, f"{'w' if mode.lower() == 'save' else ''}b") as save_file:
        if save_file.writable() and mode.lower()=="save":
            save_file.write(save_data)
            return str("Success!")
        elif save_file.readable():
            return save_file.read().decode()
        else:
            raise RuntimeError

def save_game(game_name: str, save_name: str, save_data) -> int:
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