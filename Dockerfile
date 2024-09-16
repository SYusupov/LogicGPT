# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10-slim
FROM python:${PYTHON_VERSION} as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install --no-cache-dir -r requirements.txt

# # Clone and install lm-evaluation-harness
# RUN git clone --depth 1 https://github.com/EleutherAI/lm-evaluation-harness && \
# cd lm-evaluation-harness && \
# pip install -e .

ENV PYTHONPATH=/app
# Copy the source code into the container.
COPY ./app /app

# Create a non-root user called appuser
RUN useradd -m appuser
# Switch to the non-privileged user to run the application.
USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0", "--log-level", "debug"]
