# Dockerfile for Churn & LTV API Server
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install compile tools and postgresql binary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python packages using caching layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire workspace into the image
COPY . .

# Expose port 8000 for local access
EXPOSE 8000

# Start FastAPI server on port 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
