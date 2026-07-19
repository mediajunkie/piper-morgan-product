# syntax=docker/dockerfile:1
# Dockerfile for Piper Morgan Main Application
# PM-055 Step 2: Docker configuration for Python 3.11 consistency
# Created: 2025-07-22

# Use Python 3.11-slim base image for PM-055 compliance.
# MUST be slim-bookworm (Debian 12 → sqlite 3.40.1): chromadb requires sqlite >= 3.35.
# slim-bullseye (Debian 11) ships sqlite 3.34.1 and crash-loops the app on startup (#1299).
# Do NOT downgrade to bullseye. The live 0.8.7 droplet image was bookworm; the repo had
# drifted to bullseye, which broke the 0.8.8 deploy (rolled back 2026-06-19).
FROM python:3.11-slim-bookworm

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

# Install Python dependencies.
# BuildKit cache mount (#1408): persists pip's download/wheel cache across builds
# in BuildKit storage — NOT in the image layer — so a code-only rebuild whose
# docker layer-cache misses re-installs from local wheels instead of re-downloading
# the whole dep set. torch alone is 821MB; at the droplet's ~290kB/s that download
# was ~45min of every dot-deploy. The mount keeps the image slim (cache isn't a
# layer) while killing the re-download. Requires BuildKit (the `# syntax` directive
# above enables it; the droplet + Fly builders both use buildx).
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    # #1409: pre-seed the CPU-only torch wheel BEFORE the requirements install.
    # `pip install torch` on Linux defaults to the CUDA build and drags ~4GB of
    # nvidia_*_cu12 wheels no CPU-only host (droplet, Fly) ever uses. With
    # torch already satisfied at the same version, the requirements resolve
    # skips it entirely. Keep the version in lockstep with requirements.txt.
    pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu && \
    pip install -r requirements.txt

# Add Python version verification during build
RUN python --version && \
    python -c "import sys; assert sys.version_info >= (3, 11), f'Python {sys.version} < 3.11 (PM-055 requirement)'"

# Copy application code
COPY . .

# Create version verification script inline (avoids CRLF issues from Windows hosts)
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
python -c "
import sys
try:
    import asyncio, fastapi, sqlalchemy, uvicorn
    print('Core dependencies compatible with Python {}.{}'.format(sys.version_info.major, sys.version_info.minor))
except ImportError as e:
    print('Dependency compatibility issue:', e)
    sys.exit(1)
" || exit 1
python -c "
import asyncio
async def test_async():
    return 'async_ok'
result = asyncio.run(test_async())
assert result == 'async_ok', 'Async test failed'
print('Async patterns working correctly')
" || exit 1
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
