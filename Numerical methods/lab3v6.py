import math

def make_diagonally_dominant(A, tol=1e-8, max_iter=100):
    n = len(A)

    for it in range(max_iter):
        changed = False
        for i in range(n):
            diag = abs(A[i][i])
            off_diag_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
            if diag <= off_diag_sum + tol:
                for k in range(n):
                    if k != i and abs(A[k][k]) > tol:
                        factor = A[i][k] / A[k][k]
                        if factor != 0:
                            for j in range(n):
                                A[i][j] -= factor * A[k][j]
                            changed = True
        if not changed:
            break

    for i in range(n):
        diag = abs(A[i][i])
        off_diag_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag <= off_diag_sum + tol:
            print("Не удалось полностью добиться диагонального преобладания.")
            return A

    print("Матрица с диагональным преобладанием:")
    return A


def JACOBI(A, b, eps=0.001, max_iter=1000):
    n = len(A)
    Xold = [0.0] * n
    Xnew = [0.0] * n

    B = [[0.0]*n for _ in range(n)]
    C = [0.0]*n
    for i in range(n):
        for j in range(n):
            if i != j:
                B[i][j] = -A[i][j] / A[i][i]
        C[i] = b[i] / A[i][i]

    norm_B = max(sum(abs(B[i][j]) for j in range(n)) for i in range(n))
    norm_C = max(abs(ci) for ci in C)

    est_iter = None
    if norm_B < 1:
        rhs = eps * (1 - norm_B) / norm_C
        if rhs > 0:
            est_iter = math.ceil(math.log(rhs) / math.log(norm_B) - 1)

    for k in range(max_iter):
        for i in range(n):
            s = 0
            for j in range(n):
                if j != i:
                    s += A[i][j] * Xold[j]
            Xnew[i] = (b[i] - s) / A[i][i]

        diff = max(abs(Xnew[i] - Xold[i]) for i in range(n))
        if diff < eps:
            return Xnew, k+1, est_iter

        Xold = Xnew.copy()

    return Xnew, max_iter, est_iter

A = [
    [-2.4, 1.0, 1.2],
    [0.93, -2.5, 5.8],
    [1.2, 1.3, 1.4]
]
b = [5.1, 11.1, 1.5]

result = make_diagonally_dominant(A)
for row in result:
    print(row)

solution, steps, est_iter = JACOBI(A, b)
print("Решение:", solution)
print("Число итераций (факт):", steps)
if est_iter:
    print("Оценка числа итераций по теореме:", est_iter)
else:
    print("Оценку числа итераций получить нельзя ( >= 1)")
