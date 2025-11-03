x = [0.20, 0.24, 0.27, 0.30, 0.32, 0.38]
f = [1.2214, 1.2712, 1.3100, 1.3499, 1.3771, 1.4623]
alpha = 2.5699
beta = 3.3378
x_calc = 0.25

n = len(x) - 1
h = [x[i+1] - x[i] for i in range(n)]

a = [0]*(n+1)
b = [0]*(n+1)
c = [0]*(n+1)
d = [0]*(n+1)
r = [0]*(n+1)

for i in range(2, n): #ai * Mi-1 + bi * Mi + ci * Mi+1 = ri
    a[i] = h[i-1]
    b[i] = 2*(h[i-1] + h[i])
    c[i] = h[i]
    r[i] = 6*((f[i+1]-f[i])/h[i] - (f[i]-f[i-1])/h[i-1])

b[1] = 2*h[0]
c[1] = h[0]
r[1] = 6*((f[1]-f[0])/h[0] - alpha/(2*h[0]))

a[n-1] = h[n-2]
b[n-1] = 2*h[n-2]
r[n-1] = 6*(beta/(2*h[n-2]) - (f[n]-f[n-1])/h[n-2])

p = [0]*(n+1)
q = [0]*(n+1)
for i in range(1, n):
    denom = b[i] - a[i]*p[i-1]
    p[i] = c[i]/denom
    q[i] = (r[i] - a[i]*q[i-1])/denom
    # Mi = pi * Mi+1 + qi

M = [0]*(n+1)
M[n-1] = q[n-1]

for i in range(n-2, 0, -1):
    M[i] = q[i] - p[i]*M[i+1]

M[0] = alpha - 2*M[1]
M[n] = (beta - M[n-1]) / 0.3

a_coef = [f[i] for i in range(n)]
b_coef = [0]*n
d_coef = [0]*n
for i in range(n):
    d_coef[i] = (M[i+1] - M[i]) / h[i]
    b_coef[i] = (f[i+1] - f[i])/h[i] - (h[i]/6)*(2*M[i] + M[i+1])

for i in range(n):
    if x[i] <= x_calc <= x[i+1]:
        xi, fi = x[i], f[i]
        hi = h[i]
        Mi, Mi1 = M[i], M[i+1]
        bi, di = b_coef[i], d_coef[i]
        break

dx = x_calc - xi
S = fi + bi*dx + (Mi/2)*dx**2 + (di/6)*dx**3

print("f(%.2f) = %.6f" % (x_calc, S))
