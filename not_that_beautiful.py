def smallest_cover_window(text, need):
    len_t = len(text)
    len_n = len(need)

    start_i = -1
    end_i = -1

    for i in range(0, len_t - len_n + 1):
        current_substring = text[i:i + len_n]
        if current_substring == need:
            start_i = i
            break

    if start_i == -1:
        print("")
        return ""

    for i in range(len_t - len_n, start_i - 1, -1):
        current_substring = text[i:i + len_n]
        if current_substring == need:
            end_i = i + len_n  # make end_i an "end index" (exclusive)
            break

    for i in range(start_i, end_i):
        print(text[i])

    return text[start_i:end_i]


text = input().strip()
need = input().strip()
print(smallest_cover_window(text, need))
