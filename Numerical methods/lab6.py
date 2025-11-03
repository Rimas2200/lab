from math import cos, pi, sin


def f(x):
    return cos(x)


a = pi / 4
b = 3*pi / 4

n = 5
h = (b - a) / n

sum_trap = 0.0
for i in range(1, n):
    xi = a + h * i
    sum_trap += f(xi)
I_trap = h * ((f(a) + f(b)) / 2 + sum_trap)
I_exact = sin(a) - sin(b)

print(f"Метод трапеции: {I_trap:.8f}")
print(f"Погрешноcть: {(I_trap - I_exact):.8f}")