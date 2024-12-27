from mask_evaluation import evaluate_mask
from data_masking import masking
from typing import List, Tuple
from matrix_preamble import *


# Add preamble patterns to matrix
def preamble(matrix: List[List[int]], version: int, size: int) -> List[List[int]]:
    matrix = finder_patterns(matrix, size)
    matrix = separators(matrix, size)
    matrix = alignment_patterns(matrix, version, size)
    matrix = format_information_area(matrix, size)
    matrix = version_information_area(matrix, version, size)
    matrix = dark_pixel(matrix, version)
    matrix = timing_patterns(matrix, size)
    return matrix


# Next data bit to place data at
def next_data_bit(matrix: List[List[int]], size: int, xydv: Tuple[int]) -> Tuple[int]:
    # Convert coordinates for easier math handling
    x = size-1-xydv[0]
    y = size-1-xydv[1]
    d = xydv[2]  # direction: 1 = up, -1 = down
    v = xydv[3]  # reached vertical bar: 0 = no, 1 = yes

    # Pair pixels pattern
    if (x + v) % 2 == 0:
        x += 1
    # Vertical pattern
    else:
        x -= 1
        if d == 1:
            y += 1
        else:
            y -= 1

    # Wrap around top/bottom
    if y < 0:
        y += 1
        x += 2
        d = 1
    elif y >= size:
        y -= 1
        x += 2
        d = -1

    # Skip over vertical timing pattern
    if x == size-FINDER_OUTER:
        x += 1
        v = 1

    # Convert coordinates back to actual values
    x = size-1-x
    y = size-1-y

    return (x, y, d, v)


# Creates and returns deep copy of matrix without modifying matrix
def deep_copy(matrix: List[List[int]]) -> List[List[int]]:
    matrixCopy = []
    for row in matrix:
        rowCopy = []
        for column in row:
            rowCopy.append(column)
        matrixCopy.append(rowCopy)
    return matrixCopy


# Place data bits
def data_bits(matrix: List[List[int]], size: int, dataBits: str, maskNumber: int) -> List[List[int]]:
    matrixCopy = deep_copy(matrix)
    idx = 0
    curr = (size-1, size-1, 1, 0)
    x = curr[0]
    y = curr[1]
    while curr[0] > -2:
        x = curr[0]
        y = curr[1]
        # Only place data bit if pixel at coordinates not already occupied from preamble
        if x >= 0 and y >= 0 and x < size and y < size and matrix[y][x] == -1:
            matrixCopy[y][x] = masking(maskNumber, int(dataBits[idx]), x, y)
            idx += 1
        curr = next_data_bit(matrix, size, curr)
    return matrixCopy


# Determining best mask and applying it
def best_mask(matrix: List[List[int]], size: int, dataBits: str) -> List[List[int]]:
    bestScore = 99999999
    bestMask = -1
    for maskNumber in range(0, 8):
        currentMatrix = data_bits(matrix, size, dataBits, maskNumber)
        currentScore = evaluate_mask(currentMatrix, size)
        if currentScore < bestScore:
            bestMask = maskNumber
    matrix = data_bits(matrix, size, dataBits, bestMask)
    return matrix


# Testing, display matrix, temporary function
def print_matrix(matrix: List[List[int]]):
    for row in matrix:
        for col in row:
            if col == -1:
                print("-", end="")
            else:
                print(col, end="")
        print()
    print()


# Testing
if __name__ == "__main__":
    version = 5
    size = size(version)
    mat = empty_matrix(size)
    mat = preamble(mat, version, size)
    print_matrix(mat)
    data = "01000011111101101011011001000110010101011111011011100110111101110100011001000010111101110111011010000110000001110111011101010110010101110111011000110010110000100010011010000110000001110000011001010101111100100111011010010111110000100000011110000110001100100111011100100110010101110001000000110010010101100010011011101100000001100001011001010010000100010001001011000110000001101110110000000110110001111000011000010001011001111001001010010111111011000010011000000110001100100001000100000111111011001101010101010111100101001110101111000111110011000111010010011111000010110110000010110001000001010010110100111100110101001010110101110011110010100100110000011000111101111011011010000101100100111111000101111100010010110011101111011111100111011111001000100001111001011100100011101110011010101111100010000110010011000010100010011010000110111100001111111111011101011000000111100110101011001001101011010001101111010101001001101111000100010000101000000010010101101010001101101100100000111010000110100011111100000010000001101111011110001100000010110010001001111000010110001101111011000000000"
    mat = best_mask(mat, size, data)
    print_matrix(mat)
