from src.block import Move


def display_moves(moves: list[Move] | None) -> None:
    if moves is None:
        print("No moves.")
        return
    for move in moves:
        print(f"{move.from_cell} -> {move.to_cell} (Block: {move.block})")
