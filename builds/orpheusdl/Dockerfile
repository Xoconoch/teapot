FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copiar el contenido al contenedor
COPY dockerorpheus /app

# Instalar dependencias como root
RUN apt-get update && apt-get install -y nano && pip install -r /app/requirements.txt

