from Pawn import Pawn

class BoardState:
    """
    This will be used in order to represent all the
    pieces on the board
    """
    def __init__(self):
        self.friendlyPawns: list[Pawn] = []
        self.enemyPawns: list[Pawn] = []

    def findPossibleFriendlyMoves(self):
        """
        Returns a list of all the possible moves that
        the friendly player can make.
        """
        pass

    def findPossibleEnemyMoves(self):
        """
        Returns a list of all the possible moves that
        an enemy player can make.
        """
        pass