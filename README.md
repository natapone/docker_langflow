# Langflow Docker Setup

This repository contains a Docker Compose configuration for running Langflow locally with custom Python packages.

## Prerequisites

- Docker Desktop for Mac installed
- At least 4GB of free RAM
- At least 10GB of free disk space

## Getting Started

1. **Run the setup script:**

```bash
./setup.sh
```

This will:
- Create necessary directories (`custom_components`, `data/langflow`, `data/postgres`)
- Copy `.env.example` to `.env` (if it doesn't exist)

2. **Customize configuration (optional):**

Edit the `.env` file to change settings like port, database credentials, etc.

3. **Start Langflow with Docker Compose:**

```bash
docker compose up -d
```

This will:
- Initialize volume permissions
- Start the PostgreSQL database
- Start the Langflow application with custom Python packages

4. **Check running containers:**

```bash
docker compose ps
```

5. **Access Langflow in your browser:**

```
http://localhost:7860
```
(or the port you specified in your `.env` file)

6. **Stop containers:**

```bash
docker compose down
```

## Python Package Installation

This setup automatically installs the following Python packages when the container starts:
- gspread
- oauth2client
- google-api-python-client
- google-auth
- google-auth-httplib2

To add more packages or modify the existing ones, edit the `command` section in `docker-compose.yml`.

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Installation Guide](docs/setup/installation.md)**: Step-by-step instructions for installing and setting up Langflow
- **[Environment Configuration](docs/setup/environment_configuration.md)**: Detailed guide on configuring environment variables
- **[Data Persistence](docs/setup/data_persistence.md)**: Information on data storage, backup, and restore
- **[Basic Usage](docs/usage/basic_usage.md)**: Guide to using Langflow, including creating flows and managing data
- **[Custom Components](docs/usage/custom_components.md)**: Guide to creating and using custom components
- **[Troubleshooting](docs/setup/troubleshooting.md)**: Solutions for common issues

## Features

- **Custom Python Packages**: Automatically installs required packages at container startup
- **Custom Components Support**: Place your custom components in the `./custom_components` directory
- **PostgreSQL Database**: Uses PostgreSQL for better performance and persistence
- **Persistent Storage**: All data is stored in local directories for easy access and backup
- **Environment Configuration**: Easy configuration via `.env` file

## Configuration

You can configure the setup in two ways:

1. **Using the `.env` file (recommended):**
   - Edit the `.env` file to customize settings
   - Changes take effect after restarting the containers

2. **Directly editing `docker-compose.yml`:**
   - For advanced configurations not covered by environment variables
   - To modify the list of Python packages to install

Common configuration options in `.env`:
- `LANGFLOW_PORT`: The port Langflow will be accessible on (default: 7860)
- `POSTGRES_USER`, `POSTGRES_PASSWORD`: Database credentials
- `LANGFLOW_LOG_LEVEL`: Logging level (debug, info, warning, error, critical)
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI components)

## Data Management

All persistent data is stored in the `./data` directory:
- `./data/langflow`: Contains Langflow data (flows, settings, etc.)
- `./data/postgres`: Contains PostgreSQL database files

This makes it easy to backup, restore, or inspect your data.

## Common Commands

| Command | Description |
|---------|-------------|
| `./setup.sh` | Prepare the environment for Langflow |
| `docker compose up -d` | Start the Langflow containers |
| `docker compose down` | Stop the Langflow containers |
| `docker compose restart` | Restart the Langflow containers |
| `docker compose ps` | Check the status of the Langflow containers |
| `docker compose logs -f` | View the logs of the Langflow containers |

## Troubleshooting

If you encounter any issues:

1. Check container logs:
   ```bash
   docker compose logs -f
   ```

2. Restart the services:
   ```bash
   docker compose restart
   ```

3. Reset everything (this will stop containers but preserve data):
   ```bash
   docker compose down
   docker compose up -d
   ```

4. Permission issues:
   If you encounter permission errors, run:
   ```bash
   docker compose run --rm init-volumes
   ```

5. Verify package installation:
   ```bash
   docker exec langflow_app pip list | grep gspread
   ```

For more detailed troubleshooting information, see the [Troubleshooting Guide](docs/setup/troubleshooting.md).
