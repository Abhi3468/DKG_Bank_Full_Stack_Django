# DKG_ATM/Dockerfile
# Use Python 3.11 (matching runtime.txt) - more stable than 3.12 for Django 4.2
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user FIRST (better layer caching)
RUN groupadd -r django && useradd -r -g django django

# Set work directory
WORKDIR /app

# Install Python dependencies (cacheable layer)
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy project files
COPY --chown=django:django . .

# Collect static files (FAIL if error - don't hide with || true)
RUN python manage.py collectstatic --noinput

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python manage.py check --deploy || exit 1

# Run gunicorn with optimized settings
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--worker-class", "sync", \
     "--worker-tmp-dir", "/dev/shm", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "DKG_ATM.wsgi:application"]