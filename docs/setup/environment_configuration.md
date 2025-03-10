# Environment Configuration

This guide explains how to configure Langflow using environment variables in the `.env` file.

## Overview

Langflow's Docker setup uses environment variables for configuration. These variables are defined in the `.env` file and are used by Docker Compose to configure the containers.

The setup process automatically creates a `.env` file from the `.env.example` template if it doesn't exist. You can then edit this file to customize your configuration.

## Configuration File

The `.env` file contains several sections of configuration options:

```
# Port Configuration
LANGFLOW_PORT=7860

# Database Configuration
POSTGRES_USER=langflow_user
POSTGRES_PASSWORD=password
POSTGRES_DB=langflow_db

# Langflow Configuration
LANGFLOW_DATABASE_URL=postgresql://langflow_user:password@db:5432/langflow_db
LANGFLOW_COMPONENTS_PATH=/app/custom_components
LANGFLOW_CONFIG_DIR=/app/langflow
LANGFLOW_LOG_LEVEL=info

# Optional: OpenAI API Key
# OPENAI_API_KEY=your_openai_api_key

# Optional: Cache Configuration
# LANGFLOW_CACHE_TYPE=redis
# LANGFLOW_REDIS_URL=redis://redis:6379/0
```

## Available Configuration Options

### Port Configuration

- `LANGFLOW_PORT`: The port Langflow will be accessible on (default: 7860)

### Database Configuration

- `POSTGRES_USER`: PostgreSQL database username (default: langflow_user)
- `POSTGRES_PASSWORD`: PostgreSQL database password (default: password)
- `POSTGRES_DB`: PostgreSQL database name (default: langflow_db)

### Langflow Configuration

- `LANGFLOW_DATABASE_URL`: The connection string for the PostgreSQL database
- `LANGFLOW_COMPONENTS_PATH`: The path to custom components inside the container
- `LANGFLOW_CONFIG_DIR`: The directory where Langflow stores configuration data
- `LANGFLOW_LOG_LEVEL`: The logging level (options: debug, info, warning, error, critical)

### Optional: OpenAI API Key

- `OPENAI_API_KEY`: Your OpenAI API key for using OpenAI components

### Optional: Cache Configuration

- `LANGFLOW_CACHE_TYPE`: The type of cache to use (e.g., redis)
- `LANGFLOW_REDIS_URL`: The connection string for Redis if using Redis cache

## How to Apply Configuration Changes

Different configuration changes require different methods to apply:

### Changes That Require a Restart

These changes take effect after restarting the containers with `make restart`:

- `LANGFLOW_PORT`: Changing the port
- `LANGFLOW_LOG_LEVEL`: Changing the logging level
- `OPENAI_API_KEY`: Adding or changing API keys

Example:
```bash
# Edit the .env file
nano .env

# Restart the containers
make restart
```

### Changes That Require a Full Restart

These changes require stopping the containers, then starting them again:

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: Database credentials
- `LANGFLOW_DATABASE_URL`: Database connection string

Example:
```bash
# Edit the .env file
nano .env

# Stop the containers
make clean

# Start the containers again
make start
```

## Default Values and Fallbacks

The `docker-compose.yml` file includes fallback values for most environment variables. If a variable is not defined in the `.env` file, the fallback value will be used.

For example, the port configuration in `docker-compose.yml` looks like this:
```yaml
ports:
  - "${LANGFLOW_PORT:-7860}:7860"
```

This means that if `LANGFLOW_PORT` is not defined, the default value of `7860` will be used.

## Security Considerations

1. **Database Passwords**: Change the default database password in production environments
2. **API Keys**: Never commit your `.env` file with API keys to version control
3. **Port Exposure**: Consider using a reverse proxy in production environments

## Troubleshooting

If you encounter issues with your configuration:

1. Check the Docker logs: `make logs`
2. Verify that the `.env` file has the correct format
3. Ensure that the values in the `.env` file are valid
4. Try resetting to the default configuration by copying `.env.example` to `.env` 