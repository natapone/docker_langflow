# Langflow Installation Guide

This guide provides step-by-step instructions for installing and setting up Langflow using Docker with custom Python packages.

## Prerequisites

- Docker Desktop for Mac installed
- At least 4GB of free RAM
- At least 10GB of free disk space

## Installation Steps

### Step 1: Clone the Repository

If you haven't already, clone the repository to your local machine:

```bash
git clone <repository-url>
cd docker_langflow
```

### Step 2: Run the Setup Script

```bash
./setup.sh
```

This script will:
- Create necessary directories (`custom_components`, `data/langflow`, `data/postgres`)
- Copy `.env.example` to `.env` if it doesn't exist

### Step 3: Configure Environment Variables (Optional)

Edit the `.env` file to customize settings:

```bash
nano .env
```

Key settings:
- `LANGFLOW_PORT`: Port to access Langflow (default: 7860)
- `POSTGRES_USER`, `POSTGRES_PASSWORD`: Database credentials
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI components)

### Step 4: Start Langflow

```bash
docker compose up -d
```

This command:
- Initializes volume permissions
- Starts the PostgreSQL database
- Starts the Langflow application with custom Python packages

### Step 5: Verify Installation

Check that the containers are running:

```bash
docker compose ps
```

You should see `langflow_app` and `langflow_db` containers in the "running" state.

### Step 6: Access Langflow

Open your browser and navigate to:

```
http://localhost:7860
```

(or the port you specified in your `.env` file)

## Custom Python Packages

The setup automatically installs these Python packages:
- gspread
- oauth2client
- google-api-python-client
- google-auth
- google-auth-httplib2

To add or modify packages, edit the `command` section in `docker-compose.yml`.

## Data Storage

All persistent data is stored in the `./data` directory:
- `./data/langflow`: Contains Langflow data (flows, settings, etc.)
- `./data/postgres`: Contains PostgreSQL database files

## Common Commands

| Command | Description |
|---------|-------------|
| `./setup.sh` | Prepare the environment |
| `docker compose up -d` | Start containers |
| `docker compose down` | Stop containers |
| `docker compose restart` | Restart containers |
| `docker compose ps` | Check container status |
| `docker compose logs -f` | View container logs |

## Troubleshooting

If you encounter installation issues:

1. Check logs: `docker compose logs -f`
2. Verify volume permissions: `docker compose run --rm init-volumes`
3. Check package installation: `docker exec langflow_app pip list | grep gspread`
4. Restart containers: `docker compose restart`
5. Reset containers (preserves data): `docker compose down && docker compose up -d`

## Next Steps

After successful installation, proceed to [basic usage](basic_usage.md) to learn how to create your first flow. 