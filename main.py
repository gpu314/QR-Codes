from typing import List

from data_analysis import encoding_mode

from data_encoding import error_correction_level
from data_encoding import smallest_version
from data_encoding import data_encoding

from error_correction_coding import final_message

from matrix_generation import matrix_generation

BLACK = "██"
WHITE = "░░"

# Displays QR code matrix onto python console
def display_matrix(matrix: List[List[int]]) -> None:
    for row in matrix:
        for col in row:
            if col == 1:
                print(BLACK, end="")
            elif col == 0:
                print(WHITE, end="")
            else:
                print(col*2, end="")
        print()
    print()


# Returns string array containing rows of QR code matrix
def return_matrix(matrix: List[List[int]]) -> List[str]:
    result = []
    for row in matrix:
        rowResult = ""
        for col in row:
            if col == 1 or col == "1":
                rowResult += BLACK
            elif col == 0 or col == "0":
                rowResult += WHITE
            else:
                rowResult += str(col)*2
        result.append(rowResult)
    return result


# Displays QR code matrix on python console given string array containing rows of QR code matrix
def display_return_matrix(matrix: List[List[int]]) -> None:
    result = return_matrix(matrix)
    for row in result:
        print(row)
    print()


# Returns 2D matrix with 1s/0s representing QR code, given text and error correction level
def qr_code_encoding(text, errorCorrectionLevel) -> List[List[int]]:
    mode = encoding_mode(text)
    version = smallest_version(text, mode, errorCorrectionLevel)
    encodedList = data_encoding(text, mode, errorCorrectionLevel, version)
    dataBits = final_message(encodedList, version, errorCorrectionLevel)
    matrix = matrix_generation(dataBits, version, errorCorrectionLevel)
    return matrix


# Text QR code
def main_text(text, errorCorrectionLevel) -> List[str]:
    matrix = qr_code_encoding(text, errorCorrectionLevel)
    return return_matrix(matrix)


# PNG QR code, returns -1 if unsuccessful and 0 if successful
from PIL import Image
def main_png(text, errorCorrectionLevel, fileName) -> int:
    matrix = qr_code_encoding(text, errorCorrectionLevel)
    try:
        size = len(matrix)
        img = Image.new('1', (size, size), color=1)
        pixels = img.load()
        for y in range(size):
            for x in range(size):
                pixels[x, y] = 1-matrix[y][x]
        img.save(fileName+".png")
        return 0
    except:
        return -1


if __name__ == "__main__":
    text = input("Text: ")
    errorCorrectionLevel = error_correction_level()
    fileName = input("File name: ")
    # display_matrix(qr_code_encoding(text, errorCorrectionLevel))
    # display_return_matrix(main_text(text, errorCorrectionLevel))
    if main_png(text, errorCorrectionLevel, fileName) == -1:
        print("ERROR")
    else:
        print("YAHOO")
