# Problem: Secure Password Generator
# 
# Create a Python program that generates a secure password based on user input.
# The program should ask the user for the desired length and whether they want to include:
# - Uppercase letters
# - Lowercase letters
# - Numbers
# - Special characters
#
# The program should then generate a random password that meets the user's criteria.
#
# Constraints:
# - The minimum password length is 6 characters.
# - The maximum password length is 64 characters.
# - The program should handle invalid inputs gracefully.

import random
import string

def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_special):
    if length < 6 or length > 64:
        raise ValueError("Password length must be between 6 and 64 characters.")
    
    char_pool = ""
    if use_uppercase:
        char_pool += string.ascii_uppercase
    if use_lowercase:
        char_pool += string.ascii_lowercase
    if use_numbers:
        char_pool += string.digits
    if use_special:
        char_pool += string.punctuation
    
    if not char_pool:
        raise ValueError("At least one character type must be selected.")
    
    return "".join(random.choice(char_pool) for _ in range(length))

def verify_password(password, use_uppercase, use_lowercase, use_numbers, use_special):
    if len(password) < 6 or len(password) > 64:
        return False
    
    has_upper = any(char in string.ascii_uppercase for char in password) if use_uppercase else True
    has_lower = any(char in string.ascii_lowercase for char in password) if use_lowercase else True
    has_digit = any(char in string.digits for char in password) if use_numbers else True
    has_special = any(char in string.punctuation for char in password) if use_special else True
    
    return has_upper and has_lower and has_digit and has_special

# Example usage
if __name__ == "__main__":
    try:
        length = int(input("Enter password length (6-64): "))
        use_uppercase = input("Include uppercase letters? (y/n): ").strip().lower() == "y"
        use_lowercase = input("Include lowercase letters? (y/n): ").strip().lower() == "y"
        use_numbers = input("Include numbers? (y/n): ").strip().lower() == "y"
        use_special = input("Include special characters? (y/n): ").strip().lower() == "y"
        
        password = generate_password(length, use_uppercase, use_lowercase, use_numbers, use_special)
        print(f"Generated password: {password}")
        
        print("Password verification result:", verify_password(password, use_uppercase, use_lowercase, use_numbers, use_special))
    except ValueError as e:
        print(f"Error: {e}")
