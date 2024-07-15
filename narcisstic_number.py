"""
Problem Statement:
Write a program that checks if a given number is an Armstrong number. 
An Armstrong number (also known as a narcissistic number) is a number that 
is equal to the sum of its own digits each raised to the power of the number of digits.
"""

def is_armstrong_number(num):
    num_digits = len(str(num))
    
    sum_of_powers = 0
    """
    leng = len(str(x))
    for i in range(1, leng + 1):
        temp = (x % (10 ** (leng - i + 1))) // (10 ** (leng - i))
        result += temp
        x -= temp * (10 ** (leng - i))
    """
    temp = num
    # sum_of_powers += digit ** num_digits 
    for i in range(1, num_digits+1):
        digit = (num % (10 ** (num_digits - i + 1))) // (10 ** (num_digits - i))
        sum_of_powers += digit ** num_digits
        temp -= digit * (10 ** (num_digits - i))
    
    return sum_of_powers == num

number = int(input("Enter a number: "))

if is_armstrong_number(number):
    print(f"{number} is an Armstrong number.")
else:
    print(f"{number} is not an Armstrong number.")
