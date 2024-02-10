from Enums.SideEnum import SideEnum
from Enums.PieceEnum import PieceEnum


class IPiece:

    def __init__(self, side: SideEnum, piece: PieceEnum) -> None:
        self.side = side
        self.pieceType: PieceEnum = piece
        self.hasMoved: bool = False

    def __str__(self) -> str:
        return f'{self.side.name}{self.pieceType.name}'
