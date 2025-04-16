 # Play a random game
    final_node, moves_made = play_random_game(root_node)
    print("Final Node:")
    print(final_node)
    print("\nMoves Made:")
    for i, move in enumerate(moves_made):
        print(f"Move {i}: {move}")
