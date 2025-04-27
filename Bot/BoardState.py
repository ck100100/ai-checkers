from .Pawn import Pawn
from utils.types import Coordinates, Piece
from typing import Optional

class BoardState:
    """
    This IS used in order to represent all the
    pieces on the board
    """
    def __init__(self, red_pieces=None, white_pieces=None, player:Piece=None):
        if(red_pieces == None and white_pieces == None):
            if(player == None):
                raise Exception("Need to supply a player value")
            self.__setInitialState()
        elif(red_pieces != None and white_pieces != None):
            self.red_pieces = red_pieces
            self.white_pieces = white_pieces #REMEMBER: these are lists of tuples
        else:
            raise Exception("One of the piece types were not given!")

    def is_empty(self, row, col):
        return not any(piece.row == row and piece.col == col for piece in self.red_pieces + self.white_pieces)
    
    def copy(self):
        new_red_pieces = [piece.copy() for piece in self.red_pieces]
        new_white_pieces = [piece.copy() for piece in self.white_pieces]
        return BoardState(new_red_pieces, new_white_pieces)

    def makeMove(self, prevPosition:Coordinates, newPosition:Coordinates) -> None:
        pawnToMove = self.getPawnAtPosition(prevPosition)
        if(pawnToMove == None):
            raise Exception("This pawn does not exist!")
        pawnToMove.move(newPosition.yPos, newPosition.xPos)
        
    def getPawnAtPosition(self, coordinates:Coordinates) -> Optional[Pawn]:
        searchResult = self.__searchPawnPositionInList(coordinates, self.red_pieces)
        if(searchResult != None):
            return searchResult

        searchResult = self.__searchPawnPositionInList(coordinates, self.white_pieces)
        return searchResult
        
    def __searchPawnPositionInList(self, pos:Coordinates, list) -> Optional[Pawn]:
        found:bool = False
        i = 0
        while (not found) and i < len(list):
            currPawn:Pawn = list[i]
            if(currPawn.col == pos.xPos and currPawn.row == pos.yPos):
                found = True
            else:
                i += 1

        if found:
            return list[i]
        else:
            return None



    def __setInitialState(self) -> None:
        """
        Returns the state of the board when the game first starts
        """

        redPiecePositions = [(0, 0), (0, 2), (0, 4), (0, 6), (1, 1), (1, 3), (1, 5), (1, 7), (2, 0), (2, 2), (2, 4), (2, 6)]
        whitePiecePositions = [(5, 1), (5, 3), (5, 5), (5, 7), (6, 0), (6, 2), (6, 4), (6, 6), (7, 1), (7, 3), (7, 5), (7, 7)]

        self.red_pieces = [Pawn(row, col) for row, col in redPiecePositions]
        self.white_pieces = [Pawn(row, col) for row, col in whitePiecePositions]
    
    def __eq__(self, otherObject):
        if(isinstance(otherObject, BoardState) == False):
            raise Exception("Cant compare objects that have different types")

        otherBoardState:BoardState = otherObject
        isEqualBoardState:bool = self.__comparePawnArrays(self.red_pieces, otherBoardState.red_pieces) and self.__comparePawnArrays(self.white_pieces, otherBoardState.white_pieces)

        return isEqualBoardState

    def comparePawnsByPlayer(self, otherBoardState:'BoardState', player:Piece):
        res:bool
        if(player == Piece.WHITE):
            res = self.__comparePawnArrays(self.white_pieces, otherBoardState.white_pieces)
        elif(player == Piece.RED):
            res = self.__comparePawnArrays(self.red_pieces, otherBoardState.red_pieces)
        
        return res

    def __comparePawnArrays(self, pawnList1:list[Pawn], pawnList2:list[Pawn]) -> bool:
        list1 = pawnList1.copy()
        list2 = pawnList2.copy()

        while len(list1) > 0:
            found = False
            for j in range(len(list2)):
                if(list1[0] == list2[j]):
                    found = True
                    list2.pop(j)
                    break

            if(found == False):
                return False
            else:
                list1.pop(0)

        if(len(list2) > 0):
            return False
        
        return True

    def __str__(self):
        arr = self.to2DArray()
        textRepr = "Board State\n_______________________________"
        for row in arr:
            textRepr += "\n" + str(row)

        return textRepr
        
    def to2DArray(self):
        board = []
        for i in range(8):
            board.append([])
            for j in range (8):
                board[i].append(" ")
        
        whiteSymbol = "X"
        redSymbol = "O"
        for piece in self.white_pieces:
            board[piece.row][piece.col] = whiteSymbol

        for piece in self.red_pieces:
            board[piece.row][piece.col] = redSymbol
        
        return board