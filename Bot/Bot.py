from abc import ABC, abstractmethod
import sys
from .BoardState import BoardState
from .Pawn import Pawn
from utils.types import Coordinates
from .BoardNode import BoardNode

INF:int = sys.maxsize
RED =0
WHITE=1

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
        self._visited_nodes = 0
        self._pruned_nodes = 0
        self._pruned_branches = [] #For testing

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

        self.__parentNode.boardStatesTree(self.__currentTurn, self.__depthChecking)

        childNode = self.__parentNode.getChildNode(prevCoordinates, newCoordinates)
        if(childNode == None):
            raise Exception("This move is not possible!")
        
        self.__parentNode = childNode
        self.__currentTurn = True

        self.updateEvaluations()


    def getBotMove(self) -> BoardState:
        print("reminder that depth checking is set to: ", self.__depthChecking)
        """
        This will be used to ask the bot what the next move will be.
        here we will have to execute the min-max algorithm and do
        alpha beta pruning in order to achieve this.
        """
        if(self.__currentTurn == False):
            raise Exception("Can only make a move when it is the bot's move")

        maxScore = -INF
        maxScoringChild:BoardNode         
        alpha = -INF
        beta = INF
        possible_moves = self.__parentNode.findPossibleMovesWithPruning(True) #moves with a level of pruning
        #keep the best 10 moves
        possible_moves = sorted(possible_moves, key=lambda move: move.evaluatePosition(True), reverse=True) [:10]
        for move in possible_moves:
            moveScore = self.__recursiveUpdateScores(move,self.__depthChecking -1, alpha,beta, False)
            if moveScore>= maxScore:
                maxScore = moveScore
                maxScoringChild = move
            alpha = max (alpha, maxScore)
            if maxScoringChild ==None:
                raise Exception("Bot could not find valid move.")          
        
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
        
        if depth <= 0:
            raise Exception("Depth must be greater than zero")

        self.__parentNode.boardStatesTree(self.__currentTurn, depth)
        self.__recursiveUpdateScores(self.__parentNode, turn, depth)
        
    def __recursiveUpdateScores(self, node: BoardNode, turn: bool, depth: int, alpha: int = -INF, beta: int = INF):
        """
        Recursively updates the scores of the nodes in the game tree using alpha-beta pruning.
        """
        if depth == 0 or node.is_terminal():
            return node.evaluatePosition(turn)
        
        children = node.findPossibleMovesWithPruning(RED if turn else WHITE ,alpha,beta)
        children.sort(key=lambda ch: ch.evaluatePosition(turn),reverse= turn)


        if turn:  # Maximizing player
            maxEval = -INF
            for child in children:
                eval = self.__recursiveUpdateScores(child, False, depth - 1, alpha, beta)
                self._visited_nodes += 1 #Ignore this/for testing
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    self._pruned_nodes += 1  # Count pruning
                    self._pruned_branches.append((node,child))
                    break  # Prune the branch
            node.score = maxEval
            return maxEval
        else:  # Minimizing player
            minEval = INF
            for child in children:
                eval = self.__recursiveUpdateScores(child, True, depth - 1, alpha, beta)
                self._visited_nodes += 1
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    self._pruned_nodes += 1  # Count pruning
                    self._pruned_branches.append((node,child))
                    break  # Prune the branch
            node.score = minEval
            return minEval

    def getPrunedBranches(self):
        return self._pruned_branches
