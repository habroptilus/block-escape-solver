import argparse
import os
import shutil
from pathlib import Path

import imageio.v2 as imageio
import matplotlib.pyplot as plt

from src.block import Block, Board, Cell, Move, PositionList
from src.solver import Solver
from upload_draft import upload_draft
from upload_image import upload_image

GRID_SIZE = 6


def get_color(block: Block) -> str:
    # ターゲットブロックは赤
    if block.is_target:
        return "red"
    return "gray"


def draw_board(
    positions: PositionList,
    step: int,
    total_steps: int,
    filepath: str,
    next_move: Move | None = None,
):
    _, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, GRID_SIZE)
    ax.set_ylim(0, GRID_SIZE)
    ax.set_xticks(range(GRID_SIZE + 1))
    ax.set_yticks(range(GRID_SIZE + 1))
    ax.grid(True)

    move_block = None

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
        # 動かすブロックの情報を取得
        if (next_move is not None) and (block.id == move.block.id):
            move_block = (x, y, w, h)

    # 矢印の描画（移動対象のブロックがある場合）
    if move_block:
        x, y, w, h = move_block
        center_x = x + (w / 2)
        center_y = y + (h / 2)

        # 矢印の終点を設定
        direction = move.get_direction()
        arrow_dx, arrow_dy = 0, 0
        if direction == "up":
            arrow_dy = -1
        elif direction == "down":
            arrow_dy = 1
        elif direction == "left":
            arrow_dx = -1
        elif direction == "right":
            arrow_dx = 1

        ax.annotate(
            "",
            xy=(center_x + arrow_dx, center_y + arrow_dy),
            xytext=(center_x, center_y),
            arrowprops=dict(
                facecolor="white", edgecolor="black", arrowstyle="->", lw=4
            ),
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
        "--input-dir",
        type=str,
        default="problems",
        help="Directory where the input Json file exists.",
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
        "--keep-images",
        action="store_true",
        help="If true, generated images will be keeped.",
    )

    args = parser.parse_args()
    input_filepath = Path(f"{args.input_dir}/{args.input_json}")

    # ファイルからJSON文字列を読み込む
    with open(input_filepath, "r", encoding="utf-8") as f:
        json_data = f.read()

    # JSON文字列を PositionList インスタンスに変換
    init_positions = PositionList.model_validate_json(json_data)

    N = GRID_SIZE
    goal = Cell(x=5, y=2)

    board = Board(width=N, height=N, goal=goal, positions=init_positions)

    # solve
    solver = Solver()
    best_moves = solver.run(board=board)

    project_name = input_filepath.stem
    output_filepath = f"{args.output_gif_dir}/{input_filepath.stem}.gif"

    if best_moves is None:
        print("No solution found.")
    else:
        print(f"Shortest moves: {len(best_moves)}")
        total_steps = len(best_moves)
        images = []
        image_dir = Path(f"{args.img_dir}/{project_name}")
        os.makedirs(image_dir, exist_ok=True)

        for step, move in enumerate(best_moves):
            filepath = draw_board(
                board.positions,
                step,
                total_steps,
                filepath=image_dir / f"step_{step}.png",
                next_move=move,
            )
            images.append(imageio.imread(filepath))
            board = board.apply_move(move)

        # Last step
        filepath = draw_board(
            board.positions,
            total_steps,
            total_steps,
            filepath=image_dir / f"step_{total_steps}.png",
        )
        images.append(imageio.imread(filepath))

        # GIFに変換
        imageio.mimsave(output_filepath, images, fps=1)
        print(f"GIF saved as {output_filepath}")

        if not args.keep_images:
            shutil.rmtree(image_dir)  # ディレクトリごと削除
            print(f"Deleted: {image_dir}")

        level, level_num = project_name.split("_")

        mapping = {
            "expert": "エキスパート",
            "pro": "プロ",
            "hard": "ハード",
            "master": "マスター",
        }
        if level not in mapping:
            print(f"{level} is not supported. So Uploading draft is skipped.")

        username = os.environ.get("HATENA_USER_NAME")
        api_key = os.environ.get("HATENA_API_KEY")
        image_path = "solutions/expert_1.gif"  # アップロードする画像のパス
        folder_name = "MyFolder"  # アップロード先フォルダ名（任意）

        # Upload
        print("Uploading Gif file...")
        image_url = upload_image(
            username=username,
            api_key=api_key,
            image_path=image_path,
            folder_name=folder_name,
        )
        print("Uploading blog post...")
        upload_draft(
            level=mapping[level], level_num=int(level_num), image_url=image_url
        )
