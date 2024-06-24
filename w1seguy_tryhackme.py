import socket
import binascii
import argparse

def derive_key_part(hex_encoded, known_plaintext, start_index):
    encrypted_bytes = bytes.fromhex(hex_encoded)
    derived_key = ""
    
    for i in range(len(known_plaintext)):
        derived_key += chr(encrypted_bytes[start_index + i] ^ ord(known_plaintext[i]))
    
    return derived_key

def xor_decrypt(hex_encoded, key):
    encrypted_bytes = bytes.fromhex(hex_encoded)
    decrypted_message = ""
    
    for i in range(len(encrypted_bytes)):
        decrypted_message += chr(encrypted_bytes[i] ^ ord(key[i % len(key)]))
    
    return decrypted_message

def connect_and_get_flag(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        
        welcome_message = s.recv(1024).decode()
        print("Received:", welcome_message)
        
        encoded_flag = welcome_message.split("flag 1: ")[1].split("\n")[0]
        
        known_start_plaintext = 'THM{'
        known_end_plaintext = '}'

        derived_key_start = derive_key_part(encoded_flag, known_start_plaintext, 0)
        print("Derived start of the key:", derived_key_start)

        derived_key_end = derive_key_part(encoded_flag, known_end_plaintext, len(encoded_flag) // 2 - 1)
        print("Derived end of the key:", derived_key_end)

        key_length = 5
        derived_key = (derived_key_start + derived_key_end)[0:key_length]
        print("Derived key:", derived_key)

        # Decrypt the full message using the derived key
        decrypted_message = xor_decrypt(encoded_flag, derived_key)
        print("Decrypted message:", decrypted_message)

        # Send the derived key back to the server
        s.sendall(derived_key.encode() + b'\n')
        
        # Read the server response with flag 2
        response = s.recv(1024).decode()
        print("Server response:", response)

        s.sendall(derived_key.encode() + b'\n')
        response = s.recv(1024).decode()
        print("Server response:", response)

if __name__ == '__main__':
    # Define the server IP and port
    server_ip = "10.10.218.175"
    server_port = 1337

    # Connect to the server and get the flag
    connect_and_get_flag(server_ip, server_port)
