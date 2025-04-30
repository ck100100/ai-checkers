from utils.types import PawnType
from utils.constants import BOARD_HEIGHT

class Pawn:
    def __init__(self, row, col, is_king=False):
        self.row = row
        self.col = col
        self.is_king = is_king

    def getPawnType(self) -> type[PawnType]:
        return self.__pawnType
    
    def move(self, newRow, newCol):
        if (0 > newRow and newRow > 7) or (0 > newCol and newCol > 7):
            raise Exception("Illegal Move")
        self.row = newRow
        self.col = newCol

    def getType(self) -> type[PawnType]:
        if self.is_king:
            return PawnType.KING
        else:
            return PawnType.NORMAL

    def __eq__(self, other):
        if other == None:
            return False
        
        return self.row == other.row and self.col == other.col and self.is_king == other.is_king

    def __hash__(self):
        return hash((self.row, self.col, self.is_king))

    def copy(self):
        return Pawn(self.row, self.col, self.is_king)
