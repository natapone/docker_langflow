# Langflow Docker Documentation

Welcome to the Langflow Docker documentation. This documentation provides comprehensive guides for setting up, configuring, and using Langflow with Docker.

## Overview

Langflow is a UI for LangChain, enabling users to create and prototype LLM applications visually. This Docker setup provides an easy way to run Langflow locally with custom Python packages, proper data persistence, and configuration options.

## Documentation Structure

- [Installation Guide](installation.md): Step-by-step instructions for installing and setting up Langflow with Docker
- [Basic Usage](basic_usage.md): Guide to using Langflow, including creating flows and managing data
- [Custom Components](custom_components.md): Guide to creating and using custom components
- [Troubleshooting](troubleshooting.md): Solutions for common issues

## Quick Start

To get started quickly:

1. Clone the repository
2. Run the setup script:
   ```bash
   ./setup.sh
   ```
3. Start Langflow:
   ```bash
   docker compose up -d
   ```
4. Access Langflow at http://localhost:7860 (or the port specified in your `.env` file)

## Available Commands

| Command | Description |
|---------|-------------|
| `./setup.sh` | Prepare the environment for Langflow |
| `docker compose up -d` | Start the Langflow containers |
| `docker compose down` | Stop the Langflow containers |
| `docker compose restart` | Restart the Langflow containers |
| `docker compose ps` | Check the status of the Langflow containers |
| `docker compose logs -f` | View the logs of the Langflow containers |

## Configuration

Langflow can be configured using environment variables in the `.env` file. Common settings include:

- `LANGFLOW_PORT`: The port Langflow will be accessible on (default: 7860)
- `POSTGRES_USER`, `POSTGRES_PASSWORD`: Database credentials
- `LANGFLOW_LOG_LEVEL`: Logging level (debug, info, warning, error, critical)
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI components)

## Custom Python Packages

This setup automatically installs these Python packages:
- gspread
- oauth2client
- google-api-python-client
- google-auth
- google-auth-httplib2

To add or modify packages, edit the `command` section in `docker-compose.yml`.

## Data Storage

Langflow stores data in the `./data` directory:
- `./data/langflow`: Langflow configuration and data
- `./data/postgres`: PostgreSQL database files

## Custom Components

You can extend Langflow with custom components by adding Python files to the `./custom_components` directory. See the [Custom Components](custom_components.md) guide for details.

## Getting Help

If you encounter issues, check the [Troubleshooting](troubleshooting.md) guide. If your issue is not covered, you can:

1. Check the [Langflow Documentation](https://docs.langflow.org)
2. Visit the [Langflow GitHub Repository](https://github.com/langflow-ai/langflow)
3. Search for similar issues in the GitHub issues 