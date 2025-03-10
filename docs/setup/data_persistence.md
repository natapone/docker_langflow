# Data Persistence and Management

This guide explains how data is stored and managed in the Langflow Docker setup.

## Overview

Langflow stores data in two main locations:
1. **PostgreSQL database**: Stores flows, components, and other application data
2. **Langflow data directory**: Stores configuration files and custom components

In this Docker setup, both types of data are persisted to local directories on your host machine, ensuring that your data remains available even if containers are stopped or removed.

## Directory Structure

The data is stored in the `./data` directory, which is created during the setup process:

```
docker_langflow/
├── data/
│   ├── langflow/         # Langflow configuration and data
│   │   ├── cache/        # Cache files
│   │   └── logs/         # Log files
│   └── postgres/         # PostgreSQL database files
├── custom_components/    # Custom components directory
└── ...
```

## Data Types

### PostgreSQL Database

The PostgreSQL database stores:
- Saved flows
- User settings
- API keys (encrypted)
- Component configurations

This data is persisted to the `./data/postgres` directory on your host machine.

### Langflow Data

The Langflow data directory stores:
- Configuration files
- Cache files
- Log files

This data is persisted to the `./data/langflow` directory on your host machine.

### Custom Components

Custom components are stored in the `./custom_components` directory on your host machine. This directory is mounted to the Langflow container, making your custom components available to the application.

## Volume Mounts

The Docker Compose configuration uses volume mounts to persist data:

```yaml
volumes:
  - ./data/postgres:/var/lib/postgresql/data
  - ./data/langflow:/app/langflow
  - ./custom_components:/app/custom_components
```

## Backup and Restore

### Backing Up Data

To back up your Langflow data:

1. **Export Flows**: From the Langflow UI, export important flows as JSON files
2. **Back Up the Data Directory**: Copy the entire `./data` directory to a safe location

```bash
# Stop the containers before backup
make stop

# Back up the data directory
cp -r ./data /path/to/backup/location

# Restart the containers
make start
```

### Restoring Data

To restore your Langflow data:

1. **Stop the Containers**:
```bash
make stop
```

2. **Restore the Data Directory**:
```bash
# Remove the existing data directory
rm -rf ./data

# Restore from backup
cp -r /path/to/backup/location/data ./data

# Ensure proper permissions
make setup
```

3. **Start the Containers**:
```bash
make start
```

## Permissions Management

The setup includes an initialization service (`init-volumes`) that ensures proper permissions for the data directories. This service runs before the main Langflow service and sets the correct ownership and permissions.

If you encounter permission issues, you can run:

```bash
make setup
```

This command will reset the permissions on the data directories.

## Cleaning Data

If you need to reset your Langflow instance and remove all data:

```bash
# Stop and remove containers, networks, and volumes
make clean

# Remove the data directory
rm -rf ./data

# Set up a fresh instance
make setup
make start
```

## Troubleshooting

### Database Connection Issues

If Langflow cannot connect to the database:

1. Check if the PostgreSQL container is running:
```bash
make status
```

2. Check the database logs:
```bash
docker logs langflow_db
```

3. Verify that the database credentials in the `.env` file match those in the `docker-compose.yml` file.

### Data Persistence Issues

If your data is not persisting between container restarts:

1. Check if the volume mounts are correctly configured in the `docker-compose.yml` file
2. Verify that the data directories exist and have the correct permissions
3. Check the Docker logs for any volume-related errors:
```bash
make logs
```

### Permission Issues

If you encounter permission errors:

1. Run the setup command to reset permissions:
```bash
make setup
```

2. Check the logs of the initialization service:
```bash
docker logs docker_langflow-init-volumes-1
```

## Best Practices

1. **Regular Backups**: Regularly back up your data directory, especially before updates
2. **Export Important Flows**: Export critical flows as JSON files for additional backup
3. **Monitor Disk Space**: Ensure sufficient disk space for database growth
4. **Secure Access**: Restrict access to the data directories to prevent unauthorized access
5. **Version Control**: Consider using version control for custom components 