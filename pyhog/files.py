"""Pyhog file handler"""

"""Version declaration"""
__Release__ = 0x00
__Feature__ = 0x00
__Bugfix__ = 0x00
__BETA__ = 0x01

VER = f"{chr(__Release__)}{chr(__Feature__)}{chr(__Bugfix__)}{chr(__BETA__)}"

"""Header building"""

HeaderLen = 0x08
PADDING = 0x7f
FILE_TYPES = {0x00: "state", 0x01: "save"}
MODES = {0x00: "menu", 0x01: "level"}
HEADER = bytes(f"{chr(HeaderLen)}{VER}{chr(PADDING)}".encode())

class VersionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def verify_version(file, data):
    """Verifies that the data's version is the same as the above Version"""
    file_ver = ""
    for _ in data[1:5]:
        file_ver += chr(_)
    file_ver = file_ver
    return file_ver == VER

def get_state() -> str:
    """Gets the current state of the game with an external file"""
    with open(f"state.phg", "rb") as f:
        data = f.read()
        if verify_version(f"state.phg", data):
            
            return MODES[data[-2]], data[-1]

def set_state(mode, ID:int) -> None:
    """Sets the current state of the game with an external file"""
    with open(f"state.phg", "wb") as f:
        f.write(HEADER + bytes(f"{chr(mode)}{chr(ID)}".encode()))
        
def save(fname, data:str):
    with open(f"{fname}.phg", 'wb') as f:
        f.write(VER + bytes(data))

def load(fname):
    with open(f"{fname}.phg", "rb") as f:
        full = f.read()
        
if not __name__ == "__main__":
    set_state(0, 0)