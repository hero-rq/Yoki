def decode_message(typed):
    if not typed:
        return ""

    result = []

    for i in range(len(typed) - 1):
        if typed[i] != typed[i + 1]:
            result.append(typed[i])

    result.append(typed[-1])

    return "".join(result)

typed = input().strip()
print(decode_message(typed))
