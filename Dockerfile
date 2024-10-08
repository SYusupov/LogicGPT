# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.10-slim
FROM python:${PYTHON_VERSION} AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y g++ curl

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
# RUN python -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install --no-cache-dir -r requirements.txt

RUN rm -rf /root/.cache /var/lib/apt/lists/*

# Expose the port that the application listens on.
EXPOSE 8501

# Ensure Streamlit is available
RUN python -m streamlit --version

# Run the application.
CMD streamlit run /app/app_ui.py