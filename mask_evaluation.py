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
    darkPixels = sum(matrix[y][x] == 1 for y in range(size) for x in range(size))
    darkPercentage = 100 * (darkPixels / totalPixels)

    previousMultiple5 = int((darkPercentage // 5) * 5)
    nextMultiple5 = previousMultiple5 + 5

    num1 = abs(previousMultiple5 - 50) // 5
    num2 = abs(nextMultiple5 - 50) // 5

    penalty4 = 10 * min(num1, num2)


    # Overall penalty score
    penalty = penalty1 + penalty2 + penalty3 + penalty4
    print(penalty1, penalty2, penalty3, penalty4)
    return penalty




if __name__ == "__main__":
    # bleh = ["111111101100001111111",
    #         "100000101001001000001",
    #         "101110101001101011101",
    #         "101110101000001011101",
    #         "101110101010001011101",
    #         "100000100010001000001",
    #         "111111101010101111111",
    #         "000000001000000000000",
    #         "011010110000101011111",
    #         "010000001111000010001",
    #         "001101110110001011000",
    #         "011011010011010101110",
    #         "100010101011101110101",
    #         "000000001101001000101",
    #         "111111101010000101100",
    #         "100000100101101101000",
    #         "101110101010001111111",
    #         "101110100101010100010",
    #         "101110101000111101001",
    #         "100000101011010001011",
    #         "111111100000111100001"]
    bleh = ["111111100001001111111",
            "100000100100001000001",
            "101110100100101011101",
            "101110101101001011101",
            "101110100111001011101",
            "100000101111001000001",
            "111111101010101111111",
            "000000001101000000000",
            "011000100101101101000",
            "000101011010010111011",
            "011000100011011110010",
            "001110000110000000100",
            "110111111110111011111",
            "000000001000011101111",
            "111111100111010000110",
            "100000100000111000010",
            "101110100111011010101",
            "101110100000000001000",
            "101110101101101000011",
            "100000101110000100001",
            "111111100101101001011"]
    bleh2 = ["11111110-----01111111",
             "10000010-----01000001",
             "10111010-----01011101",
             "10111010-----01011101",
             "10111010-----01011101",
             "10000010-----01000001",
             "111111101010101111111",
             "00000000-----00000000",
             "------1--------------",
             "------0--------------",
             "------1--------------",
             "------0--------------",
             "------1--------------",
             "000000001------------",
             "11111110-------------",
             "10000010-------------",
             "10111010-------------",
             "10111010-------------",
             "10111010-------------",
             "10000010-------------",
             "11111110-------------"]
    mat = []
    for row in bleh:
        rr = []
        for c in row:
            rr.append(int(c))
        mat.append(rr)
    
    for y in range(len(mat)):
        for x in range(len(mat)):
            if bleh2[y][x] == "-" and (y) % 2 == 0:
                mat[y][x] = 1-mat[y][x]
    

    from matrix_generation import deep_copy
    from data_masking import masking
    for mask in range(8):
        matCopy = deep_copy(mat)
        for y in range(len(mat)):
            for x in range(len(mat)):
                if bleh2[y][x] == "-":
                    matCopy[y][x] = masking(mask, matCopy[y][x], y, x)
        from matrix_generation import print_matrix
        print(mask)
        print_matrix(matCopy)
        p = evaluate_mask(matCopy, len(mat))
        print(p)
        print()
    




