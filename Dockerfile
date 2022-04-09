FROM nexus.okala.com:10000/python:3.10

# Edit with mysql-client, postgresql-client, sqlite3, etc. for your needs.
# Or delete entirely if not needed.
RUN mkdir /app \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# For Django
EXPOSE 80
#CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
CMD ["sh","-c","python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:80"]
