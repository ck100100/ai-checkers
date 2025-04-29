from .Pawn import Pawn
from .BoardState import BoardState
from utils.types import Coordinates, Piece, Player
import sys

# I know we  have a constants file. i will fix it later
BOARD_SIZE = 8
RED = 0
WHITE = 1

INF:int = sys.maxsize

class BoardNode:
    def __init__(self, board_state:BoardState, botPieceType:Piece, parent=None):
        self.board_state:BoardState = board_state
        self.parent = parent
        self.children = []
        self.score = 0  # unused for the time being
        self.alpha = -INF
        self.beta = INF
        self.__isTerminal:bool = False
        self.movenum = 1
        self.botPieces:Piece = botPieceType
        self.oppPieces:Piece = Piece.RED if botPieceType == Piece.WHITE else Piece.WHITE

    def boardStatesTree(self, move_for:Player, depth):
        if depth == 0:  # Terminate recursion when depth is 0
            return [self.board_state]

        possible_moves = self.findPossibleMoves(move_for)
        if(len(possible_moves) == 0):
            self.setTerminal()
        child=1
        for move in possible_moves:
            next_move_for = Player.YOU if move_for == Player.OPP else Player.OPP
            move.boardStatesTree(next_move_for, depth - 1)
            self.children.append(move)
            child += 1

        return self.children

    def getChildren (self):
        return self.children  
    
    def getChildNode(self, prevCoordinates:Coordinates, newCoordinates:Coordinates, player:Player):
        nextBoardState = self.board_state.copy()
        nextBoardState.makeMove(prevCoordinates, newCoordinates)
        found:bool = False
        i = 0
        currentChild = None
        while (not found) and i < len(self.children):
            currentChild:'BoardNode' = self.children[i]
            playerPieceType = self.botPieces if player == Player.YOU else self.oppPieces
            if(currentChild.board_state.comparePawnsByPlayer(nextBoardState, playerPieceType)):
                found = True
            else:
                i += 1
        
        if not found:
            raise Exception("This move is not possible!")
        
        return currentChild


    def __str__(self):
        return str(self.board_state)

    def is_within_bounds(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def create_new_node(self, moved_piece, new_row, new_col, captured_piece=None):
        new_board_state = self.board_state.copy()

        # Check if the moved piece should be promoted to a king
        if new_row == BOARD_SIZE - 1 and moved_piece in new_board_state.red_pieces and not moved_piece.is_king:
            # Red piece reaches the last row and becomes a king
            new_board_state.red_pieces.remove(moved_piece)
            new_board_state.red_pieces.append(Pawn(new_row, new_col, is_king=True))
        elif new_row == 0 and moved_piece in new_board_state.white_pieces and not moved_piece.is_king:
            # White piece reaches the last row and becomes a king
            new_board_state.white_pieces.remove(moved_piece)
            new_board_state.white_pieces.append(Pawn(new_row, new_col, is_king=True))
        else:
            # Regular move or jump
            if moved_piece in new_board_state.red_pieces:
                new_board_state.red_pieces.remove(moved_piece)
                new_board_state.red_pieces.append(Pawn(new_row, new_col, moved_piece.is_king))
            elif moved_piece in new_board_state.white_pieces:
                new_board_state.white_pieces.remove(moved_piece)
                new_board_state.white_pieces.append(Pawn(new_row, new_col, moved_piece.is_king))

        # Remove captured piece if any
        if captured_piece:
            if captured_piece in new_board_state.red_pieces:
                new_board_state.red_pieces.remove(captured_piece)
            else:
                new_board_state.white_pieces.remove(captured_piece)
    
        new_node = BoardNode(new_board_state, self.botPieces, self)
        new_node.movenum = self.movenum + 1  # Increment movenum based on the parent node
        return new_node

    def findPossibleMoves(self, move_for:Player):
        children = []
        botPawns = None
        oppPawns = None
        if self.botPieces == Piece.RED:
            botPawns = self.board_state.red_pieces
            oppPawns = self.board_state.white_pieces
        else:
            botPawns = self.board_state.white_pieces
            oppPawns = self.board_state.red_pieces

        pieces = botPawns if move_for == Player.YOU else oppPawns

        for piece in pieces:
            # Determine possible directions based on whether the piece is a king
            if piece.is_king:
                directions = [-1, 1]  # Kings can move both forward and backward
            else:
                directions = [1] if (move_for == Player.YOU and self.botPieces == Piece.RED) or (move_for == Player.OPP and self.oppPieces == Piece.RED) else [-1]  # Regular pieces move forward only

            for direction in directions:
                # Normal moves
                for dc in [-1, 1]:  # Check both left and right diagonals
                    new_row, new_col = piece.row + direction, piece.col + dc
                    if self.is_within_bounds(new_row, new_col) and self.board_state.is_empty(new_row, new_col):
                        new_node = self.create_new_node(piece, new_row, new_col)
                        children.append(new_node)

                # Jump moves
                for dc in [-1, 1]:
                    new_row, new_col = piece.row + 2 * direction, piece.col + 2 * dc
                    mid_row, mid_col = piece.row + direction, piece.col + dc
                    if self.is_within_bounds(new_row, new_col) and self.board_state.is_empty(new_row, new_col):
                        mid_piece = next((p for p in (botPawns if move_for == Player.OPP else oppPawns)
                                        if p.row == mid_row and p.col == mid_col), None)
                        if mid_piece:
                            new_node = self.create_new_node(piece, new_row, new_col, mid_piece)
                            children.append(new_node)
                            # Recursively check for further jumps
                            if self.botPieces == Piece.RED:
                                yP = new_node.board_state.red_pieces
                                oP = new_node.board_state.white_pieces
                            else:
                                yP = new_node.board_state.white_pieces
                                oP = new_node.board_state.red_pieces
                            self.find_jump_moves(new_node, yP[-1] if move_for == RED else oP[-1], move_for, children)

        return children

    def find_jump_moves(self, node:'BoardNode', piece, move_for:Player, children):
        # Determine possible directions based on whether the piece is a king
        if piece.is_king:
            directions = [-1, 1]  # Kings can move both forward and backward
        else:
            directions = [1] if (move_for == Player.YOU and self.botPieces == Piece.RED) or (move_for == Player.OPP and self.oppPieces == Piece.RED) else [-1]

        if move_for == Player.YOU:
            if self.botPieces == Piece.RED:
                botPawns = node.board_state.red_pieces
            else:
                botPawns = node.board_state.white_pieces
        else:
            if self.oppPieces == Piece.RED:
                oppPawns = node.board_state.red_pieces
            else:
                oppPawns = node.board_state.white_pieces

        for direction in directions:
            for dc in [-1, 1]:
                new_row, new_col = piece.row + 2 * direction, piece.col + 2 * dc
                mid_row, mid_col = piece.row + direction, piece.col + dc
                if self.is_within_bounds(new_row, new_col) and node.board_state.is_empty(new_row, new_col):
                    mid_piece = next((p for p in (botPawns if move_for == Player.YOU else oppPawns)
                                    if p.row == mid_row and p.col == mid_col), None)
                    if mid_piece:
                        new_node = node.create_new_node(piece, new_row, new_col, mid_piece)
                        children.append(new_node)
                        self.find_jump_moves(new_node, botPawns[-1] if move_for == Player.YOU else oppPawns[-1], move_for, children)

    def findPossibleMovesWithPruning(self, turn:Player, alpha:int = -INF, beta:int = INF) -> list:
            '''Generates possible moves for each node, applying alpha-beta pruning while generating'''
            possible_moves= []
            for move in self.findPossibleMoves(turn):
                move_score = move.evaluatePosition(turn)
                if turn:# maximizing player
                    if move_score>= beta:# if the move is so good that surpasses the best score the min player accepts
                        #the min player will not choose this move
                        break #prune the branch
                    alpha = max(alpha, move_score)
                else:#minimizing player
                    if move_score <= alpha:#if the move's score is so low that the max has a better option
                        #the maximizer will not choose this branch
                        break
                    beta = min (beta,move_score)
                possible_moves.append(move)
            return possible_moves

    def getBoardState(self) -> BoardState:
        return self.board_state

    def get_red_pieces(self):
        return self.board_state.red_pieces

    def get_white_pieces(self):
        return self.board_state.white_pieces

    def kingExists(self):
        for piece in self.board_state.red_pieces + self.board_state.white_pieces:
            if piece.is_king:
                return True
        return False

    def evaluatePosition(self, turn:Player) -> int:
        red_score = 0
        white_score = 0
        for piece in self.board_state.red_pieces:
            score = 1 #Basic value
            if piece.is_king:
                score += 2 #Kings are more valuable
            #If we are in a central position more valuable
            if 2<= piece.row <= 5 and 2<= piece.col <=5:
                score += 0.5
                red_score +=score

        for piece in self.board_state.white_pieces:
            score = 1
            if piece.is_king:
                score += 2
            if 2 <= piece.row <= 5 and 2 <= piece.col <= 5:
                score += 0.5
            white_score += score

        eval_score = red_score - white_score #possitive score is good for red, negative for white player
        if (turn == Player.OPP and self.oppPieces == Piece.RED) or (turn == Player.YOU and self.oppPieces == Piece.WHITE):
            eval_score *= -1
        return eval_score
    
    def is_terminal(self) -> bool:
        return self.__isTerminal
    
    def setTerminal(self) -> None:
        self.__isTerminal = True