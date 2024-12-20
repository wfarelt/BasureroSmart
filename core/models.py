from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser
from django.db import models

import cv2
import os

def recortar_foto(path_image, id_user):
    # Cargar el clasificador de cara de OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Leer la imagen
    img = cv2.imread(path_image)

    # Verificar si la imagen fue cargada correctamente
    if img is None:
        print(f"Error: No se pudo cargar la imagen en {path_image}.")
        return

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detectar caras en la imagen
    try:
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    except Exception as e:
        print(f"Error al detectar caras en la imagen: {e}")
        return

    # Si se detecta al menos una cara
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            # Recortar la cara de la imagen
            face_img = img[y:y+h, x:x+w]

            # Guardar la imagen de la cara recortada
            cv2.imwrite(path_image, face_img)
            print(f"Foto registrada exitosamente: {path_image}")
            break  # Solo guardamos la primera cara detectada
        return True
    else:
        print("No se detectó ninguna cara en la imagen.")
        return False

# Modelo extendido de usuario para añadir la bonificación total
def user_directory_path(instance, filename):
    # Consultar si no tiene id, es porque es un nuevo usuario
    if not instance.id:
        last_id = User.objects.last().id + 1
    else:
        last_id = instance.id
    
    return f'datasets/faces/{last_id}/{filename}'

class User(AbstractUser):
    total_points = models.PositiveIntegerField(default=0, verbose_name="Total de Puntos")
    image_perfil = models.ImageField(upload_to=user_directory_path, null=True, blank=True, verbose_name="Imagen de Perfil")
    image_perfil2 = models.ImageField(upload_to=user_directory_path, null=True, blank=True, verbose_name="Imagen de Perfil 2")
    image_perfil3 = models.ImageField(upload_to=user_directory_path, null=True, blank=True, verbose_name="Imagen de Perfil 3")
   
    def __str__(self):
        return f"{self.username} - Puntos: {self.total_points}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        image_fields = ["image_perfil", "image_perfil2", "image_perfil3"]

        for field_name in image_fields:
            image_field = getattr(self, field_name, None)
            if image_field:  # Si la imagen existe
                try:
                    print(f"Recortando imagen... {image_field.name}")
                    path_image = f"media/{image_field.name}"
                    if recortar_foto(path_image, self.id):
                        print(f"Imagen recortada exitosamente: {image_field.name}")
                    else:
                        print(f"No se pudo recortar la imagen: {image_field.name}")
                        # Eliminar imagen si no se pudo recortar
                        os.remove(path_image)
                except Exception as e:
                    print(f"Error al recortar la imagen {field_name}: {e}")
    
    def total_transactions(self):
        return self.transactions.count()
    
    def total_claims(self):
        return self.claims.count()

# Modelo para representar los contenedores de basura
class WasteContainer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del Contenedor")
    location = models.CharField(max_length=255, verbose_name="Ubicación del Contenedor")
    #Estado del contenedor choises = [Opertivo, lleno, en mantenimiento]
    status = models.CharField(max_length=20, 
                              choices=[('Operativo', 'Operativo'), 
                                       ('Lleno', 'Lleno'), 
                                       ('Mantenimiento','Mantenimiento')], 
                              default='Operativo')
    last_maintenance = models.DateTimeField(auto_now_add=True, verbose_name="Último Mantenimiento")
    capacity = models.PositiveIntegerField(verbose_name="Capacidad del Contenedor", default=100)
    # Nivel actual de residuos en el contenedor en porcentaje
    current_level = models.PositiveIntegerField(verbose_name="Nivel Actual de Residuos", default=0)
    
    def __str__(self):
        return f"{self.name} - {self.location} - {self.status}"

# Modelo para representar los tipos de residuos
class WasteType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tipo de Residuo")
    bonus_points = models.PositiveIntegerField(verbose_name="Bonificación en Puntos")

    def __str__(self):
        return f"{self.name} - {self.bonus_points} Puntos"

# Modelo para registrar cada reciclaje realizado por los usuarios
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    waste_type = models.ForeignKey(WasteType, on_delete=models.CASCADE, verbose_name="Tipo de Residuo")
    container = models.ForeignKey(WasteContainer, on_delete=models.CASCADE, verbose_name="Contenedor")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Transacción")
    points_awarded = models.PositiveIntegerField(verbose_name="Puntos Otorgados")

    def __str__(self):
        return f"Transacción - {self.user.username}: {self.points_awarded} puntos"

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"

    # Método para guardar la transacción y actualizar los puntos del usuario, solo si la transacción es nueva
    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.total_points += self.points_awarded
            self.user.save()
            self.container.current_level += 1
            self.container.save()
        super().save(*args, **kwargs)
        
