FROM python:3.11-slim

# Instalar Docker, dependencias y herramientas necesarias
RUN apt-get update && apt-get install -y \
    docker.io \
    iptables \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Crear el directorio de logs para dockerd
RUN mkdir -p /var/log && touch /var/log/dockerd.log

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de la aplicación
COPY ./app.py ./
COPY ./frontend ./frontend
COPY ./app ./app
COPY ./requirements.txt ./
COPY ./orpheusdl.tar ./
COPY ./zotify.tar ./

# Copiar y configurar el script de entrada
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto de Flask
EXPOSE 7983

# Crear directorios de configuracion

RUN mkdir /app/credentials
RUN mkdir /app/config
RUN mkdir /app/downloads

# Variables de entorno para Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Usar el script de entrada para iniciar los servicios
CMD ["/entrypoint.sh"]
