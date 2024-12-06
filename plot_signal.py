import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal import correlate

# Cargar el archivo de audio
# Cambia "sonido.wav" por el archivo real que estás utilizando
sample_rate, signal = read("prueba.wav")

# Seleccionar un segmento de 30 ms (ajusta según la frecuencia de muestreo)
segment_duration_ms = 30
samples_per_segment = int(sample_rate * segment_duration_ms / 1000)
segment = signal[:samples_per_segment]  # Tomamos el inicio como ejemplo

time_axis = np.linspace(0, segment_duration_ms, samples_per_segment)

# Calcular la autocorrelación del segmento
autocorrelation = correlate(segment, segment, mode='full')
autocorrelation = autocorrelation[autocorrelation.size // 2:]

# Encontrar el primer máximo secundario en la autocorrelación
d = np.diff(autocorrelation)
start = np.where(d > 0)[0][0]  # Encuentra el primer punto donde la derivada es positiva
peak = np.argmax(autocorrelation[start:]) + start

# Crear subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Plot de la señal temporal
axs[0].plot(time_axis, segment)
axs[0].set_xlabel("Tiempo (ms)")
axs[0].set_ylabel("Amplitud")
axs[0].set_title("Señal de 30 ms")

# Plot de la autocorrelación
lags = np.arange(0, len(autocorrelation))
axs[1].plot(lags, autocorrelation)
axs[1].plot(peak, autocorrelation[peak], 'ro')  # Marcar el primer máximo secundario
axs[1].set_xlabel("Lags")
axs[1].set_ylabel("Autocorrelación")
axs[1].set_title("Autocorrelación de la señal")

plt.tight_layout()
plt.show()
