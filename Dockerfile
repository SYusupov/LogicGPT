# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.10-slim
FROM python:${PYTHON_VERSION} AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set to noninteractive to avoid interactive prompts
# ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Add dependencies before the pip install step
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     cmake \
#     g++
    # && python -m pip install --upgrade pip setuptools wheel

RUN apt-get update && apt-get install -y g++

# RUN !CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install  llama-cpp-python --no-cache-dir

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
# RUN python -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install --no-cache-dir -r requirements.txt

# Create the /model_files directory
# and Download the model using gdown
# and remove unnecessary packages after downloading everything
# RUN mkdir -p /model_files \
#     && gdown 1MMdhxFgvcwgFXi068atfqIbGn1m8ur_l -O /model_files/unsloth.Q4_K_M.gguf \
    # && apt-get purge -y --auto-remove build-essential cmake g++ \
RUN rm -rf /root/.cache /var/lib/apt/lists/*
    # && pip uninstall -y gdown

ENV PYTHONPATH=/app
# # Copy the source code into the container.
# COPY ./app /app # loaded with containers
# COPY ./model_files /model_files
# Ensure that the model file is readable by all users
# RUN chmod -R 755 /model_files

# # Create a non-root user called appuser
# RUN useradd -m appuser
# # Switch to the non-privileged user to run the application.
# USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0", "--log-level", "debug"]
