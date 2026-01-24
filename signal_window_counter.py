def signal_window_counter(signal: str, k: int) -> str:
    """
    Slides a window of size k over a digit string.
    For each window, counts how many digits are strictly greater than 5.
    Returns the counts concatenated as a string.
    """
    result = []

    # iterate over all valid window start positions
    for i in range(len(signal) - k + 1):
        window = signal[i:i + k]

        # count digits > 5 in the current window
        count = sum(int(digit) > 5 for digit in window)

        result.append(str(count))

    return "".join(result)


if __name__ == "__main__":
    print(signal_window_counter("564625", 3))   # "20"
    print(signal_window_counter("3525243", 2))  # "87"
