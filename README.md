# Langflow Docker Setup

This repository contains a Docker Compose configuration for running Langflow locally on your MacBook Pro.

## Prerequisites

- Docker Desktop for Mac installed
- At least 4GB of free RAM
- At least 10GB of free disk space

## Getting Started

1. **Create required directories and setup environment:**

```bash
make setup
```

This will:
- Create necessary directories (`custom_components`, `data/langflow`, `data/postgres`)
- Copy `.env.example` to `.env` (if it doesn't exist)

2. **Customize configuration (optional):**

Edit the `.env` file to change settings like port, database credentials, etc.

3. **Start Langflow with Docker Compose:**

```bash
make start
```

4. **Check running containers:**

```bash
make status
```

5. **Access Langflow in your browser:**

```
http://localhost:7860
```
(or the port you specified in your `.env` file)

6. **Stop containers:**

```bash
make stop
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Installation Guide](docs/setup/installation.md)**: Step-by-step instructions for installing and setting up Langflow
- **[Environment Configuration](docs/setup/environment_configuration.md)**: Detailed guide on configuring environment variables
- **[Data Persistence](docs/setup/data_persistence.md)**: Information on data storage, backup, and restore
- **[Basic Usage](docs/usage/basic_usage.md)**: Guide to using Langflow, including creating flows and managing data
- **[Custom Components](docs/usage/custom_components.md)**: Guide to creating and using custom components
- **[Troubleshooting](docs/setup/troubleshooting.md)**: Solutions for common issues

For a complete overview of the documentation, see the [Documentation Index](docs/index.md).

## Features

- **Custom Components Support**: Place your custom components in the `./custom_components` directory
- **PostgreSQL Database**: Uses PostgreSQL for better performance and persistence
- **Persistent Storage**: All data is stored in local directories for easy access and backup
- **Automatic Restarts**: Services restart automatically unless manually stopped
- **Permission Management**: Includes a volume initialization service to ensure proper permissions
- **Environment Configuration**: Easy configuration via `.env` file

## Configuration

You can configure the setup in two ways:

1. **Using the `.env` file (recommended):**
   - Copy `.env.example` to `.env` (done automatically by `make setup`)
   - Edit the `.env` file to customize settings
   - Changes take effect after restarting the containers

2. **Directly editing `docker-compose.yml`:**
   - For advanced configurations not covered by environment variables

Common configuration options in `.env`:
- `LANGFLOW_PORT`: The port Langflow will be accessible on (default: 7860)
- `POSTGRES_USER`, `POSTGRES_PASSWORD`: Database credentials
- `LANGFLOW_LOG_LEVEL`: Logging level (debug, info, warning, error, critical)
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI components)

For detailed configuration information, see the [Environment Configuration Guide](docs/setup/environment_configuration.md).

## Data Management

All persistent data is stored in the `./data` directory:
- `./data/langflow`: Contains Langflow data (flows, settings, etc.)
- `./data/postgres`: Contains PostgreSQL database files

This makes it easy to backup, restore, or inspect your data.

For detailed information on data management, see the [Data Persistence Guide](docs/setup/data_persistence.md).

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

## Troubleshooting

If you encounter any issues:

1. Check container logs:
   ```bash
   make logs
   ```

2. Restart the services:
   ```bash
   make restart
   ```

3. Reset everything (this will stop containers but preserve data):
   ```bash
   make clean
   make start
   ```

4. Permission issues:
   If you encounter permission errors, run:
   ```bash
   make setup
   ```

For more detailed troubleshooting information, see the [Troubleshooting Guide](docs/setup/troubleshooting.md).
