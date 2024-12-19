# Selects error correction level. Returns: L-7%, M-15%, Q-25%, H-30%
def error_correction_level(text: str) -> str:
    return 'Q'


# Determine smallest version neccessary for the data
from information import SMALLEST_VERSION
def smallest_version(textLength: int, encodingMode: int, errorCorrectionLevel: str) -> int:
    checkArray = SMALLEST_VERSION[encodingMode][errorCorrectionLevel]

    for i in range(len(checkArray)):
        if textLength <= checkArray[i]:
            return (i+1)
    
    return -1


# Generate mode indicator
from information import MODE_INDICATOR
def mode_indicator(encodingMode: int) -> str:
    return MODE_INDICATOR[encodingMode]


# Generate character count indicator
from information import CHARACTER_COUNT_LENGTH
def character_count_indicator(textLength: int, encodingMode: int, version: int) -> str:
    idx = (0 if (1 <= version and version <= 9) else (1 if (10 <= version and version <= 26) else (2 if (27 <= version and version <= 40) else -1)))

    bits = CHARACTER_COUNT_LENGTH[encodingMode][idx]
    return bin(textLength)[2:].zfill(bits)


# Numeric mode encoding
def encode_numeric_mode(text: str, textLength: int) -> str:
    encoded = ""
    i = 0
    while i < textLength:
        current = text[i:min(i+3, textLength)]
        bits = (10 if len(current) == 3 else (7 if len(current) == 2 else 4))
        encoded += (bin(int(current))[2:].zfill(bits))
        i += 3
    return encoded


# Alphanumeric mode encoding
from information import ALPHANUMERIC
def encode_alphanumeric_mode(text: str, textLength: int) -> str:
    encoded = ""
    i = 0
    while i < textLength:
        subtext = text[i:min(i+2, textLength)]
        if i == textLength-1:
            bits = 6
            current = ALPHANUMERIC.index(subtext)
        else:
            bits = 11
            current = ALPHANUMERIC.index(subtext[0])*45+ALPHANUMERIC.index(subtext[1])
        encoded += (bin(current)[2:].zfill(bits))
        i += 2
    return encoded

# Byte mode encoding
def encode_byte_mode(text: str, textLength: int) -> str:
    encoded = ""
    bits = 8
    for i in range(textLength):
        subtext = text[i]
        current = subtext.encode("latin_1").hex()
        encoded += (bin(int(current, 16))[2:].zfill(bits))
    return encoded


# Kanji mode encoding
def encode_kanji_mode(text: str, textLength: int) -> str:
    encoded = ""
    bits = 13
    for i in range(textLength):
        subtext = text[i]
        byte_pair = (subtext.encode("shift_jis")[0], subtext.encode("shift_jis")[1])
        bytes = (byte_pair[0] << 8) | byte_pair[1]
        if int(0x8140) <= bytes and bytes <= int(0x9FFC):
            bytes -= int(0x8140)
        elif int(0xE040) <= bytes and bytes <= int(0xEBBF):
            bytes -= int(0xC140)
        left = bytes >> 8
        right = (bytes & ((1 << 8) - 1))
        current = left * int(0xC0) + right
        encoded += (bin(current)[2:].zfill(bits))
    return encoded


# Generate encoded text
def encode_text(text: str, textLength: int, encodingMode: int) -> str:
    if encodingMode == 0:
        return encode_numeric_mode(text, textLength)
    elif encodingMode == 1:
        return encode_alphanumeric_mode(text, textLength)
    elif encodingMode == 2:
        return encode_byte_mode(text, textLength)
    elif encodingMode == 3:
        return encode_kanji_mode(text, textLength)
    return ""

from information import ERROR_CORRECTION
from information import PAD_BYTES
def data_encoding(text: str, textLength: int, encodingMode: int, errorCorrectionLevel: str, version: int) -> str:
    totalBits = 8*ERROR_CORRECTION[version-1][errorCorrectionLevel][0]

    modeIndicator = mode_indicator(encodingMode)
    characterCountIndicator = character_count_indicator(textLength, encodingMode, version)
    encodedText = encode_text(text, textLength, encodingMode)
    encoded = modeIndicator + characterCountIndicator + encodedText + "0000"

    if len(encoded) >= totalBits:
        return encoded[:totalBits]
    
    encoded += ("0"*(0 if (len(encoded)%8 == 0) else (8-len(encoded)%8)))

    switch = 0
    while len(encoded) < totalBits:
        encoded += PAD_BYTES[switch]
        switch = not switch
    
    return encoded


from data_analysis import encoding_mode
if __name__ == "__main__":
    # n = int(input())
    # for i in range(n):
        text = input()
        textLength = len(text)
        encodingMode = encoding_mode(text)
        errorCorrectionLevel = error_correction_level(text)
        version = smallest_version(textLength, encodingMode, errorCorrectionLevel)
        print(data_encoding(text, textLength, encodingMode, errorCorrectionLevel, version))


