import math
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(f"Coordinates: ({self.x}, {self.y})")

    def move(self, changed_x, changed_y):
        self.x += changed_x
        self.y += changed_y
        print(f"Coordinates: ({self.x}, {self.y})")

    def dist(self, other_point):
        distance = math.sqrt((other_point.x - self.x) ** 2 + (other_point.y - self.y) ** 2)
        return int(distance)
p1 = Point(6, 8)
p2 = Point(3, 5)
p1.show()
p2.move(8, 2)
print(f"Distance between two points: {p1.dist(p2)}")
