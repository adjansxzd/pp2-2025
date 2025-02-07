def histogram(our_list):
    for num in our_list:
        print('*' * num)

numbers = list(map(int, input("Enter numbers sep by space: ").split()))
histogram(numbers)        