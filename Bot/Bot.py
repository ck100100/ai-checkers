from abc import ABC, abstractmethod
from BoardState import BoardState
from Pawn import Pawn
from ..utils.constants import Coordinates

class Bot(ABC):
    """
    This is an abstract class, this defines the layout that
    all our future bots must have in order to be compatible
    with the GUI
    """
    def __init__(self):
        pass

    @abstractmethod
    def initialiseState(self):
        pass

    @abstractmethod
    def getCurrentBoardState(self) -> BoardState:
        pass

    @abstractmethod
    def setOpponentMove(self, prevCoordinates:Coordinates, newCoordinates:Coordinates) -> None:
        pass

    @abstractmethod
    def getBotMove(self):
        pass

class BotMinMaxAB(Bot):
    """
    This class will be used to create a bot using the
    min max algorithm with alpha-beta pruning
    """
    def __init__(self):
        pass

    def initialiseState(self):
        pass

    def getCurrentBoardState(self) -> BoardState:
        pass

    def setOpponentMove(self, prevCoordinates:Coordinates, newCoordinates:Coordinates) -> None:
        pass

    def getBotMove(self):
        pass