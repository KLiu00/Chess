from Enums.SideEnum import SideEnum as Side
from Enums.PieceEnum import PieceEnum
from Move import Move
from Stack import Stack

from Pieces.BasePiece import IPiece
from Pieces.Queen import Queen
from Pieces.Bishop import Bishop
from Pieces.King import King
from Pieces.Knight import Knight
from Pieces.Rook import Rook
from Pieces.Pawn import Pawn


class ChessEngine:

    def __init__(self) -> None:
        self.__SideToPlay: Side = Side.WHITE
        self.__MoveHistory = Stack()
        self.turnCount = 0
        self.board = []
        self.checkmated = False
        self.board = self.__InitBoard()

        # Board movement directions in one dimensional array.
        self.__HorizontalMovement = [-1, 1]
        self.__VerticalMovement = [-8, 8]
        self.__DiagonalMovement = [-7, -9, 7, 9]
    # Returns a fresh board
    def __InitBoard(self) -> list[IPiece]:
        board = [
            Rook(Side.BLACK), Knight(Side.BLACK), Bishop(Side.BLACK), Queen(Side.BLACK),
            King(Side.BLACK), Bishop(Side.BLACK), Knight(Side.BLACK), Rook(Side.BLACK),
            Pawn(Side.BLACK), Pawn(Side.BLACK), Pawn(Side.BLACK), Pawn(Side.BLACK),
            Pawn(Side.BLACK), Pawn(Side.BLACK), Pawn(Side.BLACK), Pawn(Side.BLACK),
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            Pawn(Side.WHITE), Pawn(Side.WHITE), Pawn(Side.WHITE), Pawn(Side.WHITE),
            Pawn(Side.WHITE), Pawn(Side.WHITE), Pawn(Side.WHITE), Pawn(Side.WHITE),
            Rook(Side.WHITE), Knight(Side.WHITE), Bishop(Side.WHITE), Queen(Side.WHITE),
            King(Side.WHITE), Bishop(Side.WHITE), Knight(Side.WHITE), Rook(Side.WHITE)
        ]
        return board
    
    # Returns a list of the requested pieces and the respective index on the board 
    def getPieces(self, pieceType: PieceEnum, side: Side) -> list[tuple[IPiece, int]]:
        pieces: list[tuple[IPiece, int]] = []
        for i,cell in enumerate(self.board):
            if cell is None: 
                continue
            if (cell.pieceType == pieceType) and (cell.side == side):
                pieces.append((cell, i))
        return pieces
    
    def displayBoard(self) -> str:
        display = ""
        for i, cell in enumerate(self.board):
            if i % 8 == 0:
                display += "\n"
            display += f"{ '--' if cell is None else str(cell)} "

        return display
    
    def switchSide(self) -> None:
        self.__SideToPlay = Side.WHITE if self.__SideToPlay == Side.BLACK else Side.BLACK

    # Makes a move on the board and returns whether the operation failed or succeeded.
    def makeMove(self, initialIndex: int, finalIndex: int) -> bool:
        initialCell = self.board[initialIndex]
        finalCell = self.board[finalIndex]
        takingPiece = False if finalCell is None else True

        # Selected nothing to move
        if initialCell is None:
            return False
        # Attempting to take self piece
        if takingPiece and initialCell.side == finalCell.side:
            return False

        self.board[initialIndex] = None
        self.board[finalIndex] = initialCell

        # Add move onto the move history.
        self.__MoveHistory.push(Move(initialIndex, finalIndex, initialCell, finalCell))

        # Switch playing sides
        self.switchSide()

        return True
    
    def unmakeMove(self) -> bool:
        # Check if move history is empty
        if len(self.__MoveHistory) == 0:
            return False
        
        previousMove = self.__MoveHistory
        
