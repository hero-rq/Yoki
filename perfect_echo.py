def analyze_signal(signal):
    n = len(signal)
    flag = 0

    # 1. Check for Perfect Echo
    # Logic: Try different 'Core' lengths from 1 up to n/2
    for length in range(1, n):
        core = signal[:length]

        # how many times core would repeat
        if length == 0:
            continue

        l = n // length

        if core * l == signal:
            flag = 1
            break

    if flag == 1:
        return "Perfect Echo"
    else:
        pass

    # 2. Check for Corrupted Echo
    # Logic: Try removing the last character and see if it's a Perfect Echo
    potential_signal = signal[:-1]
    m = len(potential_signal)

    for length in range(1, m):
        core = potential_signal[:length]

        if length == 0:
            continue

        l = m // length

        if core * l == potential_signal:
            return "Corrupted Echo"

    return "Total Noise"


# Test the hacker logic
print(analyze_signal("abcabc"))   # Expected: Perfect Echo
print(analyze_signal("abcabcx"))  # Expected: Corrupted Echo
