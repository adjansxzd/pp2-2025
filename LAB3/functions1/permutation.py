from itertools import permutations

def perms(s):
    for p in permutations(s):
        print("".join(p))

user_input = input("Enter something: ")
perms(user_input)