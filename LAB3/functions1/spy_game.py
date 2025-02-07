# print(spy_game([1,2,4,0,0,7,5])) --> True
# print(spy_game([1,0,2,4,0,5,7]))--> True
# print(spy_game([1,7,2,0,4,5,0])) --> False

def spy_game(nums):
    shablon = [0, 0, 7]
    index = 0
    for num in nums:
        if num == shablon[index]:
            index += 1
            if index == len(shablon):
                return True
    return False        
