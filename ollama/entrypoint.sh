#!/bin/bash

# Start Ollama in the background
ollama serve &

# Wait for the Ollama service to be available
until curl -s http://localhost:11435/api/health; do
  echo "Waiting for Ollama to start..."
  sleep 2
done

# Create the mistral model
ollama create mistral -f /Modelfile

# Keep the Ollama service running in the foreground
fg
