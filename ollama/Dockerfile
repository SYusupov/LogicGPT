FROM ollama/ollama:latest

# Copy Modelfile to the container
COPY Modelfile /Modelfile

# Create the model in the container
RUN ollama create mistral -f /Modelfile

# Run the model when the container starts
CMD ["ollama", "run", "mistral"]
