from Pieces.BasePiece import IPiece

class Move:

    def __init__(self, startPosition: int, endPosition: int, pieceMoved: IPiece, capturedPiece: IPiece, capturedPiecePosition: int = 0) -> None:
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.pieceMoved = pieceMoved
        self.capturedPieceMoved = capturedPiece
        self.capturedPiecePosition = capturedPiecePosition if capturedPiecePosition != 0 else endPosition

class CastleMove(Move):
    def __init__(self, king_position: int, rook_position: int, king_piece: IPiece, rook_piece: IPiece, king_end_position, rook_end_position) -> None:
        super().__init__(king_position, king_end_position, king_piece, None)
        self.rook_piece = rook_piece
        self.rook_start_position = rook_position
        self.rook_end_position = rook_end_position
