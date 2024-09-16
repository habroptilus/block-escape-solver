from collections import deque

from block import Board, Cell, Move, Position
from samples import sample_map


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

        is_leaf_node = True
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
                is_leaf_node = False
                visited.add(state_tuple)
                queue.append((new_board, moves + [move]))

        if is_leaf_node:
            current_board, moves = queue.popleft()
            current_board.display_board()
            # display_moves(moves)
    return None


def display_moves(moves: list[Move]) -> None:
    for move in moves:
        print(f"{move.from_cell} -> {move.to_cell} (Block: {move.block})")


def main():
    N = 6
    goal = Cell(x=5, y=2)

    init_positions = sample_map["pro_12"]

    board = Board(width=N, height=N, goal=goal, positions=init_positions)

    best_moves = find_shortest_path_to_clear(board=board)

    if best_moves is None:
        print("No solution found.")
    else:
        print(f"Shortest moves: {len(best_moves)}")
        display_moves(best_moves)


if __name__ == "__main__":
    main()
