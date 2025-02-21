import argparse
import os
import shutil
from pathlib import Path

import imageio.v2 as imageio
import matplotlib.pyplot as plt

from src.block import Block, Board, Cell, PositionList
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
        "input_json",
        type=str,
        help="Path for the input Json file.",
    )
    parser.add_argument(
        "--img-dir",
        type=str,
        default="images",
        help="Path for temporary images directory.",
    )
    parser.add_argument(
        "--output-gif-dir",
        type=str,
        default="solutions",
        help="Path for the output GIF file directory.",
    )
    parser.add_argument(
        "--delete-images",
        action="store_true",
        help="If true, generated images will be deleted after generating gif file.",
    )

    args = parser.parse_args()
    # ファイルからJSON文字列を読み込む
    with open(args.input_json, "r", encoding="utf-8") as f:
        json_data = f.read()

    # JSON文字列を PositionList インスタンスに変換
    init_positions = PositionList.model_validate_json(json_data)

    N = GRID_SIZE
    goal = Cell(x=5, y=2)

    board = Board(width=N, height=N, goal=goal, positions=init_positions)

    solver = Solver()
    best_moves = solver.run(board=board)
    input_filepath = Path(args.input_json)
    project_name = input_filepath.stem

    if best_moves is None:
        print("No solution found.")
    else:
        print(f"Shortest moves: {len(best_moves)}")
        total_steps = len(best_moves)
        images = []
        image_dir = Path(f"{args.img_dir}/{project_name}")
        os.makedirs(image_dir, exist_ok=True)
        filepath = draw_board(
            init_positions, 0, total_steps, filepath=image_dir / "step_0.png"
        )
        images.append(imageio.imread(filepath))

        for step, move in enumerate(best_moves):
            board = board.apply_move(move)
            filepath = draw_board(
                board.positions,
                step + 1,
                total_steps,
                filepath=image_dir / f"step_{step}.png",
            )
            images.append(imageio.imread(filepath))

        output_filepath = f"{args.output_gif_dir}/{input_filepath.stem}.gif"
        # GIFに変換
        imageio.mimsave(output_filepath, images, fps=1)
        print(f"GIF saved as {output_filepath}")

        if args.delete_images:
            shutil.rmtree(image_dir)  # ディレクトリごと削除
            print(f"Deleted: {image_dir}")
