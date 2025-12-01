def count_valleys(steps):
    height = 0
    valleys = 0
    
    for step in steps:
        if step > 0:
            height += step
        else:
            height += step
        
        if height == 0 and step > 0:
            valleys += 1
    
    return valleys

steps = list(map(int, input().split()))
print(count_valleys(steps))
