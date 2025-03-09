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

2. **Create required directories**

   ```bash
   mkdir -p custom_components
   ```

3. **Configure environment variables (optional)**

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file to customize your configuration if needed.

4. **Start the Docker containers**

   ```bash
   docker compose up -d
   ```

5. **Verify installation**

   Check that the containers are running:

   ```bash
   docker ps
   ```

   You should see two containers running:
   - `langflow_app` - The Langflow application
   - `langflow_db` - The PostgreSQL database

6. **Access Langflow**

   Open your web browser and navigate to:
   ```
   http://localhost:7860
   ```

## Troubleshooting

If you encounter any issues during installation:

1. **Check Docker logs**

   ```bash
   docker logs langflow_app
   ```

2. **Verify Docker resources**

   Ensure Docker has enough resources allocated (memory, CPU) in Docker Desktop preferences.

3. **Reset the setup**

   If you need to start fresh:

   ```bash
   docker compose down -v
   docker compose up -d
   ```

## Next Steps

Once installation is complete, refer to the [Usage Guide](../usage/basic_usage.md) to learn how to use Langflow. 