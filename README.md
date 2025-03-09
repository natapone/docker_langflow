# Langflow Docker Setup

This repository contains a Docker Compose configuration for running Langflow locally on your MacBook Pro.

## Prerequisites

- Docker Desktop for Mac installed
- At least 4GB of free RAM
- At least 10GB of free disk space

## Getting Started

1. **Create required directories:**

```bash
mkdir -p custom_components
```

2. **Start Langflow with Docker Compose:**

```bash
docker compose up -d
```

3. **Check running containers:**

```bash
docker ps
```

4. **Access Langflow in your browser:**

```
http://localhost:7860
```

5. **Stop containers:**

```bash
docker compose down
```

## Features

- **Custom Components Support**: Place your custom components in the `./custom_components` directory
- **PostgreSQL Database**: Uses PostgreSQL for better performance and persistence
- **Persistent Storage**: All data is stored in Docker volumes for persistence
- **Automatic Restarts**: Services restart automatically unless manually stopped
- **Permission Management**: Includes a volume initialization service to ensure proper permissions

## Configuration

You can modify the `docker-compose.yml` file to change:

- Port mapping (default: 7860)
- Database credentials
- Volume configurations
- Environment variables

## Troubleshooting

If you encounter any issues:

1. Check container logs:
   ```bash
   docker logs langflow_app
   ```

2. Restart the services:
   ```bash
   docker compose restart
   ```

3. Reset everything (this will delete all data):
   ```bash
   docker compose down -v
   docker compose up -d
   ```

4. Permission issues:
   If you encounter permission errors, the setup includes a volume initialization service that should fix most permission issues automatically. If problems persist, you can manually fix permissions with:
   ```bash
   docker compose run --rm init-volumes
   ```
