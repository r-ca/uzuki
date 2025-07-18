import curses
from enum import Enum

class Key(Enum):
    H      = ord('h')
    J      = ord('j')
    K      = ord('k')
    L      = ord('l')
    I      = ord('i')
    X      = ord('x')
    O      = ord('o')
    ESC    = 27
    ENTER  = 10
    BACKSP = 127
    COLON  = ord(':')
    U      = ord('u')
    P      = ord('p')

    @staticmethod
    def from_code(code: int):
        for k in Key:
            if k.value == code:
                return k
        return None
