# Usamos Python 3.12 slim para tener algo liviano
FROM python:3.12-slim

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

# Evitamos buffers de stdout/stderr
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1

# Carpeta de la app dentro del contenedor
WORKDIR /app

# Copiamos archivos de requirements primero para caching
COPY pyproject.toml uv.lock ./

# System deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalamos dependencias
RUN pip install --no-cache-dir uv \
    && uv sync --frozen

# Copiamos toda la app
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Exponemos puerto de la API
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run migrations before starting the app
CMD ["sh", "-c", "uv run dbwarden migrate --all && /app/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000"]
