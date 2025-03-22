from Node import Node
class BoardNode:
    __boardState:Node = None
    __children:list["BoardNode"] = []
    __evaluation:int = None
    
    def __init__(self, boardState:Node):
        __boardState = boardState

    def descendNode(self, nextState:Node):
        pass

    def recursiveDeleteChild(self, childState:Node):
        pass

    def getChildNode(self, childState:Node):
        pass