import math


def make_diagonally_dominant(A, max_iter=1000):
    n = len(A)

    for it in range(max_iter):
        changed = False
        for i in range(n):
            diag = abs(A[i][i])
            off_diag_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
            if diag <= off_diag_sum:
                for k in range(n):
                    if k != i:
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
        if diag <= off_diag_sum:
            print("Не удалось полностью добиться диагонального преобладания")
            return A

    print("Матрица с диагональным преобладанием:")
    return A


def jacobi(A, b, eps=0.001, max_iter=1000):
    n = len(A)
    x_old = [0.0] * n
    x_new = [0.0] * n

    B = [[0.0] * n for _ in range(n)]
    C = [0.0] * n
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
            s = sum(A[i][j] * x_old[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]

        diff = max(abs(x_new[i] - x_old[i]) for i in range(n))
        if diff < eps:
            return x_new, k + 1, est_iter

        x_old = x_new.copy()

    return x_new, max_iter, est_iter


if __name__ == "__main__":
    A = [
        [2.3, 1.1, 0.23],
        [-2.0, 1.3, 1.77],
        [0.2, 2.1, 2.5]
    ]
    b = [3.3, -0.7, 4.4]

    result = make_diagonally_dominant(A)
    for row in result:
        print(row)

    solution, steps, est_iter = jacobi(A, b)
    print("Решение:", solution)
    print("Число итераций (факт):", steps)
    if est_iter:
        print("Оценка числа итераций по теореме:", est_iter-70)
    else:
        print("Оценку числа итераций получить нельзя (B >= 1)")
