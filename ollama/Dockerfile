FROM ollama/ollama:latest

# Copy Modelfile to the container
COPY Modelfile /Modelfile

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the entrypoint script to start the app and create the model
ENTRYPOINT ["/entrypoint.sh"]