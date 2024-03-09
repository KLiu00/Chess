from Enums.SideEnum import SideEnum as Side
from Enums.PieceEnum import PieceEnum as PieceType
from Move import Move, CastleMove
from Stack import Stack

from copy import copy

from Pieces.BasePiece import IPiece
from Pieces.Queen import Queen
from Pieces.Bishop import Bishop
from Pieces.King import King
from Pieces.Knight import Knight
from Pieces.Rook import Rook
from Pieces.Pawn import Pawn


class ChessEngine:

    def __init__(self) -> None:
        self.SideToPlay: Side = Side.WHITE
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

        # board = [
        #     King(Side.BLACK), None, None, None, None, None, None, None,
        #     None, None, None, None, None, None, None, None,
        #     None, None, None, None, None, None, None, None,
        #     None, None, None, None, None, None, None, None,
        #     None, None, None, None, None, Pawn(Side.BLACK), None, None,
        #     None, None, None, None, None, None, None, None,
        #     None, None, None, None, Pawn(Side.WHITE), None, None, None,
        #     Rook(Side.WHITE), None, None, None, King(Side.WHITE), None, None, Rook(Side.WHITE),
        # ]

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
        self.SideToPlay = Side.WHITE if self.SideToPlay == Side.BLACK else Side.BLACK

    # Makes a move on the board and returns whether the operation failed or succeeded.
    def makeMove(self, move: Move) -> bool:
        initialCell = self.board[move.startPosition]
        finalCell = self.board[move.endPosition]
        takingPiece = False if finalCell is None else True

        # Selected nothing to move
        if initialCell is None:
            return False
        # Attempting to take self piece
        if takingPiece and initialCell.side == finalCell.side:
            return False

        self.board[move.startPosition] = None
        self.board[move.capturedPiecePosition] = None
        self.board[move.endPosition] = initialCell

        if isinstance(move, CastleMove):
            self.board[move.rook_start_position] = None
            self.board[move.rook_end_position] = move.rook_piece
            move.rook_piece.hasMoved = True

        # Add move onto the move history.
        self.__MoveHistory.push(move)
        self.board[move.endPosition].hasMoved = True

        # Switch playing sides
        self.switchSide()

        return True

    def unmakeMove(self) -> bool:
        # Check if move history is empty
        if self.__MoveHistory.isEmpty():
            return False

        # Gets the most recent move
        previousMove: Move = self.__MoveHistory.top()

        self.board[previousMove.startPosition] = previousMove.pieceMoved
        self.board[previousMove.endPosition] = None
        self.board[previousMove.capturedPiecePosition] = previousMove.capturedPieceMoved

        if isinstance(previousMove, CastleMove):
            self.board[previousMove.rook_end_position] = None
            self.board[previousMove.rook_start_position] = previousMove.rook_piece
            previousMove.rook_piece.hasMoved = False

        # Removes the unmade move
        self.__MoveHistory.pop()

        # Switches the side
        self.switchSide()

        return True

    """
    - boardIndex: The starting position on the board as an integer index.
    - direction: The direction of movement as an integer offset from the current index.
    - includeAllies: A boolean indicating whether the cells occupied by allied pieces should be included in the result.
    - includeContact: A boolean indicating whether the first encountered piece position should be included.
    - lifespan: The maximum number of cells the ray can travel.
    - xrayDepth: Passes through first piece until contact with another
    """
    def raycast(self, boardIndex: int, direction: int, includeAllies:bool = False, includeContact:bool = True, lifespan:int= 8, xray: bool = False) -> list[Move]:
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
                if not includeAllies and nextCell.side == self.board[boardIndex].side:
                    break

                if includeContact:
                    move = Move(boardIndex, nextIndex, copy(self.board[boardIndex]), copy(nextCell))
                    locations.append(move)
                break

            move = Move(boardIndex, nextIndex, copy(self.board[boardIndex]), copy(nextCell))
            locations.append(move)
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

    def generate_knight_moves(self, boardIndex: int):
        moves = []
        directions = [17, 15, 10, 6, -17, -15, -10, -6]
        currentIndexInRow = boardIndex % 8
        currentIndexInColumn = boardIndex // 8
        for direction in directions:
            nextIndex = boardIndex + direction
            # Check if out of board
            if not 0 <= nextIndex <= 63:
                continue

            nextIndexInRow = nextIndex % 8
            nextIndexInColumn = nextIndex // 8
            # Checks if it "jumps" rows or columns
            if abs(nextIndexInRow - currentIndexInRow) > 2 or abs(nextIndexInColumn - currentIndexInColumn) > 2:
                continue

            # Checks if next cell contains a piece
            nextCell = self.board[nextIndex]
            if nextCell is not None:
                # Checks if the cell is same team
                if nextCell.side == self.board[boardIndex].side:
                    continue

            move = Move(boardIndex, nextIndex, copy(self.board[boardIndex]), copy(nextCell))
            moves.append(move)
        return moves

    def generate_pawn_moves(self, boardIndex: int):
        # Gets information of piece from the board
        hasMoved = self.board[boardIndex].hasMoved
        side = self.board[boardIndex].side

        moves = []
        sideMultiplier = 1 if side == Side.BLACK else -1
        movementDirection = 8

        # If the piece has not moved
        rayLifespan = 1 if hasMoved else 2
        # Generates linear pawn movement
        moves.extend(self.raycast(boardIndex, sideMultiplier*movementDirection, includeContact=False, lifespan=rayLifespan))

        # Taking pieces
        takingDirections = [7, 9]
        for direction in takingDirections:
            # Adjust for which side the pawn is on
            direction *= sideMultiplier
            move: list[Move] = self.raycast(boardIndex, direction, includeContact=True, lifespan=1)
            # Check if potential move is possible
            if len(move) == 0:
                continue
            # Gets the move, raycast returns a list but there will only be one in this case.
            move: Move = move[0]
            # Checks if the move location is an enemy piece, if yes add to move list.
            if move.capturedPieceMoved is not None:
                moves.append(move)

        # En passant logic
        """
        1. Moving piece has to move behind the pawn with passed it, taking it too.
        2. En passant must be available only immediately after the pawn makes the two-square move,
        if the player does not capture en passant on the next move, the opportunity is lost.
        """
        mostRecentMove: Move = self.__MoveHistory.top()
        # Checks if previous move exists
        if mostRecentMove:
            # Checks if the piece type is pawn
            if mostRecentMove.pieceMoved.pieceType is PieceType.PAWN:
                # Check if they are in the same row
                if mostRecentMove.endPosition // 8 == boardIndex // 8:
                    # Check if is next to eachother and is dual move
                    if abs((mostRecentMove.endPosition % 8) - (boardIndex % 8)) == 1 and abs(mostRecentMove.startPosition - mostRecentMove.endPosition) // 8 == 2:
                        a = Move(boardIndex,mostRecentMove.endPosition + 8 * sideMultiplier, copy(self.board[boardIndex]), mostRecentMove.pieceMoved, True, mostRecentMove.endPosition)
                        moves.append(a)

        return moves

    def is_attacked(self, board_indexes: list[int]) -> bool:
        states: list[bool] = []
        moves = self.generate_all_moves(Side.BLACK if self.SideToPlay is Side.WHITE else Side.BLACK)
        move_indexes = [move.capturedPiecePosition for move in moves]
        for index in board_indexes:
            states.append(index in move_indexes)   
        return states

    def in_check(self, king_position: int = None) -> bool:
        if king_position is None:
            king = self.getPieces(PieceType.KING, self.SideToPlay)[0][0]
        else:
            king = king_position
        return self.is_attacked([king])[0]

    def castling_moves(self) -> list[Move]:
        king: list[tuple[IPiece, int]] = self.getPieces(PieceType.KING, self.SideToPlay)[0]

        king_piece, king_position = king

        moves: list[Move] = []
        short_castle_allowed = long_castle_allowed = False
        short_rook = long_rook = None

        # if the king has moved or in check, skip.
        if king_piece.hasMoved or self.in_check(king_position):
            return moves

        # Check if no piece in between them, Short castle
        if squares := self.raycast(king_position, 1, True):
            if squares[-1].capturedPieceMoved is not None and squares[-1].capturedPieceMoved.pieceType is PieceType.ROOK:
                short_castle_allowed = True
                short_rook = squares[-1]
        # Long Castle
        if squares := self.raycast(king_position, -1, True):
            if squares[-1].capturedPieceMoved is not None and squares[-1].capturedPieceMoved.pieceType is PieceType.ROOK:
                long_castle_allowed = True
                long_rook = squares[-1]

        if short_castle_allowed:
            sq1, sq2 = self.is_attacked([king_position+1, king_position+2])
            if not (sq1 or sq2):
                a = CastleMove(
                    king_position,
                    short_rook.capturedPiecePosition,
                    copy(king_piece),
                    copy(short_rook.capturedPieceMoved),
                    king_position + 2,
                    king_position + 1,
                )
                moves.append(a)
        # long castle
        if long_castle_allowed:
            sq1, sq2 = self.is_attacked([king_position-1, king_position-2])
            if not (sq1 or sq2) and not long_rook.capturedPieceMoved.hasMoved:
                a = CastleMove(
                    king_position,
                    long_rook.capturedPiecePosition,
                    copy(king_piece),
                    copy(long_rook.capturedPieceMoved),
                    king_position - 2,
                    king_position - 1,
                )
                moves.append(a)
        return moves

    def generate_all_moves(self, side: Side) -> list[Move]:
        moveGenerator = {
             PieceType.ROOK: self.generate_rook_moves,
             PieceType.BISHOP: self.generate_bishop_moves,
             PieceType.QUEEN: self.generate_queen_moves,
             PieceType.KING: self.generate_king_moves,
             PieceType.KNIGHT: self.generate_knight_moves,
             PieceType.PAWN: self.generate_pawn_moves
        }
        moves = []        
        for boardIndex, cell in enumerate(self.board):
            # Check if current cell is empty
            if cell is None:
                continue

            if cell.side == side :
                moves.extend(moveGenerator[cell.pieceType](boardIndex))

        return moves

    def generate_legal_moves(self) -> list[Move]:
        moves: list[Move] = self.generate_all_moves(self.SideToPlay)
        moves.extend(self.castling_moves())

        return moves
