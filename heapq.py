def solve():
    n = int(input().strip())
    books = []

    total_fine = 0
    max_day = 0

    for _ in range(n):
        day, fine = map(int, input().split())
        books.append((fine, day))
        total_fine += fine
        max_day = max(max_day, day)

    # Higher fine books are more important to return safely
    books.sort(reverse=True)

    # parent[d] means: latest available day at or before d
    parent = list(range(max_day + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    saved_fine = 0

    for fine, day in books:
        available_day = find(day)

        if available_day > 0:
            # Return this book on available_day
            saved_fine += fine

            # Mark this day as used.
            # Next time, the latest available day becomes available_day - 1
            parent[available_day] = find(available_day - 1)

    print(total_fine - saved_fine)


solve()
