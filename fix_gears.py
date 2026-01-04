def can_fix_gears(gears):
    count = 0
    index = -1
    
    for i in range(len(gears) - 1):
        if gears[i] >= gears[i + 1]:
            count += 1
            index = i
            
    if count == 0:
        return True
        
    if count > 1:
        return False
    
    i = index
    
    left  = gears[i - 1] if i - 1 >= 0 else float("-inf")
    a     = gears[i]
    b     = gears[i + 1]
    right = gears[i + 2] if i + 2 < len(gears) else float("inf")
    
    can_lower_left = left < b - 1
    
    can_raise_right = a < right - 1
    
    return can_lower_left or can_raise_right


# Test the hack:
print(can_fix_gears([1, 5, 3, 4]))        # True
print(can_fix_gears([10, 20, 15, 12]))    # False
print(can_fix_gears([1, 2, 10, 11]))      # True

# Extra sanity checks
print(can_fix_gears([1, 2, 2, 3]))        # True (change one 2 to 1 or 3 to make it strictly increasing)
print(can_fix_gears([3, 2, 1]))           # False (needs >=2 changes)
print(can_fix_gears([1, 3, 2]))           # True (change 3 to 1? no, change 2 to 4? no, but change 3->2? can't since strict; actually change 3->1? breaks. Change 2->4 gives [1,3,4] yes -> True)
