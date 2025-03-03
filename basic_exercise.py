def encode_message(message: str, shift: int) -> str:
    """
    Encodes the given message by shifting letters forward in the alphabet by 'shift' positions.
    Digits are also increased by 'shift' (modulo 10), while special characters remain unchanged.
    """
    eng = "abcdefghijklmnopqrstuvwxyz"
    eng2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []

    for char in message:
        if char in eng:
            l = eng.index(char)
            result.append(eng[(l + shift) % 26])  # Ensuring wrap-around
        elif char in eng2:
            l = eng2.index(char)
            result.append(eng2[(l + shift) % 26])
        elif char.isdigit():
            result.append(str((int(char) + shift) % 10))  # Handling digits
        else:
            result.append(char) 
    
    return "".join(result)  

if __name__ == "__main__":
    msg = "hello123!"
    shift_value = 3
    encoded_msg = encode_message(msg, shift_value)
    print(encoded_msg)  
