# syntax=docker/dockerfile:1
# Stage 1: Build stage
ARG PYTHON_VERSION=3.10-slim
FROM python:${PYTHON_VERSION} AS builder

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Add dependencies before the pip install step
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    && python -m pip install --upgrade pip setuptools wheel \
    && rm -rf /var/lib/apt/lists/*

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Install gdown for downloading files from Google Drive
RUN pip install gdown
# Create the /model_files directory
RUN mkdir -p /model_files
# Download the model using gdown
RUN gdown 1MMdhxFgvcwgFXi068atfqIbGn1m8ur_l -O /model_files/unsloth.Q4_K_M.gguf

# Stage 2: Final stage
FROM python:3.10-slim

WORKDIR /app
# Copy only the needed parts from the builder stage
COPY --from=builder /model_files /model_files

ENV PYTHONPATH=/app
# # Copy the source code into the container.
# COPY ./app /app # loaded with containers
# COPY ./model_files /model_files
# Ensure that the model file is readable by all users
RUN chmod -R 755 /model_files

# # Create a non-root user called appuser
# RUN useradd -m appuser
# # Switch to the non-privileged user to run the application.
# USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0", "--log-level", "debug"]
