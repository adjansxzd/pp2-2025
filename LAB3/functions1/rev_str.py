def reverse(s):
    reversed_st = " ".join(reversed(s.split()))
    print(reversed_st)

s = input("Enter text: ")
reverse(s)