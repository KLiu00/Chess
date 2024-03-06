files = ["a", "b", "c", "d", "e", "f", "g", "h"]
def indexToRF(index: int) -> str:
    return f"{files[index%8]}{8-index//8}"

def rfToIndex(rf: str) -> int:
    rank = rf[1]
    file = rf[0]
    return files.index(file) + 64 - 8 * int(rank)
