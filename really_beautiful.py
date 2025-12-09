def count_pattern(sound, pattern):
    count = 0
    i = 0
    m = len(pattern)

    for _ in range(len(sound)):
        if i > len(sound) - m:
            break  

        if sound[i:i + m] == pattern:
            count += 1
            i += m    
        else:
            i += 1     

    return count


sound = input().strip()
pattern = input().strip()
print(count_pattern(sound, pattern))
