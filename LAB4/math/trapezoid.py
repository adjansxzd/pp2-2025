def trapezoid(a, b, h):
    area = (a + b) / 2 * h
    return area

height = int(input("Height: "))
base1 = int(input("Base, first value:"))
base2 = int(input("Base, second value: "))
print("Expected output: ", trapezoid(base1, base2, height))