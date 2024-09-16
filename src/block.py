from collections import deque
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
                    cells_occupancy[cell.y][cell.x + i] = True
                elif block.orientation == "V":
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
            if position.block.is_target:
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


def apply_move(positions: list[Position], move: Move) -> list[Position]:
    results = []
    for position in positions:
        if position.block != move.block:
            results.append(position)
        else:
            results.append(Position(block=position.block, cell=move.to_cell))
    return results


def get_new_board(board: Board, move: Move) -> Board:
    positions = board.positions
    new_positions = apply_move(positions=positions, move=move)
    return Board(
        width=board.width, height=board.height, goal=board.goal, positions=new_positions
    )


def find_shortest_path_to_clear(board: Board) -> list[Move] | None:
    # BFS のためのキュー
    queue = deque([(board, [])])
    # 訪問済みの状態を管理するセット
    visited = set()
    # 現在のボードの状態を保存
    visited.add(
        tuple(
            sorted([(pos.block.id, pos.cell.y, pos.cell.x) for pos in board.positions])
        )
    )

    while queue:
        current_board, moves = queue.popleft()
        current_board.display_board()

        # ゲームがクリアされているか確認
        if current_board.is_cleared():
            return moves

        # 現在のボードから移動可能なすべての移動を計算
        available_moves = current_board.calculate_available_moves()

        for move in available_moves:
            new_board = get_new_board(current_board, move)
            new_positions = new_board.positions
            # ボードの状態を保存
            state_tuple = tuple(
                sorted(
                    [(pos.block.id, pos.cell.y, pos.cell.x) for pos in new_positions]
                )
            )

            if state_tuple not in visited:
                visited.add(state_tuple)
                queue.append((new_board, moves + [move]))

    return None
