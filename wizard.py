def find_overlap(a, b, min_overlap):
    """
    Find the largest overlap where the suffix of 'a' matches the prefix of 'b'.
    Returns the overlap length (0 if no overlap >= min_overlap is found).
    """
    max_possible = min(len(a), len(b))
    for size in range(max_possible, min_overlap - 1, -1):
        if a[-size:] == b[:size]:
            return size
    return 0


def merge_words(words, min_overlap):
    if not words:
        return []

    result = []
    current = words[0]

    for next_word in words[1:]:
        overlap = find_overlap(current, next_word, min_overlap)
        if overlap > 0:
            current = current + next_word[overlap:]
        else:
            result.append(current)
            current = next_word

    result.append(current)
    return result


# ---- Example usage ----
words = ["SUN", "UNDER", "DREAM", "AMBER"]
min_overlap = 2

merged = merge_words(words, min_overlap)

# Keep merging repeatedly until the list length stops changing
while True:
    prev_len = len(merged)
    merged = merge_words(merged, min_overlap)
    if len(merged) == prev_len:
        break

print(merged)
