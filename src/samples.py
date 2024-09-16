from block import Block, Cell, Position

PRO_12 = [
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
BASIC_01 = [
    Position(
        cell=Cell(y=2, x=0),
        block=Block(id=1, length=2, orientation="H", is_target=True),
    ),
    Position(cell=Cell(y=3, x=1), block=Block(id=1, length=2, orientation="V")),
    Position(cell=Cell(y=4, x=2), block=Block(id=2, length=2, orientation="H")),
    Position(cell=Cell(y=0, x=4), block=Block(id=3, length=2, orientation="H")),
    Position(cell=Cell(y=1, x=4), block=Block(id=4, length=2, orientation="V")),
    Position(cell=Cell(y=3, x=4), block=Block(id=5, length=2, orientation="V")),
]

sample_map = {"pro_12": PRO_12, "basic_01": BASIC_01}
