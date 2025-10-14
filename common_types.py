from enum import Enum, auto

class Player(Enum):
    P1 = auto()
    P2 = auto()

class WinConditionType(Enum):
    NOT_CONNECT_FOUR = auto()
    TIC_TAC_TOE = auto()
    CONNECT_FOUR = auto()

class TokenPhysicsType(Enum):
    FLOATING = auto()
    STRONG_GRAVITY = auto()
    WEAK_GRAVITY = auto()
    TWO_SIDES = auto()
