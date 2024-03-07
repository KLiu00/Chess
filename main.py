from Engine import ChessEngine as Chess
from ChessUtility import indexToRF, rfToIndex
from Enums.PieceEnum import PieceEnum
from Enums.SideEnum import SideEnum

if __name__ == '__main__':
    instance = Chess()

    while not instance.checkmated:
        print(instance.displayBoard())
        all_moves = instance.generate_all_moves()
        rf_moves = []
        total = 0
        for move in all_moves:
            total += 1 
            rf_moves.append(f"{indexToRF(move.startPosition)}{indexToRF(move.endPosition)}")
            print(f"{indexToRF(move.startPosition)}{indexToRF(move.endPosition)}", end=" ")
        print("\nTotal amount of moves:" , total)

        toMake = input("Enter your move: ")

        if toMake == "-1":
            instance.unmakeMove()
            continue

        # Check if move in allowed moves list
        if toMake not in rf_moves:
            # if not in the list, ask for move again by skipping make move logic
            continue

        instance.makeMove(all_moves[rf_moves.index(toMake)])
