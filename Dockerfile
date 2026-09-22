# Base image — Python 3.11 on slim Debian
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (layer caching — only reinstall if requirements change)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py homepage.py jobs.py auth.py categories.py config.py utils.py ./

# Default command to run when container starts
CMD ["python3", "app.py"]