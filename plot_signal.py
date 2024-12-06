import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

# Cargar el archivo de audio
audio_file = 'prueba.wav'
y, sr = librosa.load(audio_file, sr=None)

# Extraer un segmento de la señal (por ejemplo, de 0.5s a 0.53s)
start_sample = int(0.5 * sr)
end_sample = int(0.53 * sr)
segment = y[start_sample:end_sample]

# Calcular la autocorrelación
autocorr = np.correlate(segment, segment, mode='full')
autocorr = autocorr[len(segment)-1:]  # Solo tomamos la parte positiva
lags = np.arange(0, len(autocorr))

# Visualizar la autocorrelación
plt.plot(lags, autocorr)
plt.title("Autocorrelación")
plt.xlabel("Retraso (muestras)")
plt.ylabel("Amplitud")
plt.grid(True)
plt.show()
