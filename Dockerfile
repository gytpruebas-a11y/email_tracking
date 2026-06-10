# Imagen base de Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto
EXPOSE 8002

# Comando para correr FastAPI con Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8002"]
