#COMPLETELY OPTIONAL FILE
#This file gets an array of board states and displays them in a pygame window
#helped me debug the game logic
#Will be helpful for showcasing the game

#right arrow moves to next state, left to previous.
#

from Bot import *
import pygame
# from .BoardNode import BoardNode
# from .BoardState import BoardState

pygame.init()

# Constants, should be in constants.py
red = (255, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
gold = (212, 175, 55)
black = (0, 0, 0)

WIDTH = 800
WIDTH_OF_SCREEN = 1000
HEIGHT = 800

ROWS = 8
COLUMNS = 8
SQUARE_SIZE = WIDTH // COLUMNS

FPS = 24
#end of constants

WINDOW = pygame.display.set_mode((WIDTH_OF_SCREEN, HEIGHT))  # WIDTH_OF_SCREEN has extra space for stats
pygame.display.set_caption('Checkers')

FONT = pygame.font.SysFont('arial', 15)

class ReplayHandler:
    def __init__(self, replay_data = None):
        self.replay_data = replay_data
        self.current_move = 0
        self.window = WINDOW

        self.replay_active = True
        if not self.replay_data:
            self.waiting_screen()
        else:
            self.start_replay()

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
                    # print(f"Drew red square at ({row}, {col})")  # Debugging

    def draw_pieces(self):
        if not self.replay_data:
            return  # Exit if no data

        current_state = self.replay_data[self.current_move]

        # Draw red pieces
        for piece in current_state.getBoardState().red_pieces:
            x = piece.col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = piece.row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(self.window, gray, (x, y), 35)
            pygame.draw.circle(self.window, red, (x, y), 30)
            if piece.is_king:
                pygame.draw.circle(self.window, gold, (x, y), 15)
            # print(f"Drew red piece at ({piece.row}, {piece.col})")  # Debugging

        # Draw white pieces
        for piece in current_state.getBoardState().white_pieces:
            x = piece.col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = piece.row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(self.window, gray, (x, y), 35)
            pygame.draw.circle(self.window, white, (x, y), 30)
            if piece.is_king:
                pygame.draw.circle(self.window, gold, (x, y), 15)
            # print(f"Drew white piece at ({piece.row}, {piece.col})")  # Debugging

    def update(self):
        self.draw_board()
        pygame.display.update()

    def display_text(self):
        if not self.replay_data:
            return

        current_node = self.replay_data[self.current_move]
        current_state = current_node.getBoardState()

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

        key_held = None  # Tracks which key is being held down
        key_hold_timer = 0  # Timer to control the speed of scrolling

        while self.replay_active:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.replay_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        key_held = pygame.K_RIGHT
                        self.current_move = min(self.current_move + 1, len(self.replay_data) - 1)
                        self.update()
                    elif event.key == pygame.K_LEFT:
                        key_held = pygame.K_LEFT
                        self.current_move = max(self.current_move - 1, 0)
                        self.update()
                    elif event.key == pygame.K_a:
                        self.current_move = max(self.current_move - 1, 0)
                        self.update()
                    elif event.key == pygame.K_d:
                        self.current_move = min(self.current_move + 1, len(self.replay_data) - 1)
                        self.update()
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                        key_held = None

            # Handle key hold for rapid scrolling
            if key_held:
                key_hold_timer += 1
                if key_hold_timer >= FPS // 10:  # Adjust speed (e.g., 10 moves per second)
                    if key_held == pygame.K_RIGHT:
                        self.current_move = min(self.current_move + 1, len(self.replay_data) - 1)
                    elif key_held == pygame.K_LEFT:
                        self.current_move = max(self.current_move - 1, 0)
                    self.update()
                    key_hold_timer = 0  # Reset the timer

        pygame.quit()

    def set_replay_data(self, replay_data):
        self.replay_data = replay_data


    def waiting_screen(self):
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while not self.replay_data:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

            # Clear the screen
            self.window.fill(black)

            # Render and display the waiting text
            waiting_text = FONT.render("Waiting for replay data...", True, white)
            self.window.blit(waiting_text, (WIDTH // 2 - waiting_text.get_width() // 2, HEIGHT // 2 - waiting_text.get_height() // 2 - 20))

            # Render and display the elapsed time
            timer_text = FONT.render(f"Elapsed Time: {elapsed_time} seconds", True, white)
            self.window.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, HEIGHT // 2 - timer_text.get_height() // 2 + 20))

            # Update the display
            pygame.display.update()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Limit the frame rate
            clock.tick(FPS)