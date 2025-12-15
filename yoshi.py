def min_moves_to_balance(boxes):
    n = len(boxes)
    t = sum(boxes)
    if t % n != 0:
        return -1
    u = t // n

    moves = 0
    d = 0
    for i in range(n - 1):
        d += boxes[i] - u      # running imbalance
        moves += abs(d)        # balls crossing boundary i->i+1
    return moves

boxes = list(map(int, input().split()))
print(min_moves_to_balance(boxes))
