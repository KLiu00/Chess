from IPiece import IPiece
from Enums.SideEnum import SideEnum
from Enums.PieceEnum import PieceEnum


class Bishop(IPiece):
    def __init__(self, side: SideEnum):
        super().__init__(side, PieceEnum.BISHOP)
