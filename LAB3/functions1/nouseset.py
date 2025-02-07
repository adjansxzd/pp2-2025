def unique_elements(our_list):
    unique_list = []
    for num in  our_list:
        if num not in unique_list:
            unique_list.append(num)
    return unique_list

numbers = list(map(int, input("Enter some numbers sep by space: ").split()))        
print(unique_elements(numbers))