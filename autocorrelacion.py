import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import os

señal, fm = sf.read('prueba.wav') 
t = np.arange(0, len(señal)) / fm 
""" 
plt.figure("Signal Plot")
plt.xlabel('t[s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.plot(t, señal)
plt.show() """

t_ini = 0.744
t_fin = 0.774

n_ini = int(t_ini * fm);
n_fin = int(t_fin * fm);

l = int((fm * 30)/1e3)  #longitud de la ventana de 30ms

plt.figure("30ms Plot + autocorrelation")

plt.subplot(1, 2, 1)
plt.plot(t[n_ini:n_fin], señal[n_ini:n_fin])
plt.xlabel('t[s]')
plt.ylabel('Amplitud')
plt.title('30ms Signal')
plt.grid(True)

def autocorrelacion(vector):
  autocorrelation = np.correlate(vector, vector, mode = 'full')
  return autocorrelation[autocorrelation.size//2:]

autocorr = autocorrelacion(señal[n_ini:n_fin])
plt.subplot(1, 2, 2)
plt.plot(t[:l]*1000,autocorr)
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.title('Autocorrelation')
plt.grid(True)

plt.tight_layout()
plt.show()

rmax_index = np.argmax(autocorr[1:]) + 1
rmax = autocorr[rmax_index] / autocorr[0]
r1norm = autocorr[1] / autocorr[0]


print(f"r1norm: {r1norm}")
print(f"rmax: {rmax}")