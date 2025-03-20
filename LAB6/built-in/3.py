text = str(input())
revText = ''.join(reversed(text))
if(revText == text):
    print("Palindrome")
else:
    print("Not palindrome")