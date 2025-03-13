from Pawn import Pawn
# I know we  have a constants file. i will fix it later
BOARD_SIZE = 8
RED = 0
WHITE = 1

#this replaces BoardState.py. Every node IS a board state

class Node:
    def __init__(self, red_pieces, white_pieces, parent=None):
        #board state info
        self.red_pieces = red_pieces
        self.white_pieces = white_pieces
        
        #regular tree stuff
        self.parent = parent
        self.children = [] 

        self.score = 0 #unused for the time being

    #used for debugging
    def __str__(self):
        red_positions = [(piece.row, piece.col, piece.is_king) for piece in self.red_pieces]
        white_positions = [(piece.row, piece.col, piece.is_king) for piece in self.white_pieces]
        return f"Node(Red: {red_positions}, White: {white_positions})"

    #used for movement checks
    def is_within_bounds(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def is_empty(self, row, col, node):
        return not any(piece.row == row and piece.col == col for piece in node.red_pieces + node.white_pieces)


    #method to generalize node creation
    def create_new_node(self, node, moved_piece, new_row, new_col, captured_piece=None):
        new_red_pieces = [piece.copy() for piece in node.red_pieces]
        new_white_pieces = [piece.copy() for piece in node.white_pieces]

        #spaggetti code to move a piece. can be improved with each pawn checking if it should be promoted
        # Check if the moved piece should be promoted to a king
        if new_row == BOARD_SIZE - 1 and moved_piece in new_red_pieces and not moved_piece.is_king:
            # Red piece reaches the last row and becomes a king
            new_red_pieces.remove(moved_piece)
            new_red_pieces.append(Pawn(new_row, new_col, is_king=True))
        elif new_row == 0 and moved_piece in new_white_pieces and not moved_piece.is_king:
            # White piece reaches the last row and becomes a king
            new_white_pieces.remove(moved_piece)
            new_white_pieces.append(Pawn(new_row, new_col, is_king=True))
        else:
            # Regular move or jump
            if moved_piece in new_red_pieces:
                new_red_pieces.remove(moved_piece)
                new_red_pieces.append(Pawn(new_row, new_col, moved_piece.is_king))
            else:
                new_white_pieces.remove(moved_piece)
                new_white_pieces.append(Pawn(new_row, new_col, moved_piece.is_king))

        # Remove captured piece if any
        if captured_piece:
            if captured_piece in new_red_pieces:
                new_red_pieces.remove(captured_piece)
            else:
                new_white_pieces.remove(captured_piece)

        return Node(new_red_pieces, new_white_pieces, node)

    #here is the big one. This method finds all possible normal moves and single jumps for a given node
    def findPossibleMoves(self, node, move_for):
        children = []
        pieces = node.red_pieces if move_for == RED else node.white_pieces

        for piece in pieces:
            # Determine possible directions based on whether the piece is a king
            if piece.is_king:
                directions = [-1, 1]  # Kings can move both forward and backward
            else:
                directions = [1] if move_for == RED else [-1]  # Regular pieces move forward only

            for direction in directions:
                # Normal moves
                for dc in [-1, 1]:  # Check both left and right diagonals
                    new_row, new_col = piece.row + direction, piece.col + dc
                    if self.is_within_bounds(new_row, new_col) and self.is_empty(new_row, new_col, node):
                        new_node = self.create_new_node(node, piece, new_row, new_col)
                        children.append(new_node)
                        
                        print("found a normal move from", piece.row, piece.col, "to", new_row, new_col)

                # Jump moves
                for dc in [-1, 1]:
                    new_row, new_col = piece.row + 2 * direction, piece.col + 2 * dc
                    mid_row, mid_col = piece.row + direction, piece.col + dc
                    if self.is_within_bounds(new_row, new_col) and self.is_empty(new_row, new_col, node):
                        mid_piece = next((p for p in (node.red_pieces if move_for == WHITE else node.white_pieces)
                                        if p.row == mid_row and p.col == mid_col), None)
                        if mid_piece:
                            new_node = self.create_new_node(node, piece, new_row, new_col, mid_piece)
                            children.append(new_node)
                            print("found a jump move from", piece.row, piece.col, "to", new_row, new_col)
                            # Recursively check for further jumps
                            self.find_jump_moves(new_node, new_node.red_pieces[-1] if move_for == RED else new_node.white_pieces[-1], move_for, children)

        return children

    #is called recursively for extra jumps
    def find_jump_moves(self, node, piece, move_for, children):
        # Determine possible directions based on whether the piece is a king
        if piece.is_king:
            directions = [-1, 1]  # Kings can move both forward and backward
        else:
            directions = [1] if move_for == RED else [-1]  # Regular pieces move forward only

        for direction in directions:
            for dc in [-1, 1]:
                new_row, new_col = piece.row + 2 * direction, piece.col + 2 * dc
                mid_row, mid_col = piece.row + direction, piece.col + dc
                print("checking for jump move from", piece.row, piece.col, "to", new_row, new_col)
                if self.is_within_bounds(new_row, new_col) and self.is_empty(new_row, new_col, node):
                    mid_piece = next((p for p in (node.red_pieces if move_for == WHITE else node.white_pieces)
                                    if p.row == mid_row and p.col == mid_col), None)
                    print("mid_piece", mid_piece, "at", mid_row, mid_col)
                    if mid_piece:
                        new_node = self.create_new_node(node, piece, new_row, new_col, mid_piece)
                        children.append(new_node)
                        print("found an extra jump move from", piece.row, piece.col, "to", new_row, new_col)
                        # Recursively check for further jumps
                        self.find_jump_moves(new_node, new_node.red_pieces[-1] if move_for == RED else new_node.white_pieces[-1], move_for, children)

    #dummy methods i needed to check stuff
    def get_red_pieces(self):
        return self.red_pieces
        
    def get_white_pieces(self):
        return self.white_pieces
        
    def kingExists(self, node):
        for piece in node.red_pieces + node.white_pieces:
            if piece.is_king:
                return True
        return False
        

