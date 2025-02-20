from src.block import Board, Cell
from src.samples import sample_map
from src.solver import Solver
from src.util import display_moves


def main():
    N = 6
    goal = Cell(x=5, y=2)

    init_positions = sample_map["pro_12"]

    board = Board(width=N, height=N, goal=goal, positions=init_positions)

    solver = Solver()
    best_moves = solver.run(board=board)

    if best_moves is None:
        print("No solution found.")
    else:
        print(f"Shortest moves: {len(best_moves)}")
        display_moves(best_moves)


if __name__ == "__main__":
    main()
