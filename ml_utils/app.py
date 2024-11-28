from flask import Flask, request, jsonify
import cv2
import numpy as np
from face_recognition import recognize_face

app = Flask(__name__)

@app.route('/recognize_face', methods=['POST'])
def recognize_face_endpoint():
    if 'face_image' not in request.files:
        return jsonify({'error': 'No face_image part in the request'}), 400

    file = request.files['face_image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Leer la imagen en formato de bytes
    file_bytes = np.frombuffer(file.read(), np.uint8)
    # Convertir los bytes a una imagen
    face_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Llamar a la función recognize_face
    user_id, confidence = recognize_face(face_image)

    return jsonify({'user_id': user_id, 'confidence': confidence})

if __name__ == '__main__':
    app.run(debug=True)