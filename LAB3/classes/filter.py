def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True
class List():
    def __init__(self, u):
        self.u = u

    def filtered(self):
        return list(filter(lambda num : is_prime(num), self.u))
    
my_list = List([1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 16, 17])
print(my_list.filtered())    