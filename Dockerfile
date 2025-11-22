# Bot Mesh - Dockerfile
# Created by: Abeer Aldosari © 2025

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data && chmod 755 /app/data

EXPOSE 5000

CMD ["python", "app.py"]
