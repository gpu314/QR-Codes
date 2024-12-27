# Data masking rules
def masking(maskNumber: int, bit: int, row: int, column: int) -> int:
    if maskNumber == 0 and (row + column) % 2 == 0:
        return 1 - bit
    elif maskNumber == 1 and row % 2 == 0:
        return 1 - bit
    elif maskNumber == 2 and column % 3 == 0:
        return 1 - bit
    elif maskNumber == 3 and (row + column) % 3 == 0:
        return 1 - bit
    elif maskNumber == 4 and ((row // 2) + (column // 2)) % 2 == 0:
        return 1 - bit
    elif maskNumber == 5 and ((row * column) % 2) + ((row * column) % 3) == 0:
        return 1 - bit
    elif maskNumber == 6 and (((row * column) % 2) + ((row * column) % 3)) % 2 == 0:
        return 1 - bit
    elif maskNumber == 7 and (((row + column) % 2) + ((row * column) % 3)) % 2 == 0:
        return 1 - bit
    return bit

