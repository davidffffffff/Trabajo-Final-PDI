#--------------------------------------------------------------------------
#---------------------Detección de microsueños-----------------------------
#------- Por: David Florez Ospitia    david.florez1@udea.edu.co------------
#-------      Estudiante, Facultad de Ingenieria BLQ 21-409  --------------
#---------------------      CC 1007385838     -----------------------------
#------- Curso Básico de Procesamiento de Imágenes y Visión Artificial-----
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
#--1. Inicializo el sistema -----------------------------------------------
#--------------------------------------------------------------------------

import cv2
import mediapipe as mp
import math
import time
import pygame

# Inicializar pygame y el sonido
pygame.mixer.init()
pygame.mixer.music.load('alert_sound.flac')  # Asegúrate de tener un archivo 'alert_sound.flac' en el mismo directorio

# URL del stream de video
url = 'http://192.168.255.149:8080/video'

# Configuración de captura de video
cap = cv2.VideoCapture(url)
cap.set(3, 640)  # Reducir resolución a 640x480 para mejorar el rendimiento
cap.set(4, 480)

# Variables de control para detección de microsueños
conteo_sue = 0
inicio = 0
parpadeo = False

# Inicialización de MediaPipe para detección de malla facial
mpDibujo = mp.solutions.drawing_utils
ConfDibu = mpDibujo.DrawingSpec(thickness=1, circle_radius=0)  # Ajusta el grosor y el radio de los círculos
mpMallaFacial = mp.solutions.face_mesh
MallaFacial = mpMallaFacial.FaceMesh(max_num_faces=1)

# Contador de frames para procesar cada 2 cuadros
frame_count = 0
process_every_nth_frame = 2  # Procesar cada 2 cuadros
ultimo_resultado = None

#--------------------------------------------------------------------------
#--2. Proceso de captura y procesamiento de video -------------------------
#--------------------------------------------------------------------------

while True:
    # Captura del frame
    ret, frame = cap.read()
    if not ret:
        print("Error: No se puede recibir el frame (streaming finalizado o error de captura)")
        break

    # Incremento del contador de frames
    frame_count += 1
    
    # Procesar cada 2 cuadros para mejorar el rendimiento
    if frame_count % process_every_nth_frame == 0:
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir frame a RGB
        resultados = MallaFacial.process(frameRGB)  # Procesar frame con MediaPipe
        if resultados.multi_face_landmarks:
            ultimo_resultado = resultados
    else:
        resultados = ultimo_resultado

    # Detección de malla facial
    if resultados and resultados.multi_face_landmarks:
        al, an, c = frame.shape
        lista = []
        for rostros in resultados.multi_face_landmarks:
            mpDibujo.draw_landmarks(frame, rostros, mpMallaFacial.FACEMESH_TESSELATION, ConfDibu, ConfDibu)
            
            for id, landmark in enumerate(rostros.landmark):
                x = int(landmark.x * an)
                y = int(landmark.y * al)
                lista.append([id, x, y])
                
                # Verificación de puntos clave en la malla facial
                if len(lista) == 468:
                    # Puntos para medir el parpadeo
                    x1, y1 = lista[159][1:]  # Párpado superior
                    x2, y2 = lista[145][1:]  # Párpado inferior
                    longitud1 = math.hypot(x2 - x1, y2 - y1)

                    x3, y3 = lista[386][1:]  # Párpado superior
                    x4, y4 = lista[374][1:]  # Párpado inferior
                    longitud2 = math.hypot(x4 - x3, y4 - y3)

                    # Mostrar conteo de microsueños en el frame
                    cv2.putText(frame, f'Micro Suenos: {int(conteo_sue)}', (30, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2) 
                    
                    # Detección de parpadeo
                    if longitud1 <= 4 and longitud2 <= 4 and not parpadeo:  # Aumentar el umbral a 6
                        parpadeo = True
                        inicio = time.time()

                    # Verificar duración del parpadeo para contar microsueño
                    if parpadeo and (time.time() - inicio) > 2:
                        pygame.mixer.music.play()  # Reproducir sonido de alerta
                        conteo_sue += 1
                        parpadeo = False  # Reiniciar el estado de parpadeo para la próxima vez                        

    # Mostrar el frame en una ventana
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):  # Salir del bucle si se presiona 'q'
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

#--------------------------------------------------------------------------
#---------------------------  FIN DEL PROGRAMA ----------------------------
#--------------------------------------------------------------------------