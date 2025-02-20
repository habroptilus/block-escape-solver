import argparse
import glob
import os

import imageio.v2 as imageio
import matplotlib.pyplot as plt

from src.block import Block, Board, Cell, PositionList
from src.samples import sample_map
from src.solver import Solver

GRID_SIZE = 6


def get_color(block: Block) -> str:
    # ターゲットブロックは赤
    if block.is_target:
        return "red"
    return "gray"


def draw_board(positions: PositionList, step: int, total_steps: int, filepath: str):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, GRID_SIZE)
    ax.set_ylim(0, GRID_SIZE)
    ax.set_xticks(range(GRID_SIZE + 1))
    ax.set_yticks(range(GRID_SIZE + 1))
    ax.grid(True)

    for pos in positions:
        x = pos.cell.x
        y = pos.cell.y
        block = pos.block
        if block.orientation == "H":
            w, h = block.length, 1
        else:  # "V"
            w, h = 1, block.length
        ax.add_patch(
            plt.Rectangle(
                (x, y),
                w,
                h,
                facecolor=get_color(block),
                edgecolor="black",
                linewidth=5,
                alpha=0.8,
            )
        )

    ax.set_title(f"Step {step}/{total_steps}")
    plt.gca().invert_yaxis()

    plt.savefig(filepath)
    plt.close()
    return filepath


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Solution GIF")
    parser.add_argument(
        "--temp-dir",
        type=str,
        default="temp_images",
        help="Path for temporary images directory.",
    )
    parser.add_argument(
        "--output-gif",
        type=str,
        default="solution.gif",
        help="Path for the output GIF file.",
    )
    args = parser.parse_args()

    init_positions = PositionList(positions=sample_map["pro_12"])

    N = GRID_SIZE
    goal = Cell(x=5, y=2)

    board = Board(width=N, height=N, goal=goal, positions=init_positions)

    solver = Solver()
    best_moves = solver.run(board=board)

    if best_moves is None:
        print("No solution found.")
    else:
        print(f"Shortest moves: {len(best_moves)}")
        total_steps = len(best_moves)
        images = []
        os.makedirs(args.temp_dir, exist_ok=True)
        filepath = draw_board(
            init_positions, 0, total_steps, filepath=f"{args.temp_dir}/step_0.png"
        )
        images.append(imageio.imread(filepath))

        for step, move in enumerate(best_moves):
            board = board.apply_move(move)
            filepath = draw_board(
                board.positions,
                step + 1,
                total_steps,
                filepath=f"{args.temp_dir}/step_{step}.png",
            )
            images.append(imageio.imread(filepath))

        # GIFに変換
        imageio.mimsave(args.output_gif, images, fps=1)
        print(f"GIF saved as {args.output_gif}")

        # 一時画像を削除
        for filename in glob.glob(os.path.join(args.temp_dir, "*")):
            os.remove(filename)
        os.rmdir(args.temp_dir)
        print("Temporary images deleted.")
