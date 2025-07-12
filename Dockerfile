# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY back/ /app
COPY templates/ /app/templates
COPY requirements.txt /app/
COPY static/ /app/static


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
