from Engine import ChessEngine as Chess
from Enums.PieceEnum import PieceEnum
from Enums.SideEnum import SideEnum

if __name__ == '__main__':
    instance = Chess()
    instance.displayBoard()
    print(instance.getPieces(PieceEnum.BISHOP, SideEnum.WHITE))

