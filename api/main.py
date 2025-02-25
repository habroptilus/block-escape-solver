import os
from pathlib import Path
from typing import Any, Literal

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.block import Block, Board, Cell, Move, Position, PositionList
from src.drawer import GifDrawer
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
DirectionType = Literal["up", "down", "right", "left"]


def _get_direction(from_cell: Cell, to_cell: Cell) -> DirectionType:
    if from_cell.x == to_cell.x and from_cell.y == to_cell.y:
        raise ValueError("Cells are the same. No direction.")

    if from_cell.x == to_cell.x:
        return "up" if from_cell.y > to_cell.y else "down"
    elif from_cell.y == to_cell.y:
        return "left" if from_cell.x > to_cell.x else "right"
    else:
        raise ValueError("Cells are not aligned horizontally or vertically.")


def _remove_file(path: str):
    try:
        os.remove(path)
        print(f"Deleted file: {path}")
    except Exception as e:
        print(f"Error deleting file {path}: {e}")


# This model should be the same as Board Class.
class BoardModel(BaseModel):
    width: int
    height: int
    goal: dict[str, int]
    positions: list[dict[str, Any]]


# This model should be the same as Move Class.
class MoveModel(BaseModel):
    from_cell: dict[str, int]
    direction: DirectionType
    block_id: int


@app.post("/solve")
async def solve(board_data: BoardModel):
    # BoardクラスのインスタンスにAPIから受け取ったデータをマッピング
    board = Board(
        width=board_data.width,
        height=board_data.height,
        goal=Cell(**board_data.goal),
        positions=PositionList(
            positions=[
                Position(block=Block(**pos["block"]), cell=Cell(**pos["cell"]))
                for pos in board_data.positions
            ]
        ),
    )

    board.display_board()
    solver = Solver()
    solution: list[Move] = solver.run(board)

    display_moves(solution)

    # 最短手順をAPIのレスポンス形式に変換
    result = [
        MoveModel(
            from_cell=move.from_cell.model_dump(),
            direction=_get_direction(from_cell=move.from_cell, to_cell=move.to_cell),
            block_id=move.block.id,
        )
        for move in solution
    ]

    return {"solution": result}


app = FastAPI()


@app.post("/generate-gif")
async def generate_gif(board_data: BoardModel, background_tasks: BackgroundTasks):
    # BoardクラスのインスタンスにAPIから受け取ったデータをマッピング
    board = Board(
        width=board_data.width,
        height=board_data.height,
        goal=Cell(**board_data.goal),
        positions=PositionList(
            positions=[
                Position(block=Block(**pos["block"]), cell=Cell(**pos["cell"]))
                for pos in board_data.positions
            ]
        ),
    )
    print(board.positions)

    board.display_board()
    solver = Solver()
    solution: list[Move] = solver.run(board)

    display_moves(solution)

    output_filepath = "output.gif"
    drawer = GifDrawer(
        grid_size=board_data.width, image_dir=Path("tmp_images"), keep_images=False
    )
    drawer.run(board=board, solutions=solution, output_filepath="output.gif")

    # ファイルが存在するかチェック
    if not os.path.exists(output_filepath):
        raise HTTPException(status_code=404, detail="GIFファイルが見つかりません")

    background_tasks.add_task(_remove_file, output_filepath)

    # GIFファイルを返す
    return FileResponse(
        output_filepath,
        media_type="image/gif",
        filename="result.gif",
        background=background_tasks,
    )
