# BasureroSmart
Basurero inteligente

# Deocuple
pip install python-decouple

# Crear un archivo .env
# Configuración para el entorno local
DJANGO_ENV=local

# Configuración para la base de datos local

    LOCAL_DATABASE_ENGINE=django.db.backends.sqlite3
    LOCAL_DATABASE_NAME=db.sqlite3

    # Configuración para la base de datos de producción
    PROD_DATABASE_ENGINE=django.db.backends.postgresql
    PROD_DATABASE_NAME=basurero_prod
    PROD_DATABASE_USER=wfarel
    PROD_DATABASE_PASSWORD=wf12345*
    PROD_DATABASE_HOST=localhost
    PROD_DATABASE_PORT=5432

    # Configuración adicional para el entorno de producción
    ALLOWED_HOSTS=localhost,127.0.0.1,192.168.10.153,177.222.109.127