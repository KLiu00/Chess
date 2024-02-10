from Pieces.BasePiece import IPiece
from Enums.SideEnum import SideEnum
from Enums.PieceEnum import PieceEnum


class Queen(IPiece):
    def __init__(self, side: SideEnum) -> None:
        super().__init__(side, PieceEnum.QUEEN)
