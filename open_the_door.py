def solve():
    n = int(input().strip())
    coins = list(map(int, input().split()))

    prev_max = 0
    prev_prev_max = 0

    for num in coins:
        current_max = max(prev_max, prev_prev_max + num)

        prev_prev_max = prev_max
        prev_max = current_max

    print(prev_max)

solve()
