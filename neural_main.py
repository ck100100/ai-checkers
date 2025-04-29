from Bot.NN import CheckersNet, train
from torch import torch



if __name__ == "__main__":
    # Initialize model and train
    print("Training the model...")
    model = CheckersNet()
    trained_model = train(model, episodes=1000)
    
    # Save final model
    torch.save(trained_model.state_dict(), "checkers_final.pth")

    #des line 70 xreiazomai to findPossibleMoves kai line 96 na checkarw pote teleiwnei to game