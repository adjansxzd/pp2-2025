def Trapezoid(a, b, h):
    area = (a + b)/ 2 * h
    return area

base1 = int(input("Base, first value: "))
base2 = int(input("Base, second value: "))
height = int(input("Height: "))

print("Expected Output: ", Trapezoid(base1, base2, height))