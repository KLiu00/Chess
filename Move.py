from Pieces.BasePiece import IPiece
from ChessUtility import indexToRF

class Move:

    def __init__(self, startPosition: int, endPosition: int, pieceMoved: IPiece, capturedPiece: IPiece, capturedPiecePosition: int = 0) -> None:
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.pieceMoved = pieceMoved
        self.capturedPieceMoved = capturedPiece
        self.capturedPiecePosition = capturedPiecePosition if capturedPiecePosition != 0 else endPosition

        self.startRf = indexToRF(self.startPosition)
        self.endRf = indexToRF(self.endPosition)

class CastleMove(Move):
    def __init__(self, king_position: int, rook_position: int, king_piece: IPiece, rook_piece: IPiece, king_end_position, rook_end_position) -> None:
        super().__init__(king_position, king_end_position, king_piece, None)
        self.rook_piece = rook_piece
        self.rook_start_position = rook_position
        self.rook_end_position = rook_end_position

class PromotionMove(Move):
    def __init__(self, startPosition: int, endPosition: int, pawn_moved: IPiece, promoted_to: IPiece, piece_captured: IPiece = None) -> None:
        super().__init__(startPosition, endPosition, pawn_moved, piece_captured)
        self.initial_pawn = pawn_moved
        self.promoted_piece = promoted_to