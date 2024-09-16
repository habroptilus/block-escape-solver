from block import Board, Cell, find_shortest_path_to_clear
from samples import sample_map

if __name__ == "__main__":
    N = 6
    goal = Cell(x=5, y=2)

    init_positions = sample_map["basic_01"]

    board = Board(width=N, height=N, goal=goal, positions=init_positions)
    board.display_board()

    best_moves = find_shortest_path_to_clear(board=board)

    if best_moves is None:
        print("No solution found.")
    else:
        print(f"Short moves: {len(best_moves)}")
        print(best_moves)
