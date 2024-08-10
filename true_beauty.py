import matplotlib.pyplot as plt
import numpy as np

def f(x):
    return 2 * x / (x**2 + 1)

x = np.linspace(-10, 10, 400)

y = f(x)

plt.figure(figsize=(8, 6))
plt.plot(x, y, label=r'$f(x) = \frac{2x}{x^2 + 1}$')
plt.title('Graph of f(x)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.grid(True)
plt.legend()
plt.show()
