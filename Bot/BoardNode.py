from Node import Node
#from ..utils.types import types
RED = 0
WHITE = 1

class BoardNode:
    __boardState:Node = None
    __children:list["BoardNode"] = []
    __evaluation:int = None

    def __init__ (self, boardState:Node, parent = None):
        __boardState = boardState 
        self.parent = parent
        self.__children = []            
        
    def boardStatesTree (self, move_for, depth):
        if depth == 0: #Terminate recursion when depth is 0
            return [self.__boardState]
        possible_moves = self.__boardState.findPossibleMoves(move_for)
        for move in possible_moves:
            next_move_for = RED if move_for ==WHITE else WHITE
            child_node = BoardNode (move, parent = self)
            child_node.boardStatesTree (next_move_for, depth-1)
            self.__children.append(child_node)
        return self.__children

    def getChildren (self):
        return self.__children  
      
    def descendNode(self, nextState:Node):
        pass

    def recursiveDeleteChild(self, childState:Node):
        pass

    def getChildNode(self, childState:Node):
        pass