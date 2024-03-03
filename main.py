from Engine import ChessEngine as Chess
from ChessUtility import indexToRF
from Enums.PieceEnum import PieceEnum
from Enums.SideEnum import SideEnum

if __name__ == '__main__':
    instance = Chess()

    while not instance.checkmated:
        print(instance.displayBoard())
        all_moves = instance.generate_all_moves()
        total = 0
        for boardIndex, move_set in all_moves:
            for move in move_set:
                total += 1 
                print(f"{indexToRF(boardIndex)}{indexToRF(move)}", end=" ")
        print("\nTotal amount of moves:" , total)
                
        fromMake = int(input("From: "))
        toMake = int(input("to: "))

        if fromMake == -1 or toMake == -1:
            instance.unmakeMove()
            continue

        instance.makeMove(fromMake, toMake)
