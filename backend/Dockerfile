# Folosește o imagine de bază cu Python
FROM python:3.11-slim

# Setează directorul de lucru
WORKDIR /app

# Instalează dependențele sistemului necesare (ex. pentru psycopg2 dacă folosești PostgreSQL)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiază fișierul requirements.txt și instalează dependențele Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiază întregul proiect în container
COPY . .

# Setează variabilele de mediu (opțional, pot fi suprascrise în docker-compose.yml)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expune portul pe care rulează aplicația (implicit 8000 pentru Django)
EXPOSE 8000

# Comandă pentru a rula aplicația
CMD ["python", "manage.py", "runserver"]