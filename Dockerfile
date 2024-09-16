# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10-slim
FROM python:${PYTHON_VERSION} AS base

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
    && rm -rf /var/lib/apt/lists/*

# Update pip and setuptools
RUN python -m pip install --upgrade pip setuptools wheel

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Download the model from Google Drive
RUN curl -L -o /model_files/unsloth.Q4_K_M.gguf "https://drive.google.com/uc?export=download&id=1MMdhxFgvcwgFXi068atfqIbGn1m8ur_l"

# # Clone and install lm-evaluation-harness
# RUN git clone --depth 1 https://github.com/EleutherAI/lm-evaluation-harness && \
# cd lm-evaluation-harness && \
# pip install -e .

ENV PYTHONPATH=/app
# # Copy the source code into the container.
# COPY ./app /app
# COPY ./model_files /model_files

# Create a non-root user called appuser
RUN useradd -m appuser
# Switch to the non-privileged user to run the application.
USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0", "--log-level", "debug"]
