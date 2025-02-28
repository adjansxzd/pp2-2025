import re

def find_pattern(str):
    pattern = r'ab*'
    if re.match(pattern, str):
        return True
    else:
        return False
    
str = str(input())
print(find_pattern(str))

