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


class Board(BaseModel):
    width: int
    height: int
    goal: Cell
    positions: list[Position]
    cells_occupancy: list[list[bool]] | None = None

    def init_occupancy(self):
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

    def display_board(self):
        if self.cells_occupancy is None:
            print("Board is not initialized. Please call init_occupancy() first.")
            return

        for row in self.cells_occupancy:
            print(" ".join("X" if cell else "." for cell in row))


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
    Position(cell=Cell(y=2, x=3), block=Block(id=8, length=2, orientation="V")),
    Position(cell=Cell(y=4, x=3), block=Block(id=9, length=2, orientation="H")),
    Position(cell=Cell(y=0, x=4), block=Block(id=10, length=2, orientation="V")),
    Position(cell=Cell(y=3, x=4), block=Block(id=11, length=2, orientation="H")),
    Position(cell=Cell(y=4, x=4), block=Block(id=12, length=2, orientation="H")),
    Position(cell=Cell(y=0, x=5), block=Block(id=13, length=3, orientation="V")),
]

board = Board(width=N, height=N, goal=goal, positions=init_positions)

board.init_occupancy()
board.display_board()
