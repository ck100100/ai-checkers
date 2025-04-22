#COMPLETELY OPTIONAL FILE
#This file gets an array of board states and displays them in a pygame window
#helped me debug the game logic
#Will be helpful for showcasing the game

#right arrow moves to next state, left to previous.
#



import pygame
from utils.constants import *
from Bot.Game import CheckersGame
from Bot.BoardNode import BoardNode


# from .BoardNode import BoardNode
# from .BoardState import BoardState

pygame.init()

# Constants, should be in constants.py

#end of constants

WINDOW = pygame.display.set_mode((WIDTH_OF_SCREEN, HEIGHT))  # WIDTH_OF_SCREEN has extra space for stats
pygame.display.set_caption('Checkers')

FONT = pygame.font.SysFont('arial', 15)

class ReplayHandler:
    def __init__(self, replay_data):
        replay_data = self.load_replay_from_game()
        # self.replay_data = replay_data
        self.current_move = 0
        self.window = WINDOW

        self.replay_active = True
        # self.start_replay()

    def load_replay_from_game():
        """
        Simulate a game using CheckersGame and return the move history for replay.
        """
        game = CheckersGame()
        game.start_game()
        return game.move_history

    def test_board(self):
        self.window.fill(black)
        self.draw_squares()
        pygame.display.update()

    def draw_board(self):
        self.window.fill(black)  # Fill the background with black
        self.draw_squares()  # Draw the checkerboard squares
        self.draw_pieces()  # Draw the pieces
        self.display_text()  # Display text
        pygame.display.update()  # Refresh the display

    def draw_squares(self):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(self.window, red, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    print(f"Drew red square at ({row}, {col})")  # Debugging

    def draw_pieces(self):
        if not self.replay_data:
            return  # Exit if no data

        current_node = self.replay_data[self.current_move]
        current_state = current_node.board_state

        # Draw red pieces
        for piece in current_state.red_pieces:
            x = piece.col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = piece.row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(self.window, gray, (x, y), 35)
            pygame.draw.circle(self.window, red, (x, y), 30)
            if piece.is_king:
                pygame.draw.circle(self.window, gold, (x, y), 15)
            print(f"Drew red piece at ({piece.row}, {piece.col})")  # Debugging

        # Draw white pieces
        for piece in current_state.white_pieces:
            x = piece.col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = piece.row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(self.window, gray, (x, y), 35)
            pygame.draw.circle(self.window, white, (x, y), 30)
            if piece.is_king:
                pygame.draw.circle(self.window, gold, (x, y), 15)
            print(f"Drew white piece at ({piece.row}, {piece.col})")  # Debugging

    def update(self):
        self.draw_board()
        pygame.display.update()

    def display_text(self):
        if not self.replay_data:
            return

        current_node = self.replay_data[self.current_move]
        current_state = current_node.board_state

        texts = [
            f"RED's Pieces: {len(current_state.red_pieces)}",
            f"WHITE's Pieces: {len(current_state.white_pieces)}",
            f"RED's Kings: {sum(p.is_king for p in current_state.red_pieces)}",
            f"WHITE's Kings: {sum(p.is_king for p in current_state.white_pieces)}",
            f"Turn: {'WHITE' if self.current_move % 2 else 'RED'}"
        ]

        for i, text in enumerate(texts):
            text_surface = FONT.render(text, True, white)
            self.window.blit(text_surface, (WIDTH + 10, 10 + i * 30))

    def start_replay(self):
        clock = pygame.time.Clock()
        self.update()  # Initial draw

        while self.replay_active:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.replay_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.current_move = min(self.current_move + 1, len(self.replay_data) - 1)
                        self.update()
                    elif event.key == pygame.K_LEFT:
                        self.current_move = max(self.current_move - 1, 0)
                        self.update()

        pygame.quit()

    def testing_function(self):
        print(f"WHITE: {white}")  # Debug: Check the value of WHITE
        print(f"RED: {red}")      # Debug: Check the value of RED
        print(f"Window: {self.window}")  # Debug: Check if self.window is valid

        self.window.fill(black)
        pygame.draw.rect(self.window, red, (0, 0, 50, 50))  # (255, 0, 0) is red
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()