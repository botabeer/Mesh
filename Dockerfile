# Base image
FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port (Render/Heroku uses $PORT)
EXPOSE 8080

# Set environment variables defaults (can override)
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV PORT=8080

# Run the bot with Gunicorn
CMD ["gunicorn", "app:app", "-w", "4", "-k", "gthread", "-b", "0.0.0.0:8080"]
