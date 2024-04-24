import random
import math
import matplotlib.pyplot as plt

t0 = (1, 0)
t1 = (1.707, 0.707)
t2 = (1, 1)
t3 = (0.293, 0.707)

points = []

p0 = random.choice([t0, t1, t2])


for _ in range(50000):
    # случайная точка ti из t0, t1, t2
    ti = random.choice([t0, t1, t2, ])
    # середина отрезка p0ti
    p1 = ((p0[0] + ti[0]) / 2, (p0[1] + ti[1]) / 2)
    points.append(p1)
    p0 = p1

x_values, y_values = zip(*points)

plt.scatter(x_values, y_values, s=1)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('lab1')
plt.show()