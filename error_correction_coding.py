# Reed–Solomon error correction

# Returns 2**exponent in Galois field 256 modulo 100011101 = 285
from information import ANTILOG
def antilog(exponent: int) -> int:
    exponent %= 255
    return ANTILOG[exponent]

# Returns log base 2 of argument in Galois field 256 modulo 100011101 = 285
from information import LOG
def log(argument: int) -> int:
    return LOG[argument-1]


# Returns the coefficients of the generator polynomial as an array containing a_n
# Where 2**a_n = exponent of x^n term. Utilizes recursion: GP(0) -> None, GP(1) -> [0, 0], GP(n) = GP(n-1) * (x+2^(n-1))
from typing import List
def generator_polynomial(errorCorrectionCodewords: int) -> List[int]:
    if errorCorrectionCodewords < 1:
        return None
    if errorCorrectionCodewords == 1:
        return [0, 0]
    
    previous_generator_polynomial = generator_polynomial(errorCorrectionCodewords-1)

    if previous_generator_polynomial == None:
        return None
    
    new_generator_polynomial = [0]
    for i in range(1, errorCorrectionCodewords):
        p1 = antilog((previous_generator_polynomial[i]) % 255)
        p2 = antilog((previous_generator_polynomial[i-1] + (errorCorrectionCodewords-1)) % 255)
        new_generator_polynomial.append(log(p1^p2))
    new_generator_polynomial.append(previous_generator_polynomial[i]+errorCorrectionCodewords-1)

    return new_generator_polynomial


# Returns codewords array converted from binary string to decimal integers
def codewords_binary_to_decimal(codewords: List[str]) -> List[int]:
    decimal = [int(x, 2) for x in codewords]
    return decimal


# Returns number of error correction codewords given version number and error correction level
from information import ERROR_CORRECTION
def number_error_correction_codewords(version: int, errorCorrectionLevel: str) -> int:
    return ERROR_CORRECTION[version-1][errorCorrectionLevel][1]


# Scalar multiplication by 2**a to polynomial coefficients 2**(a_n)
def polynomial_scalar_multiplication(scalar: int, polynomial: List[int]):
    newPolynomial = [((scalar+x)%255) for x in polynomial]
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
        sum.append(longer[i]^shorter[i])
    for i in range(len(shorter), len(longer)):
        sum.append(longer[i]^0)
    
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


# Main function, error correction coding
def error_correction_coding(codewords: List[str], errorCorrectionCodewords: int):
    messagePolynomial = codewords_binary_to_decimal(codewords)
    generatorPolynomial = generator_polynomial(errorCorrectionCodewords)

if __name__ == "__main__":
    # tmp = ['00100000', '01011011', '00001011', '01111000', '11010001', '01110010', '11011100', '01001101', '01000011', '01000000', '11101100', '00010001', '11101100', '00010001', '11101100', '00010001']
    # print(codewords_binary_to_decimal(tmp))
    # print(generator_polynomial(10))
    p = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    q = [0, 251, 67, 46, 61, 118, 70, 64, 94, 32, 45]
    r = polynomial_division(p, q)
    print(r)
