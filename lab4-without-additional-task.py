from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import math
class GeomObject(ABC):
    @abstractmethod
    def draw(self, ax):
        pass
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
        plt.show()


class Point(GeomObject):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def setx(self, x):
        self.x = x

    def sety(self, y):
        self.y = y

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def draw(self, ax):
        ax.plot(self.x, self.y, "ro", label="Point")


class Vector(GeomObject):
    def __init__(self, start, x=0.0, y=0.0):
        self.start = start
        self.x = x
        self.y = y

    def set_start(self, start):
        self.start = start

    def setx(self, x):
        self.x = x

    def sety(self, y):
        self.y = y

    def get_start(self):
        return self.start

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def draw(self):
        angle_radians = math.atan2(self.y, self.x)
        arrow_length = 5
        arrow_angle_degrees = 90

        end_x = self.start.getx() + self.x
        end_y = self.start.gety() + self.y

        arrow_tip_x = end_x - arrow_length * math.cos(angle_radians)
        arrow_tip_y = end_y - arrow_length * math.sin(angle_radians)

        arrow_side1_x = arrow_tip_x + arrow_length * math.cos((angle_radians + arrow_angle_degrees * math.pi / 180))
        arrow_side1_y = arrow_tip_y + arrow_length * math.sin((angle_radians + arrow_angle_degrees * math.pi / 180))
        arrow_side2_x = arrow_tip_x + arrow_length * math.cos((angle_radians - arrow_angle_degrees * math.pi / 180))
        arrow_side2_y = arrow_tip_y + arrow_length * math.sin((angle_radians - arrow_angle_degrees * math.pi / 180))

        # Ваш код отрисовки вектора

    def transfer(self, dx, dy):
        self.start.setx(self.start.getx() + dx)
        self.start.sety(self.start.gety() + dy)

    def rotate(self, angle_degrees):
        angle_radians = angle_degrees * math.pi / 180

        new_x = self.x * math.cos(angle_radians) - self.y * math.sin(angle_radians)
        new_y = self.x * math.sin(angle_radians) + self.y * math.cos(angle_radians)

        self.x = new_x
        self.y = new_y

    def __mul__(self, value):
        end_x = self.x - self.start.getx()
        end_y = self.y - self.start.gety()
        new_end_x = self.start.getx() + end_x * value
        new_end_y = self.start.gety() + end_y * value
        return Vector(self.start, new_end_x, new_end_y)

    def __add__(self, other_vect):
        x2 = other_vect.getx() - other_vect.get_start().getx()
        y2 = other_vect.gety() - other_vect.get_start().gety()

        return Vector(self.start, self.x + x2, self.y + y2)
    def draw(self, ax):
        ax.quiver(
            self.start.getx(),
            self.start.gety(),
            self.x,
            self.y,
            angles="xy",
            scale_units="xy",
            scale=1,
            color="b",
            label="Vector"
        )

start_point = Point(1.0, 1.0)
vector = Vector(start_point, 2.0, 3.0)

fig, ax = plt.subplots()

vector.draw(ax)
start_point.draw(ax)

ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect("equal")
ax.grid(True)
ax.legend()

plt.show()