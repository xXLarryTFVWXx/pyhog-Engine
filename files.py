"""Pyhog file handler"""
"""I might get rid of this, unless I use it for the save files."""
"""Version declaration"""
__BRANCH__ = 0x01 # 0x01 is the master branch 0x02 is the prelease branch and 0x03 is the dev branch
__REALYEAR__ = 2022
__YEAR__ = (__REALYEAR__ // 256, __REALYEAR__ % 256)
__MONTH__ = 0x00
__DAY__ = 13

VER = f"{chr(__BRANCH__)}{chr(__YEAR__[0])}{chr(__YEAR__[1])}{chr(__MONTH__)}{chr(__DAY__)}"
engine_version = 0
engine_version = int("".join([str(ord(_)) for _ in VER]))
"""Header building"""

HeaderLen = 0x08
PADDING = 0x7f
FILE_TYPES = {0x00: "state", 0x01: "save"}
MODES = {0x00: "menu", 0x01: "level"}
HEADER = bytes(f"{chr(HeaderLen)}{VER}{chr(PADDING)}".encode())

class VersionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


# This is currently unused.
def verify_version(file, data):
    """Verifies that the data's version is the same as the above Version"""
    file_ver = ""
    for num in data[1:5]:
        file_ver += str(num)
    version_to_check = int(file_ver)
    version_delta = engine_version - version_to_check
    if not version_delta == 0:
        raise VersionError(f"Uh oh, looks like this file is {version_delta} versions behind.")
    return True

def get_state() -> str:
    """Gets the current state of the game with an external file"""
    with open(f"state.phg", "rb") as f:
        data = f.read()
        # if verify_version(f"state.phg", data):
        """verision verification temporarily removed"""
        return MODES[data[-2]], data[-1]

def set_state(mode, ID:int) -> None:
    """Sets the current state of the game with an external file"""
    with open(f"state.phg", "wb") as f:
        f.write(HEADER + bytes(f"{chr(mode)}{chr(ID)}".encode()))
        
def save(fname, data:str):
    with open(f"{fname}.phg", 'wb') as f:
        f.write(VER + data.encode())

def load(fname):
    with open(f"{fname}.phg", "rb") as f:
        full = f.read()



if not __name__ == "__main__":
    set_state(0, 0)