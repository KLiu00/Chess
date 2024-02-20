from Enums.SideEnum import SideEnum as Side
from Enums.PieceEnum import PieceEnum as PieceType
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
        # board = [
        #     Rook(Side.BLACK), Knight(Side.BLACK), Bishop(Side.BLACK), Queen(Side.BLACK),
        #     King(Side.BLACK), Bishop(Side.BLACK), Knight(Side.BLACK), Rook(Side.BLACK),
        #     Pawn(Side.BLACK), Pawn(Side.BLACK), Pawn(Side.BLACK), Pawn(Side.BLACK),
        #     Pawn(Side.BLACK), Pawn(Side.BLACK), Pawn(Side.BLACK), Pawn(Side.BLACK),
        #     None, None, None, None, None, None, None, None,
        #     None, None, None, None, None, None, None, None,
        #     None, None, None, None, None, None, None, None,
        #     None, None, None, None, None, None, None, None,
        #     Pawn(Side.WHITE), Pawn(Side.WHITE), Pawn(Side.WHITE), Pawn(Side.WHITE),
        #     Pawn(Side.WHITE), Pawn(Side.WHITE), Pawn(Side.WHITE), Pawn(Side.WHITE),
        #     Rook(Side.WHITE), Knight(Side.WHITE), Bishop(Side.WHITE), Queen(Side.WHITE),
        #     King(Side.WHITE), Bishop(Side.WHITE), Knight(Side.WHITE), Rook(Side.WHITE)
        # ]

        board = [
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, Rook(Side.BLACK), None, Queen(Side.WHITE), None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
        ]
        return board

    # Returns a list of the requested pieces and the respective index on the board
    def getPieces(self, pieceType: PieceType, side: Side) -> list[tuple[IPiece, int]]:
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
        self.board[initialIndex].hasMoved = True

        # Switch playing sides
        self.switchSide()

        return True

    def unmakeMove(self) -> bool:
        # Check if move history is empty
        if self.__MoveHistory.isEmpty():
            return False

        # Gets the most recent move
        previousMove = self.__MoveHistory.top()

        self.board[previousMove.startPosition] = previousMove.pieceMoved
        self.board[previousMove.endPosition] = previousMove.capturedPiece

        # Removes the unmade move
        self.__MoveHistory.pop()

        return True

    """
    - boardIndex: The starting position on the board as an integer index.
    - direction: The direction of movement as an integer offset from the current index.
    - includeAllies: A boolean indicating whether the cells occupied by allied pieces should be included in the result.
    - includeContact: A boolean indicating whether the first encountered piece position should be included.
    - lifespan: The maximum number of cells the ray can travel.
    - xrayDepth: An integer representing how many pieces the ray can pass through.
    """
    def raycast(self, boardIndex: int, direction: int, includeAllies:bool = False, includeContact:bool = True, lifespan:int= 8, xrayDepth: int = 0) -> list[int]:
        currentIndex = boardIndex
        locations = []
        while lifespan > 0:
            currentIndexInRow = currentIndex % 8
            currentIndexInColumn = currentIndex // 8
            nextIndex = currentIndex + direction
            # Check if out of board
            if not 0 <= nextIndex <= 63:
                break

            nextIndexInRow = nextIndex % 8
            nextIndexInColumn = nextIndex // 8

            # Checks if it "jumps" rows or columns
            if abs(nextIndexInRow - currentIndexInRow) > 1 or abs(nextIndexInColumn - currentIndexInColumn) > 1:
                break

            # Checks if next cell contains a piece
            nextCell = self.board[nextIndex]
            if nextCell is not None:
                # Checks if the cell is same team
                if not includeAllies and nextCell.side == self.__SideToPlay:
                    break

                if includeContact:
                    locations.append(nextIndex)
                break

            locations.append(nextIndex)
            currentIndex = nextIndex
            lifespan -= 1
        return locations

    # Generates a list of indexes on the board the piece can go
    def generate_rook_moves(self, boardIndex: int):
        moves = []
        for direction in self.__HorizontalMovement:
            moves.extend(self.raycast(boardIndex, direction))

        for direction in self.__VerticalMovement:
            moves.extend(self.raycast(boardIndex, direction))

        return moves

    def generate_bishop_moves(self, boardIndex: int):
        moves = []
        for direction in self.__DiagonalMovement:
            moves.extend(self.raycast(boardIndex, direction))

        return moves

    def generate_queen_moves(self, boardIndex: int):
        moves = []
        moves.extend(self.generate_bishop_moves(boardIndex))
        moves.extend(self.generate_rook_moves(boardIndex))

        return moves

    def generate_king_moves(self, boardIndex: int):
        moves = []
        for direction in self.__DiagonalMovement + self.__HorizontalMovement + self.__VerticalMovement:
            moves.extend(self.raycast(boardIndex, direction, lifespan=1))

        return moves

    def generate_all_moves(self):
        moveGenerator = {PieceType.ROOK: self.generate_rook_moves,
             PieceType.BISHOP: self.generate_bishop_moves,
             PieceType.QUEEN: self.generate_queen_moves,
             PieceType.KING: self.generate_king_moves
             }
        moves = []        
        for boardIndex, cell in enumerate(self.board):
            # Check if current cell is empty
            if cell is None:
                continue

            if cell.side == self.__SideToPlay:
                moves.append((boardIndex, moveGenerator[cell.pieceType](boardIndex)))

        return moves

