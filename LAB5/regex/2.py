import re

def find_pattern(string):
    pattern = r"ab{2,3}"
    if re.match(pattern, string):
        return True
    else:
        return False

string = str(input())
print(find_pattern(string))    
