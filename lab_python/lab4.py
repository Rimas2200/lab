import math
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def length(self):
        return 0

class Vector:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def getx(self):
        return self.end.x - self.start.x

    def gety(self):
        return self.end.y - self.start.y

    def length(self):
        return math.sqrt(self.getx()**2 + self.gety()**2)

    def draw(self, ax, color='b'):
        ax.quiver(
            self.start.x,
            self.start.y,
            self.getx(),
            self.gety(),
            angles='xy',
            scale_units='xy',
            scale=1,
            color=color
        )

class Triangle:
    def __init__(self, point1, point2, point3):
        self.points = [point1, point2, point3]
        self.vectors = [
            Vector(point1, point2),
            Vector(point2, point3),
            Vector(point3, point1)
        ]

    def draw(self):
        fig, ax = plt.subplots()
        for vector in self.vectors:
            vector.draw(ax)
        ax.set_aspect('equal')
        ax.grid(True)

        point4 = Point(3.0, 3.0)
        vector1 = Vector(self.points[0], point4)
        vector2 = Vector(self.points[1], point4)
        vector1.draw(ax, color='r')
        vector2.draw(ax, color='g')

        plt.plot(point4.x, point4.y, 'bo')

        plt.show()

    def length(self):
        return sum(vector.length() for vector in self.vectors)

point1 = Point(1.0, 1.0)
point2 = Point(4.0, 1.0)
point3 = Point(2.5, 5.0)
point4 = Point(1.0, 1.0)

triangle = Triangle(point1, point2, point3)
triangle.draw()

for object in [point1, point2, point3, triangle]:
    length = object.length()
    print(f"Длина объекта: {length}")
for vector in triangle.vectors:
    length = vector.length()
    print(f"Длина объекта: {length}")