from typing import Any, Literal

from pydantic import BaseModel


class Block(BaseModel):
    id: int
    orientation: Literal["V", "H"]
    length: int
    is_target: bool = False


class Cell(BaseModel):
    y: int
    x: int


class Position(BaseModel):
    cell: Cell
    block: Block


class Move(BaseModel):
    block: Block
    from_cell: Cell
    to_cell: Cell
    # TODO: validate moves.


class Board(BaseModel):
    width: int
    height: int
    goal: Cell
    positions: list[Position]
    cells_occupancy: list[list[bool]] | None = None

    def model_post_init(self, __context: Any) -> None:
        self._init_occupancy()

    def _init_occupancy(self) -> None:
        cells_occupancy = [
            [False for _ in range(self.width)] for _ in range(self.height)
        ]

        for position in self.positions:
            cell = position.cell
            block = position.block
            for i in range(block.length):
                if block.orientation == "H":
                    is_target_cell_occupied = cells_occupancy[cell.y][cell.x + i]
                    if is_target_cell_occupied:
                        raise Exception("The cell is already occupied.")
                    cells_occupancy[cell.y][cell.x + i] = True
                elif block.orientation == "V":
                    is_target_cell_occupied = cells_occupancy[cell.y + i][cell.x]
                    if is_target_cell_occupied:
                        raise Exception("The cell is already occupied.")
                    cells_occupancy[cell.y + i][cell.x] = True

        self.cells_occupancy = cells_occupancy

    def display_board(self) -> None:
        if self.cells_occupancy is None:
            print("Board is not initialized. Please call init_occupancy() first.")
            return

        print("--------------------")
        for row in self.cells_occupancy:
            print(" ".join("X" if cell else "." for cell in row))
        print("--------------------")

    def calculate_available_moves(self) -> list[Move]:
        """移動可能なブロックの最終位置をリストするメソッド"""
        available_moves = []

        for position in self.positions:
            cell = position.cell
            block = position.block
            to_cells = self._get_to_cells(cell, block)
            for to_cell in to_cells:
                available_moves.append(
                    Move(from_cell=cell, to_cell=to_cell, block=block)
                )

        return available_moves

    def is_cleared(self) -> bool:
        """ゲームがクリアされているかどうかを判定するメソッド"""
        for position in self.positions:
            if not position.block.is_target:
                continue
            cell = position.cell
            block = position.block

            # ブロックの範囲を計算
            if block.orientation == "H":
                block_cells = [(cell.x + i, cell.y) for i in range(block.length)]
            elif block.orientation == "V":
                block_cells = [(cell.x, cell.y + i) for i in range(block.length)]

            # goalがブロックの範囲内にあるか確認
            if (self.goal.x, self.goal.y) in block_cells:
                return True

        return False

    def _get_to_cells(self, cell, block) -> list[Cell]:
        to_cells = []
        if block.orientation == "H":
            # 水平方向に移動
            # 左に移動可能な最終位置を探す
            left = cell.x
            while left > 0 and not self.cells_occupancy[cell.y][left - 1]:
                left -= 1
            if left < cell.x:  # もし移動した場合
                to_cells.append(Cell(y=cell.y, x=left))

            # 右に移動可能な最終位置を探す
            original_block_right_end = cell.x + block.length - 1
            right = original_block_right_end
            while (
                right < self.width - 1 and not self.cells_occupancy[cell.y][right + 1]
            ):
                right += 1
            if right > original_block_right_end:  # もし移動した場合
                to_cells.append(Cell(y=cell.y, x=right - block.length + 1))

        elif block.orientation == "V":
            # 垂直方向に移動
            # 上に移動可能な最終位置を探す
            top = cell.y
            while top > 0 and not self.cells_occupancy[top - 1][cell.x]:
                top -= 1
            if top < cell.y:  # もし移動した場合
                to_cells.append(Cell(y=top, x=cell.x))

            # 下に移動可能な最終位置を探す
            original_block_bottom_end = cell.y + block.length - 1
            bottom = original_block_bottom_end
            while (
                bottom < self.height - 1
                and not self.cells_occupancy[bottom + 1][cell.x]
            ):
                bottom += 1
            if bottom > original_block_bottom_end:  # もし移動した場合
                to_cells.append(Cell(y=bottom - block.length + 1, x=cell.x))

        return to_cells
