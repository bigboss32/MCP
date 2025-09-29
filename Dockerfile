# Imagen base con Python 3.11
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Exponer el puerto del MCP
EXPOSE 8080

# Comando por defecto para arrancar el MCP
CMD ["python", "server.py"]
