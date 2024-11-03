import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Cargar el modelo
model = load_model('face_recognition/models/facial_recognition_model.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def recognize_face(image):
    """Detecta un rostro y lo autentica."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        print("No se detectaron rostros.")
        return None, 0.0  # Si no hay rostro detectado

    # Usar el primer rostro detectado
    (x, y, w, h) = faces[0]
    face_img = image[y:y+h, x:x+w]  # Recortar el rostro de la imagen original

    # Asegurarse de que la imagen esté en formato RGB si el modelo lo requiere
    face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

    try:
        resized = cv2.resize(face_rgb, (128, 128))  # Ajustar tamaño a 128x128
    except cv2.error as e:
        print(f"Error al redimensionar la imagen: {e}")
        return None, 0.0

    normalized = resized / 255.0  # Normalizar la imagen
    reshaped = np.reshape(normalized, (1, 128, 128, 3))  # Asegurar que tenga 3 canales

    predictions = model.predict(reshaped)
    user_id = np.argmax(predictions)  # Obtener el ID del usuario
    confidence = np.max(predictions)  # Obtener la confianza

    return user_id, confidence



    
