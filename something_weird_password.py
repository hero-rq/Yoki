import re

def has_mixed_case(tested_string):
    return bool(re.search(r"(?=.*[a-z])(?=.*[A-Z])", tested_string))

def password_checker(password):
    result = ""
    if len(password) < 8 or password.isalpha():
        result = 'weak'
    elif not password.isalpha() and len(password) < 12:
        result = 'medium'
    elif not password.isalpha() and len(password) >= 12 and has_mixed_case(password):
        result = 'strong'
    else:
        result = 'something weird'
    
    return result

print(password_checker("panda"))           # weak
print(password_checker("pandapanda!@P"))   # strong
print(password_checker("pppppppp!ppppppp"))
