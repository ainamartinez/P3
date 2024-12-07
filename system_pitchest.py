import numpy as np
import matplotlib.pyplot as plt

# Load data from txt files
prueba = {
    'f0': np.loadtxt('/home/aina/PAV/P3/prueba.f0'),
    'f0ref': np.loadtxt('/home/aina/PAV/P3/prueba.f0ref')
}

plt.figure(figsize=(10, 5))

plt.plot(prueba['f0ref'], '*', label='prueba.f0ref', color='green', markersize=8, markeredgewidth=1)
plt.plot(prueba['f0'], 'o', label='prueba.f0', color='lightblue', markersize=5, markeredgewidth=1)
plt.grid(True)
plt.xlabel('Index')
plt.ylabel('Values')
plt.title('Plot of f0 and f0ref')
plt.legend()
plt.show()
