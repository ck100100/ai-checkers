from utils.types import PawnType
from utils.constants import BOARD_HEIGHT

class Pawn:
    def __init__(self, row, col, is_king=False):
        self.row = row
        self.col = col
        self.is_king = is_king

    def getPawnType(self) -> type[PawnType]:
        return self.__pawnType
    
    #not needed with my implementation. Handled by each node
    def promoteToKing(self) -> None:
        if(self.__pawnType == PawnType.KING):
            raise Exception("Unnable to promote pawn that is already promoted!")
        
        finalRow = None
        if(self.__isFriendly):
            finalRow = BOARD_HEIGHT - 1
        else:
            finalRow = 0
        
        if(self.__coordinates.yPos != finalRow):
            raise ValueError("The pawn must be on the highest part of the board in order to promote!")

        self.__pawnType = PawnType.KING
    
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
