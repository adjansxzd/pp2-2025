# proverka na prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def filter_prime(numbers):
    return [num for num in numbers if is_prime(num)]

numbers_str = input("Enter numbers separated by space:" )
numbers_list = list(map(int, numbers_str.split())) 
filtered_numbers = filter_prime(numbers_list)
print(filtered_numbers)   