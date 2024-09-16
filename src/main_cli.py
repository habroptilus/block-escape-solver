from block import Block, Board, Cell, Position
from solver import Solver
from util import display_moves


def main():
    N = 6
    goal = Cell(x=5, y=2)

    # init_positions = sample_map["pro_12"]

    # board = Board(width=N, height=N, goal=goal, positions=init_positions)
    board = Board(
        width=6,
        height=6,
        goal=Cell(y=2, x=5),
        positions=[
            Position(
                cell=Cell(y=2, x=0),
                block=Block(id=0, orientation="H", length=2, is_target=False),
            ),
            Position(
                cell=Cell(y=0, x=4),
                block=Block(id=1, orientation="H", length=2, is_target=False),
            ),
            Position(
                cell=Cell(y=4, x=2),
                block=Block(id=2, orientation="H", length=2, is_target=False),
            ),
            Position(
                cell=Cell(y=3, x=1),
                block=Block(id=3, orientation="V", length=2, is_target=False),
            ),
            Position(
                cell=Cell(y=1, x=4),
                block=Block(id=4, orientation="V", length=2, is_target=False),
            ),
            Position(
                cell=Cell(y=3, x=4),
                block=Block(id=5, orientation="V", length=2, is_target=False),
            ),
        ],
    )
    solver = Solver()
    best_moves = solver.run(board=board)

    if best_moves is None:
        print("No solution found.")
    else:
        print(f"Shortest moves: {len(best_moves)}")
        display_moves(best_moves)


if __name__ == "__main__":
    main()
