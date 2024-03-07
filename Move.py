from Pieces.BasePiece import IPiece

class Move:

    def __init__(self, startPosition: int, endPosition: int, pieceMoved: IPiece, capturedPiece: IPiece, enPassant = False, capturedPiecePosition: int = 0) -> None:
        self.pieceMoved = pieceMoved
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.capturedPieceMoved = capturedPiece
        self.capturedPiecePosition = capturedPiecePosition if capturedPiecePosition != 0 else endPosition
