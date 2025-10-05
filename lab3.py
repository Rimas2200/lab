A = [
[2.3, 1.1, 0.23],
[-2.0, 1.3, 1.77],
[0.2, 2.1, 2.5]
]
b = [3.3, -0.7, 4.4]

def jacobi(A, b, eps=0.001, max_iter=1000):
    n = len(A)
    x_old = [0.0] * n
    x_new = [0.0] * n

    for k in range(max_iter):
        for i in range(n):
            s = 0
            for j in range(n):
                if j != i:
                    s += A[i][j] * x_old[j]
            x_new[i] = (b[i] - s) / A[i][i]

        diff = max(abs(x_new[i] - x_old[i]) for i in range(n))
        if diff < eps:
            return x_new, k+1

        x_old = x_new.copy()
    return x_new, max_iter


solution, steps = jacobi(A, b)
print("Решение:", solution)
print("Число итераций:", steps)