import argparse
from pathlib import Path

from block_escape_solver_api.src.block import Board, Cell, PositionList
from block_escape_solver_api.src.drawer import GifDrawer
from block_escape_solver_api.src.solver import Solver

GRID_SIZE = 6

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
    image_dir = Path(f"{args.img_dir}/{project_name}")

    # draw
    if best_moves is None:
        print("No solution found.")
    else:
        print(f"Shortest moves: {len(best_moves)}")
        drawer = GifDrawer(
            grid_size=GRID_SIZE, image_dir=image_dir, keep_images=args.keep_images
        )
        drawer.run(board=board, solutions=best_moves, output_filepath=output_filepath)
