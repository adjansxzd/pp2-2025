"""
Area of regular polygon: (n * a^2) / (4*tan(pi/n)) 
where
n - number of sides
a - length of a side
"""
import math

def Polygon(n, a):
    return math.floor((n * (a**2))/(4 * math.tan(math.pi / n)))

number_of_sides = int(input("Input number of sides: "))  
length = int(input("Input the length of a side: "))

print("The area of the polygon is: ", Polygon(number_of_sides, length))