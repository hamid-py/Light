FROM python:slim-buster
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

RUN python manage.py makemigrations

EXPOSE 80


CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:80"]
