# Usamos Python 3.12 slim para tener algo liviano
FROM python:3.12-slim

# Evitamos buffers de stdout/stderr
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1

# Carpeta de la app dentro del contenedor
WORKDIR /app

# Copiamos archivos de requirements primero para caching
COPY pyproject.toml .

# System deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalamos dependencias
RUN pip install --no-cache-dir uv \
    && uv sync

# Copiamos toda la app
COPY . .

# Exponemos puerto de la API
EXPOSE 8000

# Comando para correr FastAPI con uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
