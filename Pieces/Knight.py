from Pieces.BasePiece import IPiece
from Enums.SideEnum import SideEnum
from Enums.PieceEnum import PieceEnum


class Knight(IPiece):
    def __init__(self, side: SideEnum) -> None:
        super().__init__(side, PieceEnum.KNIGHT)

    def __str__(self) -> str:
        return f'{self.side.name[0].lower()}N'
