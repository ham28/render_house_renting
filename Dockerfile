# Utiliser une image Python officielle
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source
COPY . .

# Exposer le port sur lequel Django va s'exécuter
EXPOSE 8000

# Définir la variable d'environnement pour Python
ENV PYTHONPATH=/app

# Commande pour appliquer les migrations et démarrer le serveur Django
CMD ["sh", "-c", "python manage.py makemigrations && \
                  python manage.py migrate && \
                  for fixture in fixtures/*.json; do python manage.py loaddata $fixture 2>/dev/null || true; done && \
                  python manage.py runserver 0.0.0.0:8000"]