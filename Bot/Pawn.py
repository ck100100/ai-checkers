from ..utils.constants import PawnType, Coordinates

class Pawn:
    def __init__(self, pawnType:type[PawnType], coordinates:Coordinates):
        self.__pawnType = pawnType
        self.__coordinates = coordinates

    def updateCoordinates(self, newCoordinates:Coordinates) -> None:
        # setup a function that makes sure that the coordinates are valid
        self.__coordinates = newCoordinates

    def getCoordinates(self) -> Coordinates:
        self.__coordinates