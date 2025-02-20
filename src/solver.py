from collections import deque

from src.block import Board, Move


class Solver:
    def run(self, board: Board) -> list[Move] | None:
        # BFS のためのキュー
        queue = deque([(board, [])])
        # 訪問済みの状態を管理するセット
        visited = set()
        # 現在のボードの状態を保存
        visited.add(
            tuple(
                sorted(
                    [(pos.block.id, pos.cell.y, pos.cell.x) for pos in board.positions]
                )
            )
        )

        while queue:
            current_board, moves = queue.popleft()

            # ゲームがクリアされているか確認
            if current_board.is_cleared():
                return moves

            # 現在のボードから移動可能なすべての移動を計算
            available_moves = current_board.calculate_available_moves()

            for move in available_moves:
                new_board = current_board.apply_move(move)
                new_positions = new_board.positions
                # ボードの状態を保存
                state_tuple = tuple(
                    sorted(
                        [
                            (pos.block.id, pos.cell.y, pos.cell.x)
                            for pos in new_positions
                        ]
                    )
                )

                if state_tuple not in visited:
                    visited.add(state_tuple)
                    queue.append((new_board, moves + [move]))

        return None
