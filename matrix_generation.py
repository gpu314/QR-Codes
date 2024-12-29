from matrix_preamble_finishing import version_information
from matrix_preamble_finishing import version_string
from matrix_preamble_finishing import format_information
from matrix_preamble_finishing import format_string
from mask_evaluation import evaluate_mask
from data_masking import masking
from typing import List, Tuple
from matrix_preamble_finishing import *


# Determines size (side length) of QR code from version
def matrix_size(version: int) -> int:
    return (4*(version-1)+21)


# Generates empty matrix of given size
def empty_matrix(size: int) -> List[List[int]]:
    m = [[-1 for j in range(size)] for i in range(size)]
    return m


# Add preamble patterns to matrix
def preamble(matrix: List[List[int]], version: int, size: int) -> List[List[int]]:
    matrix = finder_patterns(matrix, size)
    matrix = separators(matrix, size)
    matrix = alignment_patterns(matrix, version, size)
    matrix = timing_patterns(matrix, size)
    matrix = format_information_area(matrix, size)
    matrix = version_information_area(matrix, version, size)
    matrix = dark_pixel(matrix, version)
    return matrix


# Add finishing patterns to matrix
def finishing(matrix: List[List[int]], errorCorrectionLevel: str, mask: int, version: int, size: int) -> List[List[int]]:
    formatString = format_string(errorCorrectionLevel, mask)
    matrix = format_information(matrix, size, formatString)
    versionString = version_string(version)
    matrix = version_information(matrix, version, size, versionString)
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
    return [matrix, bestMask]


# Main function. Returns final matrix using other functions
def matrix_generation(data: str, version: int, errorCorrectionLevel: str) -> List[List[int]]:
    size = matrix_size(version)
    matrix = empty_matrix(size)
    matrix = preamble(matrix, version, size)
    matrix, mask = best_mask(matrix, size, data)
    matrix = finishing(matrix, errorCorrectionLevel, mask, version, size)
    return matrix


# # Testing, display matrix, temporary function
# def print_matrix(matrix: List[List[int]]):
#     for row in matrix:
#         for col in row:
#             if col == -1:
#                 print("-", end="")
#             else:
#                 print(col, end="")
#         print()
#     print()
