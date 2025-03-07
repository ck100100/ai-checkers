from abc import ABC, abstractmethod
from BoardState import BoardState
from Pawn import Pawn
from ..utils.types import Coordinates

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
        """
        This is used to create a tree including all of the possible
        states that the game can have 
        """
        pass

    def getCurrentBoardState(self) -> BoardState:
        pass

    def setOpponentMove(self, prevCoordinates:Coordinates, newCoordinates:Coordinates) -> None:
        """
        This simply informs the bot of the move that the player made,
        it will also have to update the tree accordingly
        """
        pass

    def getBotMove(self):
        """
        This will be used to ask the bot what the next move will be.
        here we will have to execute the min-max algorithm and do
        alpha beta pruning in order to achieve this.
        """
        pass