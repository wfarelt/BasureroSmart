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

# POSTGRES

sudo -u postgres psql
CREATE DATABASE basurero_prod;
CREATE USER wfarel WITH PASSWORD 'wf12345*';

ALTER ROLE wfarel SET client_encoding TO 'utf8';
ALTER ROLE wfarel SET default_transaction_isolation TO 'read committed';
ALTER ROLE wfarel SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE basurero_prod TO wfarel;
GRANT ALL PRIVILEGES ON SCHEMA public TO wfarel;
ALTER SCHEMA public OWNER TO wfarel;
ALTER DATABASE nombasurero_prod OWNER TO wfarel;


\q

# Install Django, Gunicorn, and the psycopg2 PostgreSQL adaptor

pip install gunicorn psycopg2-binary

sudo nano /etc/nginx/sites-available/BasureroSmart

server {
    listen 80;
    server_name 192.168.50.153;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /staticfiles/ {
        root /home/wfarel/BasureroSmart;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

sudo ln -s /etc/nginx/sites-available/BasureroSmart /etc/nginx/sites-enabled
sudo nginx -t

sudo systemctl restart gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket gunicorn.service