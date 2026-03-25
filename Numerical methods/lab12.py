from math import *
import matplotlib.pyplot as plt

d = 0.9
N = 20
h = 1.0 / N

def p(x): return -(x + d) ** 2
def q(x): return -2.0 / (x + d) ** 2
def f(x): return d

# точное решение
def exact(x): return d / (x + d)


def progonka(A, B, C, F):
    n = len(B)
    alpha = [0.0] * n
    beta = [0.0] * n
    y = [0.0] * n

    alpha[0] = -C[0] / B[0]
    beta[0] = F[0] / B[0]

    for i in range(1, n):
        den = B[i] + A[i] * alpha[i - 1]
        alpha[i] = 0 if i == n - 1 else -C[i] / den
        beta[i] = (F[i] - A[i] * beta[i - 1]) / den

    y[n - 1] = beta[n - 1]
    for i in range(n - 2, -1, -1):
        y[i] = alpha[i] * y[i + 1] + beta[i]

    return y


def solve1():
    x = [i * h for i in range(N + 1)]
    A = [0.0] * (N + 1)
    B = [0.0] * (N + 1)
    C = [0.0] * (N + 1)
    F = [0.0] * (N + 1)

    B[0] = 1 + 1/h
    C[0] = -1/h
    F[0] = (d + 1) / d

    for i in range(1, N):
        xi = x[i]
        A[i] = 1 / h**2
        B[i] = -2 / h**2 - p(xi) / h + q(xi)
        C[i] = 1 / h**2 + p(xi) / h
        F[i] = f(xi)

    B[N] = 1
    F[N] = d / (d + 1)

    return x, progonka(A, B, C, F)


def solve2():
    x = [i * h for i in range(N + 1)]
    A = [0.0] * (N + 1)
    B = [0.0] * (N + 1)
    C = [0.0] * (N + 1)
    F = [0.0] * (N + 1)

    x0 = 0.0
    B[0] = -2/h**2 - 2/h + p(x0) + q(x0)
    C[0] = 2/h**2
    F[0] = f(x0) - 2*((d+1)/d)/h + p(x0)*((d+1)/d)

    for i in range(1, N):
        xi = x[i]
        A[i] = 1 / h**2 - p(xi) / (2*h)
        B[i] = -2 / h**2 + q(xi)
        C[i] = 1 / h**2 + p(xi) / (2*h)
        F[i] = f(xi)

    B[N] = 1
    F[N] = d / (d + 1)

    return x, progonka(A, B, C, F)


x, y1 = solve1()
x, y2 = solve2()
ye = [exact(xi) for xi in x]

err1 = max(abs(y1[i] - ye[i]) for i in range(N + 1))
err2 = max(abs(y2[i] - ye[i]) for i in range(N + 1))

print("   x        y1           y2         exact")
for i in range(N + 1):
    print(f"{x[i]:.2f}   {y1[i]:.6f}   {y2[i]:.6f}   {ye[i]:.6f}")

print("\nМакс. ошибка 1 порядка =", err1)
print("Макс. ошибка 2 порядка =", err2)

plt.plot(x, ye, label="точное")
plt.plot(x, y1, 'o-', label="1 порядок")
plt.plot(x, y2, 's-', label="2 порядок")
plt.grid()
plt.legend()
plt.show()