from abc import ABC, abstractmethod
import sys
from BoardState import BoardState
from Pawn import Pawn
from ..utils.types import Coordinates
from BoardNode import BoardNode

INF:int = sys.maxsize

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
    def __init__(self, depthChecking=10):
        self.__parentNode:BoardNode|None = None
        self.__currentTurn:bool
        self.__depthChecking = depthChecking
        self.initialiseState()

    def initialiseState(self, turn=False):
        """
        This is used to create a tree including all of the possible
        states that the game can have 
        """
        self.__currentTurn = turn
        initialBoardState = BoardState()
        self.__parentNode = BoardNode(initialBoardState)

    def getCurrentBoardState(self) -> BoardState:
        return self.__parentNode.getBoardState()

    def setOpponentMove(self, prevCoordinates:Coordinates, newCoordinates:Coordinates) -> None:
        """
        This simply informs the bot of the move that the player made,
        it will also have to update the tree accordingly
        """
        if(self.__currentTurn == True):
            raise Exception("Opponent can only move a piece when it is his turn")

        childNode = self.__parentNode.getChildNode(prevCoordinates, newCoordinates)
        if(childNode == None):
            raise Exception("This move is not possible!")
        
        self.__parentNode = childNode
        self.__reevaluate()
        self.__currentTurn = True


    def getBotMove(self) -> BoardState:
        """
        This will be used to ask the bot what the next move will be.
        here we will have to execute the min-max algorithm and do
        alpha beta pruning in order to achieve this.
        """
        if(self.__currentTurn == False):
            raise Exception("Can only make a move when it is the bot's move")

        maxScore = -INF
        maxScoringChild:BoardNode 
        for child in self.__parentNode.children:
            if child.score > maxScore:
                maxScore = child.score
                maxScoringChild = child
        
        self.__parentNode = maxScoringChild
        self.__currentTurn = False
        return maxScoringChild.board_state


    def updateEvaluations(self) -> None:
        """
        Reruns the min-max algorithm so that the computer takes into account the
        new moves that have been made
        """
        turn = self.__currentTurn
        depth = self.__depthChecking
        
        if depth >= 0:
            raise Exception("Depth must be greater than zero")

        self.__recursiveUpdateScores(self.__parentNode, turn, depth)
        
    def __recursiveUpdateScores(self, node:BoardNode, turn:bool, depth:int):
        if depth == 0:
            return nodeScore

        nodeScore = None
        if turn == True:
            node.score = -INF
            scores = []
            for child in node.children:
                childScore = self.__recursiveUpdateScores(child, False, depth - 1)
                scores.append(childScore)
            node.score = max(scores)
        else:
            node.score = INF
            for child in node.children:
                childScore = self.__recursiveUpdateScores(child, True, depth - 1)
                scores.append(childScore)
            node.score = min(scores)