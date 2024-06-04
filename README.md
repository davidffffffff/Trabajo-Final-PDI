El algoritmo presentado está diseñado para detectar microsueños en tiempo real en conductores con el objetivo de mitigar accidentes viales. A continuación se presenta una descripción breve de su funcionamiento:

Inicialización del Sistema:

Importa librerías necesarias: cv2 para procesamiento de video, mediapipe para detección de malla facial, math para cálculos matemáticos, time para manejo de tiempo y pygame para reproducir sonidos de alerta.
Configura la captura de video desde una URL específica y ajusta la resolución para mejorar el rendimiento.
Inicializa variables de control para la detección de microsueños y configura MediaPipe para la detección de la malla facial.
Captura y Procesamiento de Video:

En un bucle continuo, captura cada frame del video.
Cada dos frames, convierte el frame a formato RGB y procesa la malla facial usando MediaPipe.
Si se detectan rostros, extrae y dibuja los puntos de referencia de la malla facial en el frame.
Verifica la posición de puntos clave para medir la apertura de los párpados.
Si la apertura de los párpados es menor que un umbral específico durante más de 2 segundos, se reproduce un sonido de alerta y se incrementa el conteo de microsueños.
Salida del Programa:

Muestra el video procesado en una ventana y permite salir del bucle si se presiona la tecla 'q'.
Finalmente, libera los recursos utilizados.
El objetivo principal del algoritmo es identificar y alertar a los conductores sobre microsueños, ayudando a prevenir colisiones y mejorar la seguridad vial.
