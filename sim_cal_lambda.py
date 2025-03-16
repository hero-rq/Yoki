"""
Problem:
Create a simple calculator using a dictionary and lambda functions in Python. 
The calculator should support basic arithmetic operations: addition, subtraction, 
multiplication, and division. It should ask for two numbers and an operation as input and then return the result.
"""
# Calculator with dictionary and lambda

calculator = {
    'add': lambda x, y: x + y,
    'sub': lambda x, y: x - y,
    'mul': lambda x, y: x * y,
    'div': lambda x, y: x / y 
}

num1 = 10
num2 = 5
operation = 'add'  
result = calculator[operation](num1, num2)

print(f"The result is: {result}")
