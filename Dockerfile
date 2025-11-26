# Imagen base Python
FROM python:3.10-slim

# Crea directorio de trabajo
WORKDIR /app

# Copia requirements
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código
COPY . .

# Exponer puerto Flask
EXPOSE 5000

# Comando para ejecutar con Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
