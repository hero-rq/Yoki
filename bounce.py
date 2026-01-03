def stabilize_echo(word, bounce_count):
    transmission = [word]
    
    current_word = word
    
    for _ in range(bounce_count):
        # 1. Check if current_word is long enough to bounce (>= 3 letters)
        if len(current_word) < 3:
            break
        # 2. Slice the word to remove the first and last characters
        current_word = current_word[1:-1]
        # 3. Add the new word to the 'transmission' list
        transmission.append(current_word)
        # 4. Break the loop if the word can't bounce anymore
        pass 

    return "-".join(transmission)

print(stabilize_echo("PLANET", 2)) # Expected: PLANET-LANE-AN
