# Installation Guide

This guide will help you set up Langflow using Docker on your MacBook Pro.

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Docker Desktop for Mac**
   - Download from [Docker's official website](https://www.docker.com/products/docker-desktop)
   - Minimum version: 4.0.0 or higher

2. **System Requirements**
   - macOS 11.0 or newer
   - At least 4GB of RAM allocated to Docker
   - At least 10GB of free disk space

## Installation Steps

1. **Clone or download this repository**

   ```bash
   git clone https://github.com/natapone/docker_langflow.git
   cd docker_langflow
   ```

2. **Run the setup command**

   ```bash
   make setup
   ```

   This will:
   - Create necessary directories (`custom_components`, `data/langflow`, `data/postgres`)
   - Copy `.env.example` to `.env` (if it doesn't exist)

3. **Configure environment variables (optional)**

   Edit the `.env` file to customize your configuration:

   ```bash
   nano .env
   ```

   Key configuration options:
   - `LANGFLOW_PORT`: The port Langflow will be accessible on (default: 7860)
   - `POSTGRES_USER`, `POSTGRES_PASSWORD`: Database credentials
   - `LANGFLOW_LOG_LEVEL`: Logging level (debug, info, warning, error, critical)
   - `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI components)

4. **Start the Docker containers**

   ```bash
   make start
   ```

   This will:
   - Initialize volume permissions
   - Start the PostgreSQL database
   - Start the Langflow application

5. **Verify installation**

   Check that the containers are running:

   ```bash
   make status
   ```

   You should see two containers running:
   - `langflow_app` - The Langflow application
   - `langflow_db` - The PostgreSQL database

6. **Access Langflow**

   Open your web browser and navigate to:
   ```
   http://localhost:7860
   ```
   (or the port you specified in your `.env` file)

## Data Storage

All persistent data is stored in the `./data` directory:
- `./data/langflow`: Contains Langflow data (flows, settings, etc.)
- `./data/postgres`: Contains PostgreSQL database files

This makes it easy to backup, restore, or inspect your data.

## Troubleshooting

If you encounter any issues during installation:

1. **Check Docker logs**

   ```bash
   make logs
   ```

2. **Verify Docker resources**

   Ensure Docker has enough resources allocated (memory, CPU) in Docker Desktop preferences.

3. **Reset the setup**

   If you need to start fresh but keep your data:

   ```bash
   make clean
   make start
   ```

4. **Complete cleanup**

   If you want to remove all data and start from scratch:

   ```bash
   make clean-all
   make setup
   make start
   ```

5. **Permission issues**

   If you encounter permission errors, you can manually fix permissions with:

   ```bash
   docker compose run --rm init-volumes
   ```

## Next Steps

Once installation is complete, refer to the [Usage Guide](../usage/basic_usage.md) to learn how to use Langflow. 