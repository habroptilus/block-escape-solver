from typing import Literal

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
    from_cell: Cell
    to_cell: Cell
    block: Block


class Board(BaseModel):
    width: int
    height: int
    goal: Cell
    positions: list[Position]
    cells_occupancy: list[list[bool]] | None = None

    def init_occupancy(self) -> None:
        cells_occupancy = [
            [False for _ in range(self.width)] for _ in range(self.height)
        ]

        for position in self.positions:
            cell = position.cell
            block = position.block
            for i in range(block.length):
                if block.orientation == "H":
                    cells_occupancy[cell.y][cell.x + i] = True
                elif block.orientation == "V":
                    cells_occupancy[cell.y + i][cell.x] = True

        self.cells_occupancy = cells_occupancy

    def display_board(self) -> None:
        if self.cells_occupancy is None:
            print("Board is not initialized. Please call init_occupancy() first.")
            return

        for row in self.cells_occupancy:
            print(" ".join("X" if cell else "." for cell in row))

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
            right = cell.x + block.length - 1
            while (
                right < self.width - 1 and not self.cells_occupancy[cell.y][right + 1]
            ):
                right += 1
            if right > cell.x + block.length - 1:  # もし移動した場合
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
            bottom = cell.y + block.length - 1
            while (
                bottom < self.height - 1
                and not self.cells_occupancy[bottom + 1][cell.x]
            ):
                bottom += 1
            if bottom > cell.y + block.length - 1:  # もし移動した場合
                to_cells.append(Cell(y=bottom - block.length + 1, x=cell.x))

        return to_cells


N = 6
goal = Cell(x=5, y=2)
init_positions: list[Position] = [
    Position(cell=Cell(y=0, x=0), block=Block(id=1, length=3, orientation="H")),
    Position(
        cell=Cell(y=2, x=0),
        block=Block(id=2, length=2, orientation="H", is_target=True),
    ),
    Position(cell=Cell(y=3, x=0), block=Block(id=3, length=2, orientation="V")),
    Position(cell=Cell(y=5, x=0), block=Block(id=4, length=2, orientation="H")),
    Position(cell=Cell(y=1, x=1), block=Block(id=5, length=2, orientation="H")),
    Position(cell=Cell(y=2, x=2), block=Block(id=6, length=2, orientation="V")),
    Position(cell=Cell(y=4, x=2), block=Block(id=7, length=2, orientation="H")),
    Position(cell=Cell(y=0, x=3), block=Block(id=8, length=2, orientation="V")),
    Position(cell=Cell(y=4, x=3), block=Block(id=9, length=2, orientation="H")),
    Position(cell=Cell(y=0, x=4), block=Block(id=10, length=2, orientation="V")),
    Position(cell=Cell(y=3, x=4), block=Block(id=11, length=2, orientation="H")),
    Position(cell=Cell(y=4, x=4), block=Block(id=12, length=2, orientation="H")),
    Position(cell=Cell(y=0, x=5), block=Block(id=13, length=3, orientation="V")),
]

board = Board(width=N, height=N, goal=goal, positions=init_positions)

board.init_occupancy()
board.display_board()
print(board.calculate_available_moves())
