from Bot.Game import CheckersGame
from Bot.replay_viewer import ReplayHandler


def main():
    # Run the game
    game = CheckersGame()
    game.start_game()

    # Pass the replay data to the replay viewer
    replay_handler = ReplayHandler(game.move_history)
    replay_handler.start_replay()

if __name__ == "__main__":
    main()