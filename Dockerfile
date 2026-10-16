# Base image: Python 3.11 on slim Debian (smaller than full debian)
FROM python:3.11-slim

# Metadata
LABEL maintainer="Anuj Chaturvedi"
LABEL project="jobportal"
LABEL week="4"

# Set working directory inside container
WORKDIR /app

# Copy requirements FIRST — layer caching optimisation
# This layer only rebuilds when requirements.txt changes
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir: do not store pip cache in image (keeps image smaller)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code AFTER dependencies
# This layer rebuilds on every code change — but pip install above is cached
COPY app.py homepage.py jobs.py auth.py categories.py config.py utils.py ./

# Document which port the app listens on
# This does NOT open the port — it is documentation + hint for -p flag
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Default command to run when container starts
CMD ["python3", "app.py"]
