def compress_string(s: str) -> str:
    result = []
    i = 0

    while i < len(s):
        num = 1
        # count how many times s[i] repeats
        while i + num < len(s) and s[i] == s[i + num]:
            num += 1
        
        # append with or without count
        if num > 1:
            result.append(s[i] + str(num))
        else:
            result.append(s[i])
        
        i += num

    return "".join(result)


if __name__ == "__main__":
    s = input().strip()
    print(compress_string(s))
