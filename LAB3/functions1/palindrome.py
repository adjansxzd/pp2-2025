def is_palindrome(word):
    reversed_word = word[::-1]
    if(reversed_word == word):
        print("Palindrome")
    else:
        print("Not palindrome")    
user_input = input()
is_palindrome(user_input)        
              