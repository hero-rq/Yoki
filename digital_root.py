"""
Write a program that calculates the digital root of a given number. 
The digital root is the single-digit value obtained by an iterative process of summing digits, 
on each iteration using the result from the previous iteration to compute a digit sum. 
The process continues until a single-digit number is obtained.

For example, the digital root of 456 is calculated as follows:

4 + 5 + 6 = 15
1 + 5 = 6
So, the digital root of 456 is 6.
"""

def is_less_than_tenth(num):
    return isinstance(num, int) and 0 <= num < 10

x = int(input('Please give me any number: '))
result = 0

while True:
    leng = len(str(x))
    for i in range(1, leng + 1):
        temp = (x % (10 ** (leng - i + 1))) // (10 ** (leng - i))
        result += temp
        x -= temp * (10 ** (leng - i))

    if is_less_than_tenth(result):
        break

    x = result
    result = 0

print('Digital root:', result)
