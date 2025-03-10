# Langflow Docker Documentation

Welcome to the Langflow Docker documentation. This documentation provides comprehensive guides for setting up, configuring, and using Langflow with Docker.

## Overview

Langflow is a UI for LangChain, enabling users to create and prototype LLM applications visually. This Docker setup provides an easy way to run Langflow locally on your machine with proper data persistence and configuration options.

## Documentation Structure

### Setup Guides

- [Installation Guide](setup/installation.md): Step-by-step instructions for installing and setting up Langflow with Docker
- [Environment Configuration](setup/environment_configuration.md): Detailed guide on configuring environment variables
- [Data Persistence and Management](setup/data_persistence.md): Information on data storage, backup, and restore
- [Troubleshooting](setup/troubleshooting.md): Solutions for common issues

### Usage Guides

- [Basic Usage](usage/basic_usage.md): Guide to using Langflow, including creating flows and managing data
- [Custom Components](usage/custom_components.md): Guide to creating and using custom components

## Quick Start

To get started quickly:

1. Clone the repository
2. Run the setup command:
   ```bash
   make setup
   ```
3. Start Langflow:
   ```bash
   make start
   ```
4. Access Langflow at http://localhost:7860 (or the port specified in your `.env` file)

## Available Commands

| Command | Description |
|---------|-------------|
| `make setup` | Prepare the environment for Langflow |
| `make start` | Start the Langflow containers |
| `make stop` | Stop the Langflow containers |
| `make restart` | Restart the Langflow containers |
| `make status` | Check the status of the Langflow containers |
| `make logs` | View the logs of the Langflow containers |
| `make clean` | Stop and remove the Langflow containers |

## Configuration

Langflow can be configured using environment variables in the `.env` file. See the [Environment Configuration](setup/environment_configuration.md) guide for details.

## Data Storage

Langflow stores data in the `./data` directory:
- `./data/langflow`: Langflow configuration and data
- `./data/postgres`: PostgreSQL database files

See the [Data Persistence and Management](setup/data_persistence.md) guide for more information.

## Custom Components

You can extend Langflow with custom components by adding Python files to the `./custom_components` directory. See the [Custom Components](usage/custom_components.md) guide for details.

## Getting Help

If you encounter issues, check the [Troubleshooting](setup/troubleshooting.md) guide. If your issue is not covered, you can:

1. Check the [Langflow Documentation](https://docs.langflow.org)
2. Visit the [Langflow GitHub Repository](https://github.com/langflow-ai/langflow)
3. Search for similar issues in the GitHub issues 