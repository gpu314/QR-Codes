from typing import List


# Go through border and change
def border(matrix: List[List[int]], size: int, topLeftX: int, topLeftY: int, newVal: int, borderSize: int) -> List[List[int]]:
    for i in range(borderSize):
        cells = [(topLeftX+i, topLeftY), (topLeftX+borderSize-1, topLeftY+i), (topLeftX+borderSize-1-i, topLeftY+borderSize-1), (topLeftX, topLeftY+borderSize-1-i)]
        for c in cells:
            if c[0] < 0 or c[1] < 0 or c[0] >= size or c[1] >= size:
                continue
            matrix[c[1]][c[0]] = newVal
    return matrix


# Singular finder pattern
FINDER_OUTER = 7
FINDER_MIDDLE = 5
FINDER_INNER1 = 3
FINDER_INNER2 = 1
def finder_pattern(matrix: List[List[int]], size: int, topLeftX: int, topLeftY: int) -> List[List[int]]:
    matrix = border(matrix, size, topLeftX, topLeftY, 1, FINDER_OUTER)
    matrix = border(matrix, size, topLeftX+(FINDER_OUTER-FINDER_MIDDLE)//2, topLeftY+(FINDER_OUTER-FINDER_MIDDLE)//2, 0, FINDER_MIDDLE)
    matrix = border(matrix, size, topLeftX+(FINDER_OUTER-FINDER_INNER1)//2, topLeftY+(FINDER_OUTER-FINDER_INNER1)//2, 1, FINDER_INNER1)
    matrix = border(matrix, size, topLeftX+(FINDER_OUTER-FINDER_INNER2)//2, topLeftY+(FINDER_OUTER-FINDER_INNER2)//2, 1, FINDER_INNER2)
    return matrix


# Add finder patterns
def finder_patterns(matrix: List[List[int]], size: int) -> List[List[int]]:
    matrix = finder_pattern(matrix, size, 0, 0)                   # Top Left. (0,0)
    matrix = finder_pattern(matrix, size, size-FINDER_OUTER, 0)   # Top Right. (size-FINDER_OUTER,0)
    matrix = finder_pattern(matrix, size, 0, size-FINDER_OUTER)   # Bottom Left. (0,size-FINDER_OUTER)
    return matrix


# Add separators
SEPARATOR = 9
def separators(matrix: List[List[int]], size: int) -> List[List[int]]:
    matrix = border(matrix, size, -1, -1, 0, SEPARATOR)                 # Top Left. (-1,-1)
    matrix = border(matrix, size, size-SEPARATOR+1, -1, 0, SEPARATOR)   # Top Right. (size-SEPARATOR-1,-1)
    matrix = border(matrix, size, -1, size-SEPARATOR+1, 0, SEPARATOR)   # Bottom Left. (-1,size-SEPARATOR-1)
    return matrix


# Check if empty
def isEmpty(matrix: List[List[int]], size: int, topLeftX: int, topLeftY: int, patternSize: int) -> bool:
    for y in range(topLeftY, topLeftY+patternSize):
        for x in range(topLeftX, topLeftX+patternSize):
            if x < 0 or y < 0 or x >= size or y >= size:
                continue
            if matrix[y][x] != -1:
                return False
    return True


from information import ALIGNMENT_PATTERN_LOCATIONS
# Add alignment patterns
ALIGNMENT_OUTER = 5
ALIGNMENT_MIDDLE = 3
ALIGNMENT_INNER = 1
def alignment_patterns(matrix: List[List[int]], version: int, size: int) -> List[List[int]]:
    alignmentLocations = ALIGNMENT_PATTERN_LOCATIONS[version-1]
    centers = [(x, y) for x in alignmentLocations for y in alignmentLocations]
    for center in centers:
        if isEmpty(matrix, size, center[0]-ALIGNMENT_OUTER//2, center[1]-ALIGNMENT_OUTER//2, ALIGNMENT_OUTER):
            matrix = border(matrix, size, center[0]-ALIGNMENT_OUTER//2, center[1]-ALIGNMENT_OUTER//2, 1, ALIGNMENT_OUTER)
            matrix = border(matrix, size, center[0]-ALIGNMENT_MIDDLE//2, center[1]-ALIGNMENT_MIDDLE//2, 0, ALIGNMENT_MIDDLE)
            matrix = border(matrix, size, center[0]-ALIGNMENT_INNER//2, center[1]-ALIGNMENT_INNER//2, 1, ALIGNMENT_INNER)
    return matrix


# Add timing patterns
def timing_patterns(matrix: List[List[int]], size: int) -> List[List[int]]:
    for x in range(FINDER_OUTER, size-FINDER_OUTER-1):
        matrix[FINDER_OUTER-1][x] = (1 if x%2 == 0 else 0)
    for y in range(FINDER_OUTER, size-FINDER_OUTER-1):
        matrix[y][FINDER_OUTER-1] = (1 if y%2 == 0 else 0)
    return matrix


# Add dark pixel
def dark_pixel(matrix: List[List[int]], version: int) -> List[List[int]]:
    matrix[4*version+9][8] = 1
    return matrix


# Add format information area, denote by 2
def format_information_area(matrix: List[List[int]], size: int) -> List[List[int]]:
    for x in range(SEPARATOR):
        if x == 6:
            continue
        matrix[SEPARATOR-1][x] = 2
    for x in range(size-SEPARATOR+1, size):
        matrix[SEPARATOR-1][x] = 2
    for y in range(SEPARATOR):
        if y == 6:
            continue
        matrix[y][SEPARATOR-1] = 2
    for y in range(size-SEPARATOR+2, size):
        matrix[y][SEPARATOR-1] = 2
    return matrix


# Add version information area, denote by 3
def version_information_area(matrix: List[List[int]], version: int, size: int) -> List[List[int]]:
    if version < 7:
        return matrix
    for x in range(size-SEPARATOR-2, size-SEPARATOR+1):
        for y in range(FINDER_OUTER-1):
            matrix[y][x] = 3
    for y in range(size-SEPARATOR-2, size-SEPARATOR+1):
        for x in range(FINDER_OUTER-1):
            matrix[y][x] = 3
    return matrix


# Format information string
def format_string(errorCorrectionLevel: str, mask: int) -> str:
    string = ERROR_CORRECTION_BITS[errorCorrectionLevel] + bin(mask)[2:].zfill(3)

    message = [int(x) for x in (string[::-1].zfill(15))[::-1]]

    # Remove leading 0s
    while len(message) > 0 and message[0] == 0:
        message.pop(0)
    
    generatorPolynomial = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1]

    # Polynomial division
    while len(message) >= 11:
        nextMessage = []
        currentGenerator = generatorPolynomial + [0]*max(0, len(message)-len(generatorPolynomial))
        for i in range(len(message)):
            nextMessage.append(message[i]^currentGenerator[i])
        message = nextMessage
        while len(message) > 0 and message[0] == 0:
            message.pop(0)
    
    # Left padding with 0s if length less than 10
    while len(message) < 10:
        message.insert(0, 0)
    
    newString = [int(x) for x in string] + message
    maskString = [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]

    answer = [newString[i] ^ maskString[i] for i in range(len(newString))]

    return "".join(str(x) for x in answer)


# Format information
from information import ERROR_CORRECTION_BITS
def format_information(matrix: List[List[int]], size: int, formatString: str):
    idx = 0
    for x in range(SEPARATOR):
        if x == 6:
            continue
        matrix[SEPARATOR-1][x] = formatString[idx]
        idx += 1
    for y in range(SEPARATOR-2, -1, -1):
        if y == 6:
            continue
        matrix[y][SEPARATOR-1] = formatString[idx]
        idx += 1
    idx = 0
    for y in range(size-1, size-SEPARATOR+1, -1):
        matrix[y][SEPARATOR-1] = formatString[idx]
        idx += 1
    for x in range(size-SEPARATOR+1, size):
        matrix[SEPARATOR-1][x] = formatString[idx]
        idx += 1
    return matrix


# Version information string
def version_string(version: int) -> str:
    string = bin(version)[2:].zfill(6)

    message = [int(x) for x in (string[::-1].zfill(18))[::-1]]

    # Remove leading 0s
    while len(message) > 0 and message[0] == 0:
        message.pop(0)
    
    generatorPolynomial = [1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1]

    # Polynomial division
    while len(message) >= 13:
        nextMessage = []
        currentGenerator = generatorPolynomial + [0]*max(0, len(message)-len(generatorPolynomial))
        for i in range(len(message)):
            nextMessage.append(message[i]^currentGenerator[i])
        message = nextMessage
        while len(message) > 0 and message[0] == 0:
            message.pop(0)
    
    # Left padding with 0s if length less than 12
    while len(message) < 12:
        message.insert(0, 0)
    
    answer = [int(x) for x in string] + message
    answer = answer[::-1]

    return "".join(str(x) for x in answer)


# Version information
def version_information(matrix: List[List[int]], version: int, size: int, versionString: str) -> List[List[int]]:
    if version < 7:
        return matrix
    idx = 0
    for x in range(FINDER_OUTER-1):
        for y in range(size-SEPARATOR, size-SEPARATOR-3, -1):
            matrix[y][x] = versionString[idx]
            idx += 1
    idx = 0
    for x in range(size-SEPARATOR-2, size-SEPARATOR+1):
        for y in range(FINDER_OUTER-1):
            matrix[y][x] = versionString[idx]
            idx += 1
    return matrix
    

if __name__ == "__main__":
    for ecl in ["L", "M", "Q", "H"]:
        for mask in range(8):
            print(format_string(ecl, mask))
    for version in range(7, 41):
        print(version_string(version))

