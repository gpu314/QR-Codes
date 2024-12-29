from typing import List

# Evaluates the penalty of a matrix
def evaluate_mask(matrix: List[List[int]], size: int) -> int:
    penalty = 0

    # Penalty rule 1
    penalty1 = 0

    # Assess rows
    for y in range(size):
        currentLength = 0
        currentColor = -1
        for x in range(size):
            if matrix[y][x] == currentColor:
                currentLength += 1
            else:
                currentLength = 1
                currentColor = matrix[y][x]
            if currentLength == 5:
                penalty1 += 3
            elif currentLength > 5:
                penalty1 += 1

    # Assess columns
    for x in range(size):
        currentLength = 0
        currentColor = -1
        for y in range(size):
            if matrix[y][x] == currentColor:
                currentLength += 1
            else:
                currentLength = 1
                currentColor = matrix[y][x]
            if currentLength == 5:
                penalty1 += 3
            elif currentLength > 5:
                penalty1 += 1

    # Penalty rule 2
    penalty2 = 0
    for y in range(size):
        for x in range(size):
            if x+1 >= size or y+1 >= size:
                continue
            if matrix[y][x] == matrix[y][x+1] == matrix[y+1][x] == matrix[y+1][x+1]:
                penalty2 += 3

    # Penalty rule 3
    penalty3 = 0

    # Assess rows
    for y in range(size):
        for x in range(size):
            if x + 10 >= size:
                continue
            current = "".join([str(matrix[y][x+k]) for k in range(0, 11)])
            if current == "10111010000" or current == "00001011101":
                penalty3 += 40

    # Assess columns
    for x in range(size):
        for y in range(size):
            if y + 10 >= size:
                continue
            current = "".join([str(matrix[y+k][x]) for k in range(0, 11)])
            if current == "10111010000" or current == "00001011101":
                penalty3 += 40

    # Penalty rule 4
    penalty4 = 0
    totalPixels = size*size
    darkPixels = sum(matrix[y][x] == 1 for y in range(size)
                     for x in range(size))
    darkPercentage = 100 * (darkPixels / totalPixels)

    previousMultiple5 = int((darkPercentage // 5) * 5)
    nextMultiple5 = previousMultiple5 + 5

    num1 = abs(previousMultiple5 - 50) // 5
    num2 = abs(nextMultiple5 - 50) // 5

    penalty4 = 10 * min(num1, num2)

    # Overall penalty score
    penalty = penalty1 + penalty2 + penalty3 + penalty4
    return penalty
