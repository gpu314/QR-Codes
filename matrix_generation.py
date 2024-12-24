from typing import List, Tuple

# Determines size (side length) of QR code from version
def size(version: int) -> int:
    return (4*(version-1)+21)


# Generates empty matrix of given size
def empty_matrix(size: int) -> List[List[int]]:
    m = [[-1 for j in range(size)] for i in range(size)]
    return m


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
def finder_pattern(matrix: List[List[int]], topLeftX: int, topLeftY: int) -> List[List[int]]:
    matrix = border(matrix, size, topLeftX, topLeftY, 1, FINDER_OUTER)
    matrix = border(matrix, size, topLeftX+(FINDER_OUTER-FINDER_MIDDLE)//2, topLeftY+(FINDER_OUTER-FINDER_MIDDLE)//2, 0, FINDER_MIDDLE)
    matrix = border(matrix, size, topLeftX+(FINDER_OUTER-FINDER_INNER1)//2, topLeftY+(FINDER_OUTER-FINDER_INNER1)//2, 1, FINDER_INNER1)
    matrix = border(matrix, size, topLeftX+(FINDER_OUTER-FINDER_INNER2)//2, topLeftY+(FINDER_OUTER-FINDER_INNER2)//2, 1, FINDER_INNER2)
    return matrix


# Add finder patterns
def finder_patterns(matrix: List[List[int]], size: int) -> List[List[int]]:
    matrix = finder_pattern(matrix, 0, 0)                   # Top Left. (0,0)
    matrix = finder_pattern(matrix, size-FINDER_OUTER, 0)   # Top Right. (size-FINDER_OUTER,0)
    matrix = finder_pattern(matrix, 0, size-FINDER_OUTER)   # Bottom Left. (0,size-FINDER_OUTER)
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
        matrix[SEPARATOR-1][x] = 2
    for x in range(size-SEPARATOR+1, size):
        matrix[SEPARATOR-1][x] = 2
    for y in range(SEPARATOR):
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
    d = xydv[2] # direction: 1 = up, -1 = down
    v = xydv[3] # reached vertical bar: 0 = no, 1 = yes

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


# Place data bits
def data_bits(matrix: List[List[int]], size: int, dataBits: str) -> List[List[int]]:
    idx = 0
    curr = (size-1, size-1, 1, 0)
    x = curr[0]
    y = curr[1]
    while curr[0] > -2:
        x = curr[0]
        y = curr[1]
        # Only place data bit if pixel at coordinates not already occupied from preamble
        if x >= 0 and y >= 0 and x < size and y < size and matrix[y][x] == -1:
            matrix[y][x] = dataBits[idx]
            idx += 1
        curr = next_data_bit(matrix, size, curr)
    return matrix

# Testing, display matrix, temporary function
def print_matrix(matrix: List[List[int]]):
    for row in matrix:
        for col in row:
            if col == -1:
                print("-",end="")
            else:
                print(col,end="")
        print()
    print()


# Testing
if __name__ == "__main__":
    version = 5
    size = size(version)
    mat = empty_matrix(size)
    mat = preamble(mat, version, size)
    data = "01000011111101101011011001000110010101011111011011100110111101110100011001000010111101110111011010000110000001110111011101010110010101110111011000110010110000100010011010000110000001110000011001010101111100100111011010010111110000100000011110000110001100100111011100100110010101110001000000110010010101100010011011101100000001100001011001010010000100010001001011000110000001101110110000000110110001111000011000010001011001111001001010010111111011000010011000000110001100100001000100000111111011001101010101010111100101001110101111000111110011000111010010011111000010110110000010110001000001010010110100111100110101001010110101110011110010100100110000011000111101111011011010000101100100111111000101111100010010110011101111011111100111011111001000100001111001011100100011101110011010101111100010000110010011000010100010011010000110111100001111111111011101011000000111100110101011001001101011010001101111010101001001101111000100010000101000000010010101101010001101101100100000111010000110100011111100000010000001101111011110001100000010110010001001111000010110001101111011000000000"
    mat = data_bits(mat, size, data)
    print_matrix(mat)