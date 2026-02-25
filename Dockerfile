# Dockerfile for Piper Morgan Main Application
# PM-055 Step 2: Docker configuration for Python 3.11 consistency
# Created: 2025-07-22

# Use Python 3.11-slim base image for PM-055 compliance
FROM python:3.11-slim-bullseye

# Set Python version environment variable for verification
ENV PYTHON_VERSION=3.11

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Add Python version verification during build
RUN python --version && \
    python -c "import sys; assert sys.version_info >= (3, 11), f'Python {sys.version} < 3.11 (PM-055 requirement)'"

# Copy application code
COPY . .

# Create version verification script in image (avoids CRLF from Windows host)
RUN set -e && cat > /usr/local/bin/verify-python-version.sh << 'VERIFY_EOF'
#!/bin/bash
set -e
echo "Verifying Python version for PM-055 compliance..."
PYTHON_FULL_VERSION=$(python --version 2>&1)
PYTHON_VERSION=$(echo "$PYTHON_FULL_VERSION" | awk '{print $2}' | cut -d. -f1-2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
echo "Detected Python version: $PYTHON_VERSION"
if [[ "$PYTHON_MAJOR" -lt 3 ]] || [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -lt 11 ]]; then
    echo "ERROR: Python $PYTHON_VERSION does not meet PM-055 requirements (>=3.11)"
    exit 1
fi
echo "Python version $PYTHON_VERSION meets PM-055 requirements."
python -c "import sys; import asyncio, fastapi, sqlalchemy, uvicorn; print('Dependencies OK')" || exit 1
echo "Docker container ready with Python 3.11 (PM-055 compliant)"
VERIFY_EOF
RUN chmod +x /usr/local/bin/verify-python-version.sh

# Set PYTHONPATH for proper module imports
ENV PYTHONPATH=/app:$PYTHONPATH

# Create non-root user for security
RUN groupadd -r piper && useradd -r -g piper piper
RUN chown -R piper:piper /app
USER piper

# Expose port for main application
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8001/health', timeout=5)" || exit 1

# Run version verification on startup, then start application
CMD ["/bin/bash", "-c", "/usr/local/bin/verify-python-version.sh && python main.py"]
