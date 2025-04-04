
class BoardState:
    """
    This IS used in order to represent all the
    pieces on the board
    """
    def __init__(self, red_pieces, white_pieces):
        self.red_pieces = red_pieces
        self.white_pieces = white_pieces #REMEMBER: these are lists of tuples

    def is_empty(self, row, col):
        return not any(piece.row == row and piece.col == col for piece in self.red_pieces + self.white_pieces)
    
    def copy(self):
        new_red_pieces = [piece.copy() for piece in self.red_pieces]
        new_white_pieces = [piece.copy() for piece in self.white_pieces]
        return BoardState(new_red_pieces, new_white_pieces)