FROM python:3.11-slim

WORKDIR /app

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copiar todo el proyecto (no solo pyproject.toml)
COPY pyproject.toml uv.lock README.md ./ 
COPY src/ ./src

# Instalar dependencias (ahora uv encuentra src/my_server)
RUN uv sync --frozen

# Archivos adicionales (opcional, si quieres base de datos o .env)
COPY database.db .env ./

# Comando por defecto
CMD ["uv", "run", "python", "-m", "src.main"]
