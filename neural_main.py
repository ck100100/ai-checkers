from Bot.NN import CheckersNet, train
from torch import torch



if __name__ == "__main__":
    # Initialize model and train
    print("Training the model...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CheckersNet().to(device)
    trained_model = train(model, device, episodes=1000)
    
    # Save final model
    torch.save(trained_model.state_dict(), "checkers_final.pth")
