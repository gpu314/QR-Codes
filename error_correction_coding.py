# Reed–Solomon error correction
from information import ERROR_CORRECTION
from typing import List
from information import LOG
from information import ANTILOG


# Returns 2**exponent in Galois field 256 modulo 100011101 = 285
def antilog(exponent: int) -> int:
    if exponent == 999:
        return 0
    exponent %= 255
    return ANTILOG[exponent]


# Returns log base 2 of argument in Galois field 256 modulo 100011101 = 285
def log(argument: int) -> int:
    if argument == 0:
        return 999
    return LOG[argument-1]


# Returns the coefficients of the generator polynomial as an array containing a_n
# Where 2**a_n = exponent of x^n term. Utilizes recursion: GP(0) -> None, GP(1) -> [0, 0], GP(n) = GP(n-1) * (x+2^(n-1))
def generator_polynomial(errorCorrectionCodewords: int) -> List[int]:
    if errorCorrectionCodewords < 1:
        return None
    if errorCorrectionCodewords == 1:
        return [0, 0]

    previous_generator_polynomial = generator_polynomial(
        errorCorrectionCodewords-1)

    if previous_generator_polynomial == None:
        return None

    new_generator_polynomial = [0]
    for i in range(1, errorCorrectionCodewords):
        p1 = antilog((previous_generator_polynomial[i]) % 255)
        p2 = antilog(
            (previous_generator_polynomial[i-1] + (errorCorrectionCodewords-1)) % 255)
        new_generator_polynomial.append(log(p1 ^ p2))
    new_generator_polynomial.append(
        previous_generator_polynomial[i]+errorCorrectionCodewords-1)

    return new_generator_polynomial


# Returns codewords array converted from binary string to decimal integers
def codewords_binary_to_decimal(codewords: List[str]) -> List[int]:
    decimal = [int(x, 2) for x in codewords]
    return decimal


# Returns number of error correction codewords given version number and error correction level
def number_error_correction_codewords(version: int, errorCorrectionLevel: str) -> int:
    return ERROR_CORRECTION[version-1][errorCorrectionLevel][1]


# Scalar multiplication by 2**a to polynomial coefficients 2**(a_n)
def polynomial_scalar_multiplication(scalar: int, polynomial: List[int]):
    newPolynomial = [((scalar+x) % 255) for x in polynomial]
    return newPolynomial


# Polynomial addition assuming same degree of leading term
# Performs XOR
def polynomial_addition(p1: List[int], p2: List[int]):
    longer = []
    shorter = []
    sum = []
    if len(p1) >= len(p2):
        longer = [antilog(x) for x in p1]
        shorter = [antilog(x) for x in p2]
    else:
        longer = [antilog(x) for x in p2]
        shorter = [antilog(x) for x in p1]

    for i in range(len(shorter)):
        sum.append(longer[i] ^ shorter[i])
    for i in range(len(shorter), len(longer)):
        sum.append(longer[i] ^ 0)

    while len(sum) > 0 and sum[0] == 0:
        sum.pop(0)
    
    result = [log(x) for x in sum]
    return result


# Returns the coefficients of the remainder after polynomial long division
# Operates in Galois field 256 modulo 100011101 = 285 arithmetic
def polynomial_division(dividend: List[int], divisor: List[int]) -> List[int]:
    a = [log(x) for x in dividend]
    b = [x for x in divisor]
    for i in range(len(dividend)):
        leading = a[0]
        toAdd = polynomial_scalar_multiplication(leading, b)
        a = polynomial_addition(a, toAdd)
    answer = [antilog(x) for x in a]
    return answer


# Individual error correction coding for a specific block
def block_error_correction_coding(messagePolynomial: List[int], errorCorrectionCodewords: int) -> List[int]:
    generatorPolynomial = generator_polynomial(errorCorrectionCodewords)
    answerPolynomial = polynomial_division(messagePolynomial, generatorPolynomial)
    return answerPolynomial


# Blocks up codewords according to version and error correction level
def blocking(codewords: List[str], version: int, errorCorrectionLevel: str) -> List[List[List[str]]]:
    answer = []
    idx = 0
    for x in ERROR_CORRECTION[version-1][errorCorrectionLevel][3:]:
        group = []
        for _ in range(x[0]):
            block = []
            for i in range(x[1]):
                block.append(codewords[idx+i])
            group.append(block)
            idx += x[1]
        answer.append(group)
    return answer


# Interleave blocks of codewords/error corrections
def interleave(toInterleave: List[List[List[int]]]) -> List[int]:
    blocks = []
    maxLength = 0
    for group in toInterleave:
        for block in group:
            blocks.append(block)
            maxLength = max(maxLength, len(block))
    
    interleaved = []
    for i in range(maxLength):
        for block in blocks:
            if i >= len(block):
                continue
            interleaved.append(block[i])
    
    return interleaved


# Converts blocked codewords from binary to decimal
def blocked_codewords_convert(blockedCodewords: List[List[List[str]]]) -> List[List[List[int]]]:
    blockedCodewordsConverted = []
    for group in blockedCodewords:
        new_group = []
        for block in group:
            new_group.append(codewords_binary_to_decimal(block))
        blockedCodewordsConverted.append(new_group)
    return blockedCodewordsConverted


# Generates error correction coding for integer blocked codewords
def error_correction_coding(blockedCodewordsConverted: List[List[List[int]]], version: int, errorCorrectionLevel: str):
    errorCorrectionCodewords = number_error_correction_codewords(version, errorCorrectionLevel)
    errorCorrection = []
    for group in blockedCodewordsConverted:
        errorCorrectionGroup = []
        for block in group:
            errorCorrectionGroup.append(block_error_correction_coding(block, errorCorrectionCodewords))
        errorCorrection.append(errorCorrectionGroup)
    return errorCorrection

from information import REMAINDER_BITS
# Main function. Combines codewords / error correction coding and adds remainder bits as necessary
def final_message(codewords: List[str], version: int, errorCorrectionLevel: str):
    blockedCodewords = blocking(codewords, version, errorCorrectionLevel)
    blockedCodewordsConverted = blocked_codewords_convert(blockedCodewords)
    errorCorrectionCodes = error_correction_coding(blockedCodewordsConverted, version, errorCorrectionLevel)
    
    interleavedCodewords = interleave(blockedCodewordsConverted)
    interleavedErrorCorrection = interleave(errorCorrectionCodes)

    bits = 8
    answer = "".join([bin(x)[2:].zfill(bits) for x in interleavedCodewords]) + "".join([bin(x)[2:].zfill(bits) for x in interleavedErrorCorrection]) + "0"*REMAINDER_BITS[version-1]

    return answer
            
    
if __name__ == "__main__":
    p = ["01000011","01010101","01000110","10000110","01010111","00100110","01010101","11000010","01110111","00110010","00000110","00010010","00000110","01100111","00100110","11110110","11110110","01000010","00000111","01110110","10000110","11110010","00000111","00100110","01010110","00010110","11000110","11000111","10010010","00000110","10110110","11100110","11110111","01110111","00110010","00000111","01110110","10000110","01010111","00100110","01010010","00000110","10000110","10010111","00110010","00000111","01000110","11110111","01110110","01010110","11000010","00000110","10010111","00110010","00010000","11101100","00010001","11101100","00010001","11101100","00010001","11101100"]
    print(final_message(p, 5, 'Q'))
    print()
    q = ["01000011","01010101","01000110","10000110","01010111","00100110","01010101","11000010","01110111","00110010","00000110","00010010","00000110","01100111","00100110","11110110","11110110","01000010","00000111","01110110","10000110","11110010","00000111","00100110","01010110","00010110","11000110","11000111","10010010","00000110","10110110","11100110","11110111","01110111","00110010","00000111","01110110","10000110","01010111","00100110","01010010","00000110","10000110","10010111","00110010","00000111","01000110","11110111","01110110","01010110","11000010","00000110","10010111","00110010","11100000","11101100","00010001","11101100","00010001","11101100","00010001","11101100"]
