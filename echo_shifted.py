from typing import List

def count_vowels(word: str) -> int:
    vowels = "aeiou"
    count = 0
    for ch in word:
        if ch in vowels:
            count += 1
    return count


def shift_word(word: str, k: int) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    shifted = []

    for ch in word:
        idx = alphabet.index(ch)
        new_idx = (idx + k) % 26
        shifted.append(alphabet[new_idx])

    return "".join(shifted)


def echo_word(word: str) -> str:
    rev = word[::-1]
    if len(word) % 2 == 0:
        return word + rev
    else:
        return rev + word


def echo_shift_decode(words: List[str]) -> List[str]:
    result = []

    for w in words:
        k = count_vowels(w) % 26
        shifted = shift_word(w, k)
        transformed = echo_word(shifted)
        result.append(transformed)

    return result


if __name__ == "__main__":
    print(echo_shift_decode(["code", "a"]))     # ["eqfggfqe", "bb"]
    print(echo_shift_decode(["bbb", "quiz"]))   # ["bbbbbb", "swkbbkws"]
