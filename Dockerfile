# Full Python image — install dependencies here
# This stage is discarded in the final image
# ═══════════════════════════════════════════════════════════════
FROM python:3.11 AS builder
WORKDIR /build

# Copy only requirements — not source code
COPY requirements.txt .

# Install packages into /install prefix
# --prefix: install to specific directory so we can copy it cleanly
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ═══════════════════════════════════════════════════════════════
# Stage 2: Runtime
# Slim Python image — only what the app needs to RUN
# No build tools, no pip cache, no compiler
# ═══════════════════════════════════════════════════════════════
FROM python:3.11-slim AS runtime

LABEL maintainer="Anuj Chaturvedi"
LABEL project="jobportal"
LABEL stage="Week 4 — Multi-stage build"

WORKDIR /app

# Copy installed packages from builder stage ONLY
# Everything else from the builder stage is left behind
COPY --from=builder /install /usr/local

# Copy only the application source files needed at runtime
COPY app.py homepage.py jobs.py auth.py categories.py config.py utils.py ./

EXPOSE 5000

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

CMD ["python3","app.py"]
