import random
def guess_the_number():
    random_number = random.randint(1, 20)
    print("Hello! What is your name?")
    name = input()
    print(f"Well, " + name + ", I am thinking of a number between 1 and 20.")
    print("Take a guess.")
    attempts = 0
    while True:
        user_number = int(input())
        attempts += 1
        if(user_number < random_number):
            print("Your guess is too low. \nTake a guess.")
        elif(user_number > random_number):
            print("Your guess is too high. \nTake a guess.")
        else:
            print(f"Good job, {name}! You guesses my number in {attempts} guesses! ")
            break
guess_the_number()

