digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
          'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
          'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def toBase62(input):
    chs = []
    while input > 0:
        r = input % 62
        input //= 62

        chs.append(digits[r])

    if len(chs) > 0:
        chs.reverse()
    else:
        chs.append("0")

    s = "".join(chs)
    s = digits[0] * max(1 - len(s), 0) + s
    return s


def toBase10(input):
    res = 0
    base = len(digits)
    inputLen = len(input)

    idx = 0
    for char in input:
        power = (inputLen-(idx+1))
        res += digits.index(char) * (base**power)
        idx += 1

    return res


if __name__ == "__main__":
    print(toBase62(1909146547183030277))
    print(toBase10("asdfasdfajiojoijoij"))
