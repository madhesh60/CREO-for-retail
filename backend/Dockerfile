# Backend Dockerfile
FROM python:3.10-slim

# Install system dependencies for OpenCV and Pillow
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for cache optimization
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
