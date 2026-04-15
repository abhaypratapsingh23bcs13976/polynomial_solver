FROM python:3.9-slim

WORKDIR /app

# Install dependencies for matplotlib
RUN apt-get update && apt-get install -y \
    build-essential \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose API port
EXPOSE 5000

# Run the application using Gunicorn for production
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} app:app
