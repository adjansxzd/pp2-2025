class Shape():
    def __init__(self, length, width):
        self.length = length
        self.width = width

class Rectangle(Shape):
    def area(self):
        print(self.length * self.width)      

u = int(input("Enter length: "))
p = int(input("Enter width: "))
p1 = Rectangle(u, p)
p1.area()
