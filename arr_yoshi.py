# func2: Adds 3 to the input value and returns the result
def func2(x):
    result = x + 3
    return result

# func1: Processes the input value by repeatedly dividing by 2 and conditionally
# calling func2 to update the result based on the least significant bit
def func1(x):
    result = 0
    print("Starting func1 with x =", x)

    while x != 0:
        print("Current x =", x, "result =", result)
        if x & 1:
            result = func2(result)
            print("Updated result after func2 =", result)
        x >>= 1
        print("Updated x after shifting =", x)

    return result

# main: Reads an input number, calls func1, and prints the result
def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: {} <number>".format(sys.argv[0]))
        return 1

    x = int(sys.argv[1])
    print("Input number:", x)
    result = func1(x)
    print("Result:", result)

if __name__ == "__main__":
    main()
