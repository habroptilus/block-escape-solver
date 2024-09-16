from block import Board, Cell, Move
from samples import sample_map
from solver import Solver


def display_moves(moves: list[Move]) -> None:
    for move in moves:
        print(f"{move.from_cell} -> {move.to_cell} (Block: {move.block})")


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
