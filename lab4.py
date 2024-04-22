from math import atan2, cos, sin
from abc import ABC, abstractmethod
class GeomObject(ABC):
    @abstractmethod
    def draw(self):
        pass

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

    def draw(self):
        pass


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
        angle_radians = atan2(self.y, self.x)
        arrow_length = 5
        arrow_angle_degrees = 90

        end_x = self.start.getx() + self.x
        end_y = self.start.gety() + self.y

        arrow_tip_x = end_x - arrow_length * cos(angle_radians)
        arrow_tip_y = end_y - arrow_length * sin(angle_radians)

        arrow_side1_x = arrow_tip_x + arrow_length * cos((angle_radians + arrow_angle_degrees * 3.14159265359 / 180))
        arrow_side1_y = arrow_tip_y + arrow_length * sin((angle_radians + arrow_angle_degrees * 3.14159265359 / 180))
        arrow_side2_x = arrow_tip_x + arrow_length * cos((angle_radians - arrow_angle_degrees * 3.14159265359 / 180))
        arrow_side2_y = arrow_tip_y + arrow_length * sin((angle_radians - arrow_angle_degrees * 3.14159265359 / 180))

    def transfer(self, dx, dy):
        self.start.setx(self.start.getx() + dx)
        self.start.sety(self.start.gety() + dy)

    def rotate(self, angle_degrees):
        angle_radians = angle_degrees * 3.14159265359 / 180

        new_x = self.x * cos(angle_radians) - self.y * sin(angle_radians)
        new_y = self.x * sin(angle_radians) + self.y * cos(angle_radians)

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