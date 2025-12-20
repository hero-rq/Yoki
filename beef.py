def shortest_full_distinct_window(s: str) -> int:
    target = set(s)
    need = len(target)

    count = {}
    start = 0
    have = 0
    best = float("inf")

    for end, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        if count[ch] == 1:
            have += 1

        while have == need:
            best = min(best, end - start + 1)

            left = s[start]
            count[left] -= 1
            if count[left] == 0:
                have -= 1
                # optional: del count[left]
            start += 1

    return -1 if best == float("inf") else best


s = input().strip()
print(shortest_full_distinct_window(s))
