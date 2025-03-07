from ..utils.types import PawnType, Coordinates
from ..utils.constants import BOARD_HEIGHT

class Pawn:
    def __init__(self, pawnType:type[PawnType], coordinates:Coordinates):
        self.__pawnType = pawnType
        self.__coordinates = coordinates

    def updateCoordinates(self, newCoordinates:Coordinates) -> None:
        # setup a function that makes sure that the coordinates are valid
        self.__coordinates = newCoordinates

    def getCoordinates(self) -> Coordinates:
        self.__coordinates

    def getPawnType(self) -> type[PawnType]:
        return self.__pawnType
    
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