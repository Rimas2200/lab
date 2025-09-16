def abs_x(x):
    return -x if x < 0 else x

def gauss(a, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs_x(a[k][i]) > abs_x(a[max_row][i]):
                max_row = k

        a[i], a[max_row] = a[max_row], a[i]
        b[i], b[max_row] = b[max_row], b[i]

        div = a[i][i]
        for j in range(i, n):
            a[i][j] /= div
        b[i] /= div

        for k in range(i+1, n):
            factor = a[k][i]
            for j in range(i, n):
                a[k][j] -= factor * a[i][j]
            b[k] -= factor * b[i]

    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = b[i]
        for j in range(i+1, n):
            x[i] -= a[i][j] * x[j]
    return x

def determinant(matrix):
    n = len(matrix)
    det = 1
    sign = 1

    a = [row[:] for row in matrix]

    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs_x(a[k][i]) > abs_x(a[max_row][i]):
                max_row = k
        if abs_x(a[max_row][i]) < 1e-12:
            return 0

        if max_row != i:
            a[i], a[max_row] = a[max_row], a[i]
            sign *= -1

        pivot = a[i][i]
        det *= pivot

        for k in range(i+1, n):
            factor = a[k][i] / pivot
            for j in range(i, n):
                a[k][j] -= factor * a[i][j]

    return det * sign


def cholesky_decomposition(a):
    n = len(a)
    L = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                L[i][j] = (a[i][i] - s) ** 0.5
            else:
                L[i][j] = (a[i][j] - s) / L[j][j]
    return L

def forward_substitution(L, b):
    n = len(b)
    y = [0.0] * n
    for i in range(n):
        s = sum(L[i][j] * y[j] for j in range(i))
        y[i] = (b[i] - s) / L[i][i]
    return y

def backward_substitution(L, y):
    n = len(y)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(L[j][i] * x[j] for j in range(i + 1, n))
        x[i] = (y[i] - s) / L[i][i]
    return x

def solve_cholesky(a, b):
    L = cholesky_decomposition(a)
    y = forward_substitution(L, b)
    x = backward_substitution(L, y)
    return x

if __name__ == "__main__":
    A = [
        [5.73, 3.29, 1.94, -2.21],
        [-9.55, 0.45, 7.94, -2.27],
        [-8.20, 5.63, -8.92, -9.34],
        [-3.78, 0.97, -7.28, 2.39]
    ]
    B = [-7.21, 7.41, -2.95, -6.09]

    solution = gauss(A, B)
    for i, val in enumerate(solution, start=1):
        print(f"x{i} = {val:.6f}")

    A = [
        [0.2, -0.11, -0.63, -0.14],
        [0.56, 0.04, -0.82, 0.29],
        [0.66, -0.23, -0.22, -0.71],
        [0.01, 0.47, 0.58, 0.28]
    ]
    print("det(A) =", determinant(A))

    A = [
            [1.02, 6.05, -3.73, -7.23],
            [6.05, 4.36, -1.54, -1.09],
            [-3.73, -1.54, 0.1, -6.95],
            [-7.23, -1.09, -6.95, 5.11]
        ]
    b = [-6.59, -2.38, 1.62, 6.18]

    solution = solve_cholesky(A, b)
    print("Решение:", solution)