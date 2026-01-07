def count_happy_plants(heights):
    # We need at least 3 plants for any to be happy
    if len(heights) < 3:
        return 0
    
    happy_count = 0
    
    # Loop through the plants, skipping the first and last (the lonely edges)
    for i in range(1, len(heights) - 1):
        current = heights[i]
        left = heights[i-1]
        right = heights[i+1]
        
        if current != left and current != right:
            if current > left or current > right:
                happy_count += 1
            
    return happy_count

# Test your logic:
print(count_happy_plants([1, 5, 2, 8, 3])) # Should return 2
print(f"Plateau Test [5, 5, 8, 2]: {count_happy_plants([5, 5, 8, 2])}") # Expected: 1
print(f"Mountain Test [1, 3, 2, 4, 3]: {count_happy_plants([1, 3, 2, 4, 3])}") # Expected: 2
