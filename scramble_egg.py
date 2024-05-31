import random

def user_guess():
    return input("\nPlease make a guess: ")

def provide_hint(word):
    print(f"'{word[0]}' is the first letter")
    print(f"The length of the word: {len(word)}\n")

def scramble_word(word):
    word = list(word)
    random.shuffle(word)
    return ''.join(word)

def word_scramble_game():
    words = ["apple", "banana", "orange", "grape", "strawberry", "mango"]
    word_to_guess = random.choice(words)
    scrambled_word = scramble_word(word_to_guess)
    
    print("Welcome to the Word Scramble Game!\n")
    print(f"{scrambled_word}\nThis is the scrambled word.")
    print("Can you guess the original word?")
    
    for i in range(5):
        user_input = user_guess()
        if user_input != word_to_guess:
            provide_hint(word_to_guess)
        else:
            print("OMG! You are a genius!")
            break
        if i == 4:
            print("Out of attempts! The original word is:")
            print(word_to_guess)
            break    

word_scramble_game()
