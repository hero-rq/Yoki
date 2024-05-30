import random
import string

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def randomword2(length):
    letters2 = string.ascii_uppercase
    return ''.join(random.choice(letters2) for i in range(length))

def generate_secure_password(length):
    if length < 12 or length > 16:
        print("Sorry, the length should be between 12 and 16.")
        return None
    
    random_can1 = "!@#$%^&*()-_=+[]{}|;:'"
    random_can2 = ",.<>?/~"
    random_can = random_can1 + random_can2

    part1 = randomword(1)
    part2 = randomword2(1)
    part3 = random.choice(string.digits)
    part4 = random.choice(random_can)

    remaining_length = length - 4
    all_characters = string.ascii_letters + string.digits + random_can
    remaining_part = ''.join(random.choice(all_characters) for i in range(remaining_length))

    basic = part1 + part2 + part3 + part4 + remaining_part
    password_list = list(basic)
    random.shuffle(password_list)
    output = ''.join(password_list)
    
    return output

print("these are the examples")
print(generate_secure_password(12))
print(generate_secure_password(16))

x = int(input("how many lengths of password do you want to generate ? : "))
print(generate_secure_password(x))
