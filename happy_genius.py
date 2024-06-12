def caesar_cipher(text, shift):
    def shift_char(c, shift):
        if c.isalpha():
            ascii_offset = ord('A') if c.isupper() else ord('a')
            shifted = chr((ord(c) - ascii_offset + shift) % 26 + ascii_offset)
            return shifted
        else:
            return c
    
    encoded_text = ""
    for char in text:
        encoded_text += shift_char(char, shift)

    return encoded_text

def get_user_input():
    text = input("Enter the text to be encrypted: ")
    while True:
        try:
            shift = int(input("Enter the shift amount: "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer for the shift amount.")
    return text, shift

def main():
    text, shift = get_user_input()
    encrypted_text = caesar_cipher(text, shift)
    print("Encrypted text:", encrypted_text)

def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

def run_tests():
    test_cases = [
        ("Hello, World!", 3, "Khoor, Zruog!"),
        ("abcXYZ", 2, "cdeZAB"),
        ("Python", 5, "Udymts"),
        ("Caesar Cipher", 4, "Geiwev Gmtliv")
    ]
    
    for i, (text, shift, expected) in enumerate(test_cases):
        result = caesar_cipher(text, shift)
        assert result == expected, f"Test case {i+1} failed: {result} != {expected}"
        print(f"Test case {i+1} passed.")

if __name__ == "__main__":
    main()
