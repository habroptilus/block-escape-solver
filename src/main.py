from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.block import Block, Board, Cell, Move, Position
from src.solver import Solver
from src.util import display_moves

app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ここで許可するオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],  # 許可するHTTPメソッドを指定
    allow_headers=["*"],  # 許可するHTTPヘッダーを指定
)


# This model should be the same as Board Class.
class BoardModel(BaseModel):
    width: int
    height: int
    goal: dict[str, int]
    positions: list[dict[str, Any]]


# This model should be the same as Move Class.
class MoveModel(BaseModel):
    from_cell: dict[str, int]
    to_cell: dict[str, int]
    block_id: int


@app.post("/solve")
async def solve(board_data: BoardModel):
    # BoardクラスのインスタンスにAPIから受け取ったデータをマッピング
    print(board_data)
    board = Board(
        width=board_data.width,
        height=board_data.height,
        goal=Cell(**board_data.goal),
        positions=[
            Position(block=Block(**pos["block"]), cell=Cell(**pos["cell"]))
            for pos in board_data.positions
        ],
    )

    board.display_board()
    print(board)
    solver = Solver()
    solution: list[Move] = solver.run(board)

    display_moves(solution)

    # 最短手順をAPIのレスポンス形式に変換
    result = [
        MoveModel(
            from_cell=move.from_cell.model_dump(),
            to_cell=move.to_cell.model_dump(),
            block_id=move.block.id,
        )
        for move in solution
    ]

    return {"solution": result}
