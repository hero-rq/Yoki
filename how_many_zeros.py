def longest_calm_stretch(values):
    max_length = 0
    current_length = 0

    for value in values:
        if value == 0:
            current_length = current_length + 1
        else:
            if current_length > max_length:
                max_length = current_length
            current_length = 0
    
    if current_length > max_length:
        max_length = current_length
        
    return max_length

try:
    values = list(map(int, input().split()))
    print(longest_calm_stretch(values))
except ValueError:
    pass
