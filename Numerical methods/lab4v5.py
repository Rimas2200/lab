x_values = [2.0, 2.3, 2.5, 3.0, 3.5, 3.8, 4.0]
f_values = [5.848, 6.127, 6.300, 6.694, 7.047, 7.243, 7.368]

x = 2.41


def lagrange_interpolation(x_values, f_values, x):
    n = len(x_values)
    result = 0.0

    for k in range(n):
        term = f_values[k]
        for i in range(n):
            if i != k:
                term *= (x - x_values[i]) / (x_values[i] - x_values[k])
        result += term
    return result


f_x = lagrange_interpolation(x_values, f_values, x)
print(f"f({x}) = {f_x:.5f}")