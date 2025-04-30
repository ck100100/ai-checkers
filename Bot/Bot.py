from abc import ABC, abstractmethod
import sys
import copy
from .BoardState import BoardState
from .Pawn import Pawn
from utils.types import Coordinates, Piece, Player
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
    def getBotMove(self, move:BoardState):
        pass

class BotMinMaxAB(Bot):
    """
    This class will be used to create a bot using the
    min max algorithm with alpha-beta pruning
    """
    def __init__(self, player:Piece, depthChecking=10):
        self.__parentNode:BoardNode|None = None
        self.__currentTurn:bool
        self.__depthChecking = depthChecking
        self._visited_nodes = 0
        self._pruned_nodes = 0
        self._pruned_branches = [] #For testing
        self.__player = player
        self.__otherPlayer = Piece.RED if player == Piece.WHITE else Piece.WHITE
        self.initialiseState()

    def initialiseState(self):
        """
        This is used to create a tree including all of the possible
        states that the game can have 
        """
        self.__currentTurn = True if self.__player == Piece.RED else False
        initialBoardState = BoardState(player=self.__player)
        self.__parentNode = BoardNode(initialBoardState, self.__player)

    def getCurrentBoardState(self) -> BoardState:
        return self.__parentNode.getBoardState()

    def setOpponentMove(self, prevCoordinates:Coordinates, newCoordinates:Coordinates) -> None:
        """
        This simply informs the bot of the move that the player made,
        it will also have to update the tree accordingly
        """
        if(self.__currentTurn == True):
            raise Exception("Opponent can only move a piece when it is his turn")

        self.__parentNode.boardStatesTree(Player.YOU if self.__currentTurn else Player.OPP, self.__depthChecking)


        childNode = self.__parentNode.getChildNode(prevCoordinates, newCoordinates, Player.OPP)
        if(childNode == None):
            raise Exception("This move is not possible!")
        
        self.__parentNode = childNode
        self.__currentTurn = True

        self.updateEvaluations()


    def getBotMove(self, moveNode:BoardNode):
        print("reminder that depth checking is set to: ", self.__depthChecking)
        """
        This will be used to ask the bot what the next move will be.
        here we will have to execute the min-max algorithm and do
        alpha beta pruning in order to achieve this.
        """
        self.updateEvaluations()
        if moveNode != None:
            moveState = moveNode.board_state
            child = self.__parentNode.getChildNode(moveState)
            if child.is_terminal() == True:
                return None
            self.__parentNode = child
            self.__parentNode.parent = None

            self.__currentTurn = True


        maxScore = -INF
        maxScoringChild:BoardNode         
        alpha = -INF
        beta = INF
        possible_moves = self.__parentNode.findPossibleMovesWithPruning(Player.YOU) #moves with a level of pruning
        #keep the best 10 moves
        possible_moves = sorted(possible_moves, key=lambda move: move.evaluatePosition(True), reverse=True) [:10]
        if(len(possible_moves) == 0):
            raise Exception("No moves available!")
        for moveState in possible_moves:
            moveScore = self.__recursiveUpdateScores(moveState,self.__depthChecking -1, alpha,beta, False)
            if moveScore>= maxScore:
                maxScore = moveScore
                maxScoringChild = moveState
            alpha = max (alpha, maxScore)
            if maxScoringChild ==None:
                raise Exception("Bot could not find valid move.")          
        self.__parentNode = maxScoringChild
        self.__parentNode.parent = None
        self.__currentTurn = False
        return copy.deepcopy(self.__parentNode)


    def updateEvaluations(self) -> None:
        """
        Reruns the min-max algorithm so that the computer takes into account the
        new moves that have been made
        """
        turn = self.__currentTurn
        depth = self.__depthChecking
        
        if depth <= 0:
            raise Exception("Depth must be greater than zero")

        self.__parentNode.boardStatesTree(Player.YOU if self.__currentTurn else Player.OPP, depth)
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