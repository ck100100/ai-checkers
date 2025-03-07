from enum import IntEnum

class Coordinates:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

class PawnType(IntEnum):
    NORMAL = 0
    KING = 1