# we are definitely not using a main like that
# this serves as a dump for functions that could be in main or a future bot of ours
# also showcases the replay viewer


import random
from Bot.replay_viewer import ReplayHandler
from Bot.BoardNode import BoardNode
from Bot.BoardState import BoardState
from Bot.Pawn import Pawn

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

# basic main that initializes everything and plays a random game
def main():
    # Initialize starting positions
    print("i exist")
    starting_red_pieces, starting_white_pieces = initialize_starting_positions()

    # Create the initial BoardState
    initial_board_state = BoardState(starting_red_pieces, starting_white_pieces)

    # Create the root node
    root_node = BoardNode(initial_board_state)

    # Play a random game
    final_node, moves_made = play_random_game(root_node)
    print("Final Node:")
    print(final_node)
    print("\nMoves Made:")
    for i, move in enumerate(moves_made):
        print(f"Move {i}: {move}")

    # Initialize the replay handler
    replayHandler = ReplayHandler(moves_made)

    # Start the replay
    replayHandler.start_replay()
    #replayHandler.testing_function()

if __name__ == "__main__":
    main()



