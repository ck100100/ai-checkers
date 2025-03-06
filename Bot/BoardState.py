from Pawn import Pawn

class BoardState:
    """
    This will be used in order to represent all the
    pieces on the board
    """
    def __init__(self):
        self.friendlyPawns: list[Pawn] = []
        self.hostilePawns: list[Pawn] = []