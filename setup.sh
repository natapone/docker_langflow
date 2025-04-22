#!/bin/bash
# Simple setup script for Langflow Docker

echo "Setting up Langflow..."

# Create required directories
mkdir -p custom_components data/langflow data/postgres

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env file from .env.example"
else
  echo ".env file already exists, skipping copy"
fi

echo "Setup complete. Edit .env file if needed."
echo "To start Langflow: docker compose up -d"
echo "To view logs: docker compose logs -f"
echo "To stop Langflow: docker compose down" 