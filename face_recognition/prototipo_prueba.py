import cv2
import time  # Importar para gestionar tiempo
from face_recognition import recognize_face 

def prototipo_prueba():
    cap = cv2.VideoCapture(0)  # Acceder a la cámara
    
    last_detection_time = 0  # Inicializar la última detección exitosa
    detection_interval = 2  # Esperar 2 segundos entre detecciones

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al acceder a la cámara.")
            break

         # Obtener el tiempo actual
        current_time = time.time()
        
        if current_time - last_detection_time >= detection_interval:
        
            user_id, confidence = recognize_face(frame)

            if user_id is not None and confidence > 0.80:
                print(f"Usuario detectado: {user_id} - Confianza: {confidence}")
                # Actualizar el tiempo de la última detección exitosa
                last_detection_time = current_time
            else:
                print(f"Confianza insuficiente: {confidence}. Usuario no reconocido.")

        # Mostrar video en tiempo real
        cv2.imshow('Prototipo de Prueba', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Presionar 'q' para salir
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    prototipo_prueba()
