from fastapi import FastAPI
from pydantic import BaseModel

from src.block import Board, Cell, Move, Position
from src.solver import Solver

app = FastAPI()


# This model should be the same as Board Class.
class BoardModel(BaseModel):
    width: int
    height: int
    goal: Cell
    positions: list[Position]


# This model should be the same as Move Class.
class MoveModel(BaseModel):
    from_cell: Cell
    to_cell: Cell
    block_id: int


@app.post("/solve")
async def solve(board_data: BoardModel):
    # BoardクラスのインスタンスにAPIから受け取ったデータをマッピング
    board = Board(
        width=board_data.width,
        height=board_data.height,
        goal=(board_data.goal.x, board_data.goal.y),
        positions=[
            (
                pos.block.id,
                pos.block.orientation,
                pos.block.length,
                (pos.cell.x, pos.cell.y),
            )
            for pos in board_data.positions
        ],
    )

    solver = Solver()
    solution: list[Move] = solver.run(board)

    # 最短手順をAPIのレスポンス形式に変換
    result = [
        MoveModel(
            from_cell=Cell(x=move.from_cell[0], y=move.from_cell[1]),
            to_cell=Cell(x=move.to_cell[0], y=move.to_cell[1]),
            block_id=move.block_id,
        )
        for move in solution
    ]

    return {"solution": result}
