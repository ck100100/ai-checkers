from Bot.NN import CheckersNet, train
from torch import torch
from Bot.replay_viewer import ReplayHandler



if __name__ == "__main__":
    # Initialize model and train
    print("Training the model...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CheckersNet().to(device)
    trained_model, final_played_game = train(model, device, episodes=1)
    
    # Save final model
    torch.save(trained_model.state_dict(), "checkers_final.pth")

    # workaround for pygame not responding error as model is training

    # see last game
    replay_data = final_played_game
    replay_handler = ReplayHandler(replay_data)




