from abc import ABC, abstractmethod
import sys
from .BoardState import BoardState
from .Pawn import Pawn
from utils.types import Coordinates
from utils.constants import WHITE, RED
from .BoardNode import BoardNode

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
    min-max algorithm with alpha-beta pruning.
    """
    def __init__(self, depthChecking=10, color=RED):
        self.__parentNode: BoardNode | None = None
        self.__botColor = color  # Store the bot's color (WHITE or RED)
        self.__currentTurn: bool = (color == WHITE)  # True if bot starts as WHITE
        self.__depthChecking = depthChecking
        self.initialiseState()

    def initialiseState(self, turn=RED):
        """
        This is used to create a tree including all of the possible
        states that the game can have
        """
        self.__currentTurn = (turn == self.__botColor)  # Set turn based on bot's color
        initialBoardState = BoardState()
        self.__parentNode = BoardNode(initialBoardState)

    def getCurrentBoardState(self) -> BoardState:
        return self.__parentNode.getBoardState()

    def setOpponentMove(self, prevCoordinates: Coordinates, newCoordinates: Coordinates) -> None:
        """
        This simply informs the bot of the move that the player made,
        it will also have to update the tree accordingly
        """
        if self.__currentTurn == self.__botColor:
            raise Exception("Opponent can only move a piece when it is their turn.")

        # Update the game tree based on the opponent's move
        self.__parentNode.boardStatesTree(self.__currentTurn, self.__depthChecking)

        # Find the child node corresponding to the opponent's move
        childNode = self.__parentNode.getChildNode(prevCoordinates, newCoordinates)
        if(childNode == None):
            raise Exception("This move is not possible!")

        # Update the parent node and switch to the bot's turn
        self.__parentNode = childNode
        self.__currentTurn = not self.__currentTurn  # Switch turn to the bot

        # Recalculate evaluations after the opponent's move
        self.updateEvaluations()


    def getBotMove(self, currently_moving: bool) -> BoardState:
        """
        This will be used to ask the bot what the next move will be.
        Here we execute the min-max algorithm with alpha-beta pruning.
        """
        if currently_moving != self.__botColor:
            raise Exception("Bot can only move when it's its turn")

        maxScore = -INF
        maxScoringChild: BoardNode | None = None

        # Ensure children are populated
        if not self.__parentNode.children:
            self.__parentNode.boardStatesTree(self.__currentTurn, self.__depthChecking)

        # Evaluate all possible moves (children of the current node)
        for child in self.__parentNode.children:
            print("evaluated a child")
            if child.score > maxScore:
                maxScore = child.score
                maxScoringChild = child

        if maxScoringChild is None:
            raise Exception("No valid moves available for the bot.")

        # Update the parent node and switch to the opponent's turn
        self.__parentNode = maxScoringChild
        self.__currentTurn = not self.__currentTurn  # Switch turn to the opponent
        return maxScoringChild

    def updateEvaluations(self) -> None:
        """
        Reruns the min-max algorithm so that the bot takes into account
        the new moves that have been made.
        """
        turn = self.__currentTurn
        depth = self.__depthChecking

        if depth <= 0:
            raise Exception("Depth must be greater than zero.")

        # Update the game tree and recalculate scores
        self.__parentNode.boardStatesTree(self.__currentTurn, depth)
        self.__recursiveUpdateScores(self.__parentNode, turn, depth)

    def __recursiveUpdateScores(self, node: BoardNode, turn: bool, depth: int, alpha: int = -INF, beta: int = INF):
        """
        Recursively updates the scores of the nodes in the game tree using alpha-beta pruning.
        """
        if depth == 0 or node.is_terminal():
            return node.evaluatePosition(self.__botColor)  # Evaluate based on the bot's color

        if turn:  # Maximizing player (bot's turn)
            maxEval = -INF
            for child in node.children:
                eval = self.__recursiveUpdateScores(child, False, depth - 1, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Prune the branch
            node.score = maxEval
            return maxEval
        else:  # Minimizing player (opponent's turn)
            minEval = INF
            for child in node.children:
                eval = self.__recursiveUpdateScores(child, True, depth - 1, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Prune the branch
            node.score = minEval
            return minEval

