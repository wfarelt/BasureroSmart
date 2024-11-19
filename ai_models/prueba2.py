import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Cargar el modelo entrenado
model = load_model('ai_models/facial_recognition_model.h5')

# Parámetros del modelo
IMG_SIZE = 128  # Tamaño al que redimensionamos las imágenes
LABELS = {0: 'Usuario_0', 1: 'Usuario_1', 2: 'Usuario_2'}  # Etiquetas de ejemplo

def preprocess_face(face):
    """Preprocesar la cara detectada para la predicción."""
    face = cv2.resize(face, (IMG_SIZE, IMG_SIZE))  # Redimensionar la imagen
    face = face.astype('float32') / 255.0  # Normalizar
    face = np.expand_dims(face, axis=0)  # Añadir batch dimension
    return face

def recognize_face(face):
    """Realizar la predicción del modelo sobre una cara."""
    processed_face = preprocess_face(face)
    prediction = model.predict(processed_face)
    user_id = np.argmax(prediction)  # ID del usuario con mayor probabilidad
    confidence = np.max(prediction)  # Confianza de la predicción
    return user_id, confidence

# Inicializar la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a escala de grises para detección
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = frame[y:y + h, x:x + w]  # Extraer la cara detectada
        user_id, confidence = recognize_face(face)  # Predecir usuario

        print(f"Usuario: {LABELS.get(user_id, 'Desconocido')}, Confianza: {confidence:.2f}")

        # Dibujar rectángulo y texto en la cara detectada
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {LABELS.get(user_id, 'Desconocido')}", (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    # Mostrar el video con detecciones
    cv2.imshow("Reconocimiento Facial", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
