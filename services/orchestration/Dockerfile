# Dockerfile for the Orchestration Service (Temporal Worker)
# 2025-06-03: Initial Dockerfile for orchestration service.
# 2025-07-22: Updated for PM-055 Python 3.11 consistency

# Use Python 3.11-slim base image for PM-055 compliance
FROM python:3.11-slim-bullseye

# Set Python version environment variable for verification
ENV PYTHON_VERSION=3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the top-level requirements.txt into the container
# This assumes requirements.txt is at the project root
COPY requirements.txt .

# Install Python dependencies with version verification
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Add Python version verification during build
RUN python --version && \
    python -c "import sys; assert sys.version_info >= (3, 11), f'Python {sys.version} < 3.11 (PM-055 requirement)'"

# Copy the entire 'services' directory into the container
# This allows imports like 'from services.shared_types import ...'
# This path should match the volume mount in docker-compose.yml: ./services:/app/services
COPY services /app/services

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

# Set PYTHONPATH to include the /app directory, so Python can find 'services' package
ENV PYTHONPATH=/app:$PYTHONPATH

# Keep container running until a Temporal worker entrypoint is implemented.
# When worker exists, switch to: CMD ["/bin/bash", "-c", "/usr/local/bin/verify-python-version.sh && python -m services.orchestration.worker"]
CMD ["sleep", "infinity"]
