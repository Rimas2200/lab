def f(x):
    return x**4 - 20*x**3 + 101*x**2 - 20*x + 1

def df(x):
    return 4*x**3 - 60*x**2 + 202*x - 20

def isolate_roots(a, b, step=0.1):
    res = []
    x = a
    while x < b:
        if f(x) * f(x + step) < 0:
            res.append((x, x + step))
        x += step
    return res

def bisection(a, b, eps=0.1):
    k = 0
    while (b - a) > eps:
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
        k += 1
    return (a + b) / 2, k

def newton(x0, eps=0.0001, max_iter=100):
    k = 0
    while k < max_iter:
        d = df(x0)
        if d == 0:
            return None, k
        x1 = x0 - f(x0) / d
        if abs(x1 - x0) < eps:
            return x1, k+1
        x0 = x1
        k += 1
    return x0, k
# xk+1 = xk - f(xk)/df(xk)
# |xK+1 - xK| < eps

def newton_multiple(x0, p=3, eps=0.0001, max_iter=100):
    k = 0
    while k < max_iter:
        d = df(x0)
        if d == 0:
            return None, k
        x1 = x0 - p * f(x0) / d
        if abs(x1 - x0) < eps:
            return x1, k+1
        x0 = x1
        k += 1
    return x0, k
# xk+1 = xk - p * f(xk)/df(xk)
# |xK+1 - xK| < eps

intervals = isolate_roots(-1, 1)
print("Отделение корней:", intervals)

roots = []
for a, b in intervals:
    r, it = bisection(a, b)
    roots.append(r)
    print("Бисекция:", (a, b), "корень =", r)

# |xk-x*| <= q^2^k*|x0-x*|
# |xk-x*| < eps
print()
for r0 in roots:
    x1, k1 = newton(r0)
    x2, k2 = newton_multiple(r0)
    print("Старт =", r0)
    print("Ньютон p=1:", x1, "итераций =", k1)
    print("Ньютон p=2:", x2, "итераций =", k2)
    print(f"f(x1) = {f(x1):.8f}")
    print(f"f(x2) = {f(x2):.8f}")