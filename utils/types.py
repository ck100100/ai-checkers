from enum import IntEnum

class Coordinates:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

class PawnType(IntEnum):
    NORMAL = 0
    KING = 1

class Piece(IntEnum):
    RED = 0
    WHITE = 1

class Player(IntEnum):
    YOU = 0
    OPP = 1