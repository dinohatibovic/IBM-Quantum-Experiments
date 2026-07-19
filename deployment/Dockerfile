# QOptiSolve Dockerfile

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY qoptisolve/ ./qoptisolve
COPY README.md .

# Expose FastAPI port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "qoptisolve.app:app", "--host", "0.0.0.0", "--port", "8000"]
