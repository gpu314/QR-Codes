from typing import List

from data_analysis import encoding_mode

from data_encoding import error_correction_level
from data_encoding import smallest_version
from data_encoding import data_encoding

from error_correction_coding import final_message

from matrix_generation import matrix_generation


def display_matrix(matrix: List[List[int]]):
    black = "██"
    white = "  "
    for row in matrix:
        for col in row:
            if col == 1 or col == "1":
                print(black, end="")
            elif col == 0 or col == "0":
                print(white, end="")
            else:
                print(col*2, end="")
        print()
    print()


if __name__ == "__main__":
    text = input("Text: ")
    mode = encoding_mode(text)
    errorCorrectionLevel = error_correction_level()
    version = smallest_version(text, mode, errorCorrectionLevel)
    encodedList = data_encoding(text, mode, errorCorrectionLevel, version)
    dataBits = final_message(encodedList, version, errorCorrectionLevel)
    matrix = matrix_generation(dataBits, version, errorCorrectionLevel)
    display_matrix(matrix)
