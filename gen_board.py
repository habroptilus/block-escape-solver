import json
import tkinter as tk
from tkinter import filedialog

from src.block import Block, Cell, Position, PositionList

BLOCK_SIZE = 50
BOARD_SIZE = 6


class BlockPuzzleGUI:
    def __init__(self, root):
        self.block_id = 0
        self.root = root
        self.root.title("Block Puzzle")
        self.canvas = tk.Canvas(
            root, width=600, height=700, bg="white"
        )  # 画面サイズを適切に変更
        self.canvas.grid(row=0, column=0)
        self.blocks = []
        self.selected_block = None
        self.draw_grid()
        self.create_block_palette()
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.place_block)
        self.create_get_positions_button()  # ボタンを追加

    def draw_grid(self):
        for i in range(BOARD_SIZE + 1):
            self.canvas.create_line(
                i * BLOCK_SIZE, 0, i * BLOCK_SIZE, BOARD_SIZE * BLOCK_SIZE, fill="black"
            )
            self.canvas.create_line(
                0, i * BLOCK_SIZE, BOARD_SIZE * BLOCK_SIZE, i * BLOCK_SIZE, fill="black"
            )

    def create_get_positions_button(self):
        button = tk.Button(
            self.root, text="Save as json", command=self.get_position_list
        )
        button.grid(row=1, column=0, pady=10)

    def get_position_list(self):
        position_list = PositionList(positions=self.blocks)
        data = position_list.model_dump_json(indent=2)

        # ユーザーに保存先を選ばせる
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All Files", "*.*")],
            title="Save JSON File",
        )

        if filepath:  # キャンセルされなかった場合のみ保存
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(json.loads(data), f, indent=2, ensure_ascii=False)
            print(f"Saved to {filepath}")

    def create_block_palette(self):
        self.palette_blocks = []
        self.target_block_added = False  # ターゲットブロックが配置されたか

        # 横向きブロック（画面下部）
        horizontal_blocks = [
            (0, "H", 2, False),
            (1, "H", 3, False),
            (2, "H", 2, True),  # ターゲットブロック
        ]
        for i, (id, orientation, length, is_target) in enumerate(horizontal_blocks):
            block = Block(
                id=id, orientation=orientation, length=length, is_target=is_target
            )
            self.palette_blocks.append(block)
            x1, y1 = BLOCK_SIZE + i * 160, 550  # 位置を調整
            x2 = x1 + BLOCK_SIZE * length
            y2 = y1 + BLOCK_SIZE
            color = "red" if is_target else "gray"
            self.canvas.create_rectangle(
                x1, y1, x2, y2, fill=color, tags=f"palette_{id}"
            )

        # 縦向きブロック（画面右側）
        vertical_blocks = [(0, "V", 2, False), (1, "V", 3, False)]
        for i, (id, orientation, length, is_target) in enumerate(vertical_blocks):
            block = Block(
                id=id, orientation=orientation, length=length, is_target=is_target
            )
            self.palette_blocks.append(block)
            x1, y1 = 450, BLOCK_SIZE + i * 150  # 位置を調整
            x2 = x1 + BLOCK_SIZE
            y2 = y1 + BLOCK_SIZE * length
            self.canvas.create_rectangle(
                x1, y1, x2, y2, fill="gray", tags=f"palette_{id}"
            )

    def on_drag(self, event):
        if self.selected_block:
            self.canvas.delete("drag")
            x, y = event.x, event.y
            length = self.selected_block.length * BLOCK_SIZE
            color = "red" if self.selected_block.is_target else "gray"
            if self.selected_block.orientation == "H":
                self.canvas.create_rectangle(
                    x, y, x + length, y + BLOCK_SIZE, fill=color, tags="drag"
                )
            else:
                self.canvas.create_rectangle(
                    x, y, x + BLOCK_SIZE, y + length, fill=color, tags="drag"
                )

    def start_drag(self, event):
        for block in self.palette_blocks[:]:
            if block.orientation == "H":
                x1, y1 = BLOCK_SIZE + block.id * 150, 550
                x2 = x1 + BLOCK_SIZE * block.length
                y2 = y1 + BLOCK_SIZE
            else:
                x1, y1 = 450, BLOCK_SIZE + block.id * 150
                x2 = x1 + BLOCK_SIZE
                y2 = y1 + BLOCK_SIZE * block.length

            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.selected_block = block
                if block.is_target:
                    self.palette_blocks.remove(block)  # ターゲットブロックは1回のみ
                    self.canvas.delete(f"palette_{block.id}")
                return

    def place_block(self, event):
        if self.selected_block:
            delta = 10  # ポイントしているところより少し右下に判定がくるようにする
            x, y = (event.x + delta) // BLOCK_SIZE, (event.y + delta) // BLOCK_SIZE

            if x < BOARD_SIZE and y < BOARD_SIZE:  # マス目の範囲内のみ配置
                self.blocks.append(
                    Position(
                        cell=Cell(y=y, x=x),
                        block=Block(
                            id=self.block_id,
                            orientation=self.selected_block.orientation,
                            length=self.selected_block.length,
                            is_target=self.selected_block.is_target,
                        ),
                    )
                )
                self.block_id += 1
                self.selected_block = None
                self.canvas.delete("drag")
                self.draw_blocks()

    def draw_blocks(self):
        self.canvas.delete("blocks")
        for position in self.blocks:
            x, y = position.cell.x * BLOCK_SIZE, position.cell.y * BLOCK_SIZE
            length = position.block.length * BLOCK_SIZE
            color = "red" if position.block.is_target else "gray"
            if position.block.orientation == "H":
                self.canvas.create_rectangle(
                    x, y, x + length, y + BLOCK_SIZE, fill=color, tags="blocks"
                )
            else:
                self.canvas.create_rectangle(
                    x, y, x + BLOCK_SIZE, y + length, fill=color, tags="blocks"
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = BlockPuzzleGUI(root)
    root.mainloop()
