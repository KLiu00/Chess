def indexToRF(index: int) -> str:
    files = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return f"{files[index%8]}{8-index//8}"
