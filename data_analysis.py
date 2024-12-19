# Determines encoding mode given text string. Returns integer: 0-numeric, 1-alphanumeric, 2-byte, 3-kanji, 4-eci
from information import DIGITS
from information import ALPHANUMERIC

def encoding_mode(text: str) -> int:
    mode = 0
    for x in text:
        if not(x in DIGITS):
            mode = -1
            break
    if mode == 0:
        return 0
    
    mode = 1
    for x in text:
        if not(x in ALPHANUMERIC):
            mode = -1
            break
    if mode == 1:
        return 1
    
    try:
        text.encode("latin_1")
        return 2
    except:
        try:
            text.encode("shift_jis")
            return 3
        except:
            return -1


if __name__ == "__main__":
    n = int(input())
    for i in range(n):
        line = input()
        print(encoding_mode(line))

