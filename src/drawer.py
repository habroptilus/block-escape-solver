import os
import shutil
from pathlib import Path

import imageio.v2 as imageio
import matplotlib.pyplot as plt

from src.block import Block, Board, Move, PositionList


class GifDrawer:
    def __init__(self, grid_size: int, image_dir: Path, keep_images: bool):
        self.grid_size = grid_size
        self.image_dir = image_dir
        self.keep_images = keep_images

    def _get_color(self, block: Block) -> str:
        # ターゲットブロックは赤
        if block.is_target:
            return "red"
        return "gray"

    def _draw_snapshot(
        self,
        positions: PositionList,
        step: int,
        total_steps: int,
        filepath: str,
        next_move: Move | None = None,
    ):
        _, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(0, self.grid_size)
        ax.set_ylim(0, self.grid_size)
        ax.set_xticks(range(self.grid_size + 1))
        ax.set_yticks(range(self.grid_size + 1))
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
                    facecolor=self._get_color(block),
                    edgecolor="black",
                    linewidth=5,
                    alpha=0.8,
                )
            )
            # 動かすブロックの情報を取得
            if (next_move is not None) and (block.id == next_move.block.id):
                move_block = (x, y, w, h)

        # 矢印の描画（移動対象のブロックがある場合）
        if move_block:
            x, y, w, h = move_block
            center_x = x + (w / 2)
            center_y = y + (h / 2)

            # 矢印の終点を設定
            direction = next_move.get_direction()
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

    def run(self, board: Board, solutions: list[Move], output_filepath: str):
        total_steps = len(solutions)
        images = []
        os.makedirs(self.image_dir, exist_ok=True)

        for step, move in enumerate(solutions):
            filepath = self._draw_snapshot(
                board.positions,
                step,
                total_steps,
                filepath=self.image_dir / f"step_{step}.png",
                next_move=move,
            )
            images.append(imageio.imread(filepath))
            board = board.apply_move(move)

        # Last step
        filepath = self._draw_snapshot(
            board.positions,
            total_steps,
            total_steps,
            filepath=self.image_dir / f"step_{total_steps}.png",
        )
        images.append(imageio.imread(filepath))

        # GIFに変換
        imageio.mimsave(output_filepath, images, fps=1)
        print(f"GIF saved as {output_filepath}")

        if not self.keep_images:
            shutil.rmtree(self.image_dir)  # ディレクトリごと削除
