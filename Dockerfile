# =========================================
# Bot Mesh - Dockerfile
# Author: Abeer Aldosari © 2025
# Description: Container setup for Bot Mesh
# =========================================

# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables for LINE Bot (to override in deployment)
ENV LINE_CHANNEL_ACCESS_TOKEN=""
ENV LINE_CHANNEL_SECRET=""
ENV DB_PATH="data/game.db"
ENV REDIS_ENABLED="false"
ENV REDIS_URL="redis://localhost:6379/0"
ENV CACHE_TTL="3600"

# Start the bot
CMD ["python", "app.py"]
