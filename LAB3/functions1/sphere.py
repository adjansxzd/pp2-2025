import math 

def vol(radius):
    return 4 / 3 * math.pi * (radius ** 3)
r = float(input("Enter the radius: "))
print(vol(r))
