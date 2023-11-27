"""Pyhog file handler"""
"""I might get rid of this, unless I use it for the save files."""
"""Version declaration"""
__BRANCH__ = 0x01 # 0x01 is the master branch 0x02 is the prelease branch and 0x03 is the dev branch
__REALYEAR__ = 2022
__YEAR__ = (__REALYEAR__ // 256, __REALYEAR__ % 256)
__MONTH__ = 0x00
__DAY__ = 13

VER = f"DEV_10_31_2023"
"""Header building"""

HeaderLen = len(VER)
PADDING = 0x7f

class VersionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


# This is currently unused.
def verify_version(file, data):
    raise NotImplementedError
    """Verifies that the data's version is the same as the above Version"""
    file_ver = "".join(str(num) for num in data[1:5])
    # FIXME: I return an incorrect number
    version_to_check = int(file_ver)
    version_delta = engine_version - version_to_check
    if version_delta != 0:
        raise VersionError(f"Uh oh, looks like this file is {version_delta} versions behind.")
    return True

# def get_state() -> str:
#     """Gets the current state of the game with an external file"""
#     with open("state.phg", "rb") as f:
#         data = f.read()
#         # if verify_version(f"state.phg", data):
#         """verision verification temporarily removed"""
#         return MODES[data[-2]], data[-1]
        
def save(fname, data:str):
    with open(f"{fname}.phg", 'wb') as f:
        f.write(f"{VER} {data}".encode())

def load(fname):
    with open(f"{fname}.phg", "rb") as f:
        full = f.read()