import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from collections import deque, defaultdict
from .BoardNode import BoardNode
from .BoardState import BoardState

from utils.types import Coordinates, Piece


# 1. Neural Network Architecture

class CheckersNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(5, 16, kernel_size=3, padding=1)  # 5 input channels
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * 8 * 8, 128)
        self.fc2 = nn.Linear(128, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))  # (batch, 16, 8, 8)
        x = F.relu(self.conv2(x))  # (batch, 32, 8, 8)
        x = x.view(x.size(0), -1)  # (batch, 32*8*8)
        x = F.relu(self.fc1(x))    # (batch, 128)
        return torch.tanh(self.fc2(x))  # (batch, 1)

# 2. Game State Utilities

def board_to_tensor(red_pieces, white_pieces, current_player):
    """Create 5-channel tensor from board state"""
    tensor = torch.zeros(5, 8, 8)
    
    # Red pieces (channel 0) and kings (channel 1)


    for pawn in red_pieces:
        x, y = pawn.row, pawn.col
        tensor[0, x, y] = 1
        if pawn.is_king:
            tensor[1, x, y] = 1
    
    for pawn in white_pieces:
        x, y = pawn.row, pawn.col
        tensor[2, x, y] = 1
        if pawn.is_king:
            tensor[3, x, y] = 1
            tensor[3, x, y] = 1
    
    # Turn channel (channel 4)
    tensor[4] = 1.0 if current_player == Piece.RED else 0.0
    
    return tensor

def is_draw_by_repetition(state, state_counter, threshold=3):
    """Check for repeated board states"""
    state_counter[state] += 1
    return state_counter[state] >= threshold


# 3. Self-Play

def play_game(model, epsilon=0.1, device):
    """Generate a game through self-play"""
    # Initialize game state
    # red_pieces = [(x, y, False) for x in range(3) for y in range(8) if (x + y) % 2 == 1]
    # white_pieces = [(x, y, False) for x in range(5, 8) for y in range(8) if (x + y) % 2 == 1]
    startingBoardState = BoardState(None, None, Piece.RED)
    currentBoardNode = BoardNode(startingBoardState, Piece.RED)
    current_player = Piece.RED
    tensorhistory = []
    boardHistory = []
    state_counter = defaultdict(int)
    turn_counter = 1
    
    while True:
        #print("turn: ", turn_counter)
        moves = currentBoardNode.findPossibleMoves(move_for = current_player)
        tensor_list = []
        if moves:
            # Convert moves to tensors with current player
            for move in moves:
                red_pieces = move.getBoardState().red_pieces
                white_pieces = move.getBoardState().white_pieces
                tensor = board_to_tensor(red_pieces, white_pieces, current_player)
                tensor_list.append(tensor)
            #tensor batch
            move_tensors = torch.stack(tensor_list).to(device)
            
            # Choose move using epsilon-greedy strategy
            if np.random.rand() < epsilon:
                chosen_idx = np.random.choice(len(moves))
            else:
                with torch.no_grad():
                    values = model(move_tensors)
                    chosen_idx = values.argmax().item()
            
            # Apply the chosen move
            currentBoardNode = moves[chosen_idx]
            tensorhistory.append((move_tensors[chosen_idx], current_player))
            boardHistory.append(currentBoardNode)

        else:
            currentBoardNode.setTerminal()

        if currentBoardNode.is_terminal():
            winner = Piece.WHITE if current_player == Piece.RED else Piece.RED
            break
        if is_draw_by_repetition(currentBoardNode, state_counter):
            winner = "draw"
            break
            
        current_player = Piece.WHITE if current_player == Piece.RED else Piece.RED
        turn_counter += 1
        print("winner: ", winner)


    return tensorhistory, winner

# 4. Training and Experience Replay

class ExperienceReplay:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
    
    def add(self, states, targets):
        self.buffer.extend(zip(states, targets))
    
    def sample(self, batch_size):
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        return [self.buffer[i] for i in indices]

def train(model, episodes=1000, batch_size=32):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    replay = ExperienceReplay()
    epsilon = 1.0
    min_epsilon = 0.01
    epsilon_decay = 0.995
    
    for episode in range(episodes):
        # Generate game data
        print(f"Episode {episode + 1}/{episodes}")
        game_history, winner = play_game(model, epsilon)
        states = torch.stack([s for s, _ in game_history])
        targets = torch.tensor([
            1.0 if p == winner else (-1.0 if winner != "draw" else 0.0)
            for _, p in game_history
        ], dtype=torch.float32)
        
        # Store experience
        replay.add(states, targets)
        
        # Training phase
        if len(replay.buffer) >= batch_size:
            batch = replay.sample(batch_size)
            batch_states = torch.stack([s for s, _ in batch]).to(device)
            batch_targets = torch.stack([t for _, t in batch]).to(device)
            
            optimizer.zero_grad()
            predictions = model(batch_states).squeeze()
            loss = F.mse_loss(predictions, batch_targets)
            loss.backward()
            optimizer.step()
        
        # Decay exploration
        epsilon = max(epsilon * epsilon_decay, min_epsilon)
        
        # Save checkpoint
        if episode % 100 == 0:
            torch.save(model.state_dict(), f"checkers_{episode}.pth")
    
    return model

# if __name__ == "__main__":
#     # Initialize model and train
#     model = CheckersNet()
#     trained_model = train(model, episodes=1000)
    
#     # Save final model
#     torch.save(trained_model.state_dict(), "checkers_final.pth")

#     #des line 70 xreiazomai to findPossibleMoves kai line 96 na checkarw pote teleiwnei to game