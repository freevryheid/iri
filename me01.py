from numpy import linspace, sin, pi
from piri import getpi

fs = 13  # sampling frequncy (per meter)
A = 0.001  # m
w = 3  # m
base = 0.25

x = linspace(0, 60, fs*60)
y = A*sin(2*pi*x/w)
p = y.copy()

p, n, r = getpi(p, 1/fs, base)
print(r*1000)

# plt.plot(x, y)
# plt.show()
