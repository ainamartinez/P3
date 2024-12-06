% Leer el archivo de audio
[audio, fs] = audioread('prueba.wav'); % 'archivo.wav' es tu archivo de audio

% Definir el rango de tiempo (en segundos)
start_time = 0.74420; % Inicio del segmento
end_time = start_time + 0.03; % Fin del segmento (30 ms después)

% Convertir tiempo a índices de muestra
start_sample = round(start_time * fs); % Muestra inicial
end_sample = round(end_time * fs);     % Muestra final

% Extraer el segmento del audio
segment = audio(start_sample:end_sample);

% Visualizar el segmento de audio
time_segment = (start_sample:end_sample) / fs; % Convertir a tiempo en segundos

% Segmento extraído previamente
% Supongamos que tienes el segmento "segment" y sus índices "n_segment"
n_segment = 0:length(segment)-1; % Índices del segmento

% Invertir el segmento en el tiempo
h = flip(segment); % Inversión de la señal
n_h = -fliplr(n_segment); % Índices invertidos

% Calcular la autocorrelación usando conv_digital
[y, ny] = conv_digital(segment, n_segment, h, n_h);

% Normalizar la autocorrelación (opcional)
y = y / max(abs(y));

%Gráfica del segmento y la autocorrelación

figure;

% Subplot 1: Segmento
subplot(1, 2, 1); % 1 fila, 2 columnas, posición 1
plot((0:length(segment)-1)/fs, segment, 'b'); % Tiempo en segundos
xlabel('Tiempo (s)');
ylabel('Amplitud');
title('Segmento de la señal');
grid on;

% Subplot 2: Autocorrelación (parte positiva)
subplot(1, 2, 2); % 1 fila, 2 columnas, posición 2
positive_idx = ny >= 0 & ny <= 600; % Filtrar índices entre 0 y 600
plot(ny(positive_idx), y(positive_idx), 'k', 'LineWidth', 1.5);
xlabel('Retraso (muestras)');
ylabel('Amplitud de la autocorrelación');
title('Autocorrelación del segmento');
grid on;

% Ajustar los subplots para que se vean bien
sgtitle('Segmento y su Autocorrelación')