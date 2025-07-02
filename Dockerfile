# Use Microsoft's official Playwright image with Python
# This image comes pre-installed with Chrome, Chromium, Firefox, and WebKit browsers
FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

# Set working directory (avoid conflict with app/ module directory)
WORKDIR /workspace

# Set environment variables for Playwright and Python
ENV PYTHONPATH=/workspace
# Let Playwright automatically detect browsers - no path restrictions
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Install system dependencies required for your project
RUN apt-get update && apt-get install -y \
    # Required for WeasyPrint (PDF generation)
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    # Required for psycopg2 (PostgreSQL adapter)
    libpq-dev \
    gcc \
    # General utilities
    curl \
    wget \
    # Add sudo and allow pwuser to use it without password
    sudo \
    && rm -rf /var/lib/apt/lists/* \
    # Add pwuser to sudo group and allow passwordless sudo
    && echo "pwuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Install UV package manager for faster dependency installation
RUN pip install --no-cache-dir uv

# Copy dependency files first (for better Docker layer caching)
COPY pyproject.toml uv.lock ./

# Copy the entire application
COPY . .

# Change ownership to pwuser before creating virtual environment
RUN chown -R pwuser:pwuser /workspace

# Switch to pwuser early so virtual environment is created with correct permissions
USER pwuser


# Create virtual environment as pwuser
RUN uv venv /workspace/.venv

# Activate virtual environment and install dependencies
RUN . /workspace/.venv/bin/activate && uv sync --frozen --no-dev

# Install Playwright browsers using the UV-installed version as pwuser
# pwuser now has sudo privileges to install system dependencies
RUN . /workspace/.venv/bin/activate && playwright install chrome --with-deps

# Verify browsers are available using the virtual environment's Playwright
RUN . /workspace/.venv/bin/activate && playwright install chrome --dry-run
RUN . /workspace/.venv/bin/activate && playwright chrome --version

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

# Expose the port
EXPOSE $PORT

# Run the application by creating virtual environment if needed and activating it
# This handles cases where volume mounts might override the built virtual environment
CMD ["/bin/bash", "-c", "[ ! -f /workspace/.venv/bin/activate ] && echo 'Creating virtual environment...' && uv venv /workspace/.venv && . /workspace/.venv/bin/activate && uv sync --frozen --no-dev || echo 'Virtual environment exists'; source /workspace/.venv/bin/activate && uvicorn --version && echo 'Starting FastAPI application...' && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
