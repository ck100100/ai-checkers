# we are definitely not using a main like that
# this serves as a dump for functions that could be in main or a future bot of ours
# also showcases the replay viewer


import random
from Bot.replay_viewer import ReplayHandler
from Bot.BoardNode import BoardNode
from Bot.BoardState import BoardState
from Bot.Pawn import Pawn
from Bot.GameInterface import GameInterface
from Bot.Bot import BotMinMaxAB
from utils.types import Piece
from Bot.NN import NNBot

# looks like a Node class method. could be moved there
def initialize_starting_positions():
    starting_red_pieces = [Pawn(row, col) for row, col in [(0, 0), (0, 2), (0, 4), (0, 6), (1, 1), (1, 3), (1, 5), (1, 7), (2, 0), (2, 2), (2, 4), (2, 6)]]
    starting_white_pieces = [Pawn(row, col) for row, col in [(5, 1), (5, 3), (5, 5), (5, 7), (6, 0), (6, 2), (6, 4), (6, 6), (7, 1), (7, 3), (7, 5), (7, 7)]]
    return starting_red_pieces, starting_white_pieces

# Test case for a backward jump
# kept it as a dummy function if we need to check more things
def test_backward_jump():
    red_king = Pawn(5, 3, is_king=True)
    white_piece = Pawn(4, 2)
    starting_red_pieces = [red_king]
    starting_white_pieces = [white_piece, Pawn(2, 2)]
    return starting_red_pieces, starting_white_pieces


# Initializes the board and moves pieces randomly until it makes a king
# move_for indicates wether it is a move for white or red. could be implemented better (odd moves are white, even are red) but my brain is fried rn
def play_random_game(node, move_for=0):
    moves_made = [node]
    while not node.kingExists():
        children = node.findPossibleMoves(move_for)
        if not children:
            break
        node = random.choice(children)
        moves_made.append(node)
        move_for = 1 - move_for
    return node, moves_made    

if __name__ == "__main__":
    # main()
    # GameInterface()

    # minmax opponents
    # bot1 = BotMinMaxAB(Piece.RED, 3)
    bot1 = BotMinMaxAB(Piece.RED, 5)

    # nn opponents you can also set the nn's data path
    bot2 = NNBot(Piece.WHITE) 
    # bot2 = NNBot(Piece.WHITE)

    turn_counter = 1
    turn_end=3000
    gameEnded:bool = False
    move = bot1.getBotMove(None)
    stateHistory = [move]
    while not gameEnded:
        turn_counter += 1
        move = bot2.getBotMove(move)
        if move != None:
            move.setTurnNumber(turn_counter)
            stateHistory.append(move)
        elif move == None or turn_counter > 3000:
            gameEnded = True

        turn_counter += 1
        move = bot1.getBotMove(move)
        if move != None:
            move.setTurnNumber(turn_counter)
            stateHistory.append(move)
        elif move == None or turn_counter > 3000:
            gameEnded = True
        
    replay_handler = ReplayHandler(stateHistory)