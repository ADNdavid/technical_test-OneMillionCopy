FROM python:3.13-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install UV package manager and runtime dependencies from pyproject.toml
RUN python -m pip install --no-cache-dir --upgrade pip uv

# Copy project files and install dependencies via UV
COPY pyproject.toml /app/
COPY . /app
RUN uv install --no-interaction --no-ansi

# Expose the default FastAPI port
EXPOSE 8000

# Run the application using UV
CMD ["uv", "run", "main:app", "--host", "0.0.0.0", "--port", "8000"]
