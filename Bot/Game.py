from Bot.BoardState import BoardState
from Bot.BoardNode import BoardNode
from Bot.Bot import BotMinMaxAB
from utils.constants import WHITE, RED

class CheckersGame:
    def __init__(self):
        """
        Initialize the game with both players as bots.
        RED moves first (currently_moving = True)
        """
        self.players = {
            RED: {"type": "bot", "name": "Red Bot", "bot": BotMinMaxAB(color=RED)},
            WHITE: {"type": "bot", "name": "White Bot", "bot": BotMinMaxAB(color=WHITE)}
        }
        self.turn_count = 0
        self.currently_moving = RED  # RED (True) moves first
        self.board = BoardState()
        self.move_history = [BoardNode(self.board.copy())]

    def start_game(self):
        """Start the game and manage turns."""
        print("Starting the game of Checkers!")
        print(f"Initial turn: {'WHITE' if self.currently_moving else 'RED'}")
        
        while not self.is_game_over():
            self.play_turn()
            self.switch_turn()
            self.turn_count += 1
        print(f"Game over after {self.turn_count} turns!")

    def play_turn(self):
        """Handle the current player's turn."""
        current_player = self.players[self.currently_moving]
        print(f"\nTurn {self.turn_count + 1}: {current_player['name']}'s turn")
        
        # Get the bot's move
        move_node = current_player["bot"].getBotMove(self.currently_moving)
        
        # Update the board with the move
        self.board = move_node.board_state.copy()
        self.move_history.append(BoardNode(self.board.copy()))
        
        print(f"Board after move:")
        self.print_board()

    def is_game_over(self):
        """Check if the game is over."""
        root_node = BoardNode(self.board.copy())
        root_node.boardStatesTree(self.currently_moving, 1)
        
        if not root_node.children or self.turn_count >= 100:
            print(f"{self.players[self.currently_moving]['name']} has no valid moves left!")
            return True
            
        return False

    def switch_turn(self):
        """Switch to the other player's turn."""
        self.currently_moving = not self.currently_moving  # Toggle between RED (True) and WHITE (False)
