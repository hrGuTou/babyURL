digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
          'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
          'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def toBase62(input):
    res = []

    while (input > 0):
        res.append(digits[input % 62])
        input = int(input / 62)

    return ''.join(res[::-1])


def toBase10(input):
    res = 0
    base = 1
    for i in range(len(input)-1, -1, -1):
        idx =0
        for j in range(len(digits)):
            if digits[j] == input[i]:
                idx = j
        res += idx * base
        base *= 62

    return res


if __name__ == "__main__":
    print(toBase62(100))
    print(toBase10("1C"))
