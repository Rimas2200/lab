x_nodes = [0, 1/5, 1/4, 1/3, 1/2, 1]
n_nodes = len(x_nodes)


def f(x):
    return x**3 - x**4


def L(k, x):
    result = 1.0
    for i in range(n_nodes):
        if i != k:
            result *= (x - x_nodes[i]) / (x_nodes[k] - x_nodes[i])
    return result


def integrate_rect(f, a, b, n_parts = 100):
    h = (b - a) /n_parts
    total = 0.0
    for i in range(n_parts):
        xi = a + h * (i + 0.5)
        total += f(xi)
    return h * total


a, b = 0.1, 1.0
A = []

for k in range(n_nodes):
    def Lk(x, k=k):
        return L(k, x)
    Ak = integrate_rect(Lk, a, b, 100)
    A.append(Ak)

I_approx = 0.0
for k in range(n_nodes):
    I_approx += A[k] * f(x_nodes[k])

print(I_approx)