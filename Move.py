from Pieces.BasePiece import IPiece

class Move:

    def __init__(self, startPosition: int, endPosition: int, pieceMoved: IPiece, capturedPiece: IPiece) -> None:
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.pieceMoved = pieceMoved
        self.capturedPiece = capturedPiece
