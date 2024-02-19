from Engine import ChessEngine as Chess
from Enums.PieceEnum import PieceEnum
from Enums.SideEnum import SideEnum

def indexToRF(index: int ) -> str:
    files = ["a","b","c","d","e","f","g","h"]
    return f"{files[index%8]}{8-index//8}"

if __name__ == '__main__':
    instance = Chess()
    while not instance.checkmated:
        print(instance.displayBoard())
        all_moves = instance.generate_all_moves()
        for boardIndex, move_set in all_moves:
            for move in move_set:
                print(f"{indexToRF(boardIndex)}{indexToRF(move)}", end=" ")
                
        fromMake = int(input("From: "))
        toMake = int(input("to: "))

        if fromMake == -1 or toMake == -1:
            instance.unmakeMove()
            continue

        instance.makeMove(fromMake, toMake)
