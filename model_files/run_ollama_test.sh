#!/bin/bash

echo "Starting Ollama server..."
ollama serve &  # Start Ollama in the background
OLLAMA_PID=$!  # Store the process ID of the Ollama server

echo "Ollama is ready, creating the model..."

ollama create finetuned_mistral -f /model_files/Modelfile
ollama run finetuned_mistral

sleep 10
# run the pytests
/bin/sh -c "pytest /app/test_api.py"

# kill $OLLAMA_PID