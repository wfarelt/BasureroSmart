import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)  # Abre la cámara

if not cap.isOpened():
    print("No se pudo abrir la cámara.")
else:
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("No se pudo leer el fotograma.")
    else:
        # Convertir de BGR a RGB para mostrar con matplotlib
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        plt.imshow(frame_rgb)
        plt.axis('off')  # Oculta los ejes
        plt.show()
