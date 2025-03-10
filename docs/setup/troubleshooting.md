# Troubleshooting Langflow Docker Setup

This guide provides solutions for common issues you might encounter when setting up and running Langflow with Docker.

## Container Issues

### Containers Not Starting

**Symptoms:**
- `make start` command fails
- Containers exit immediately after starting
- `make status` shows containers in an exited state

**Solutions:**

1. **Check Docker Service:**
```bash
# Verify Docker is running
docker info
```

2. **Check Logs:**
```bash
# View logs for all containers
make logs

# View logs for a specific container
docker logs langflow_app
docker logs langflow_db
```

3. **Check Port Conflicts:**
```bash
# Check if port 7860 (or your configured port) is already in use
lsof -i :7860
```

4. **Reset the Setup:**
```bash
make clean
make setup
make start
```

### Database Connection Issues

**Symptoms:**
- Langflow container starts but the web interface shows database errors
- Logs show connection refused errors

**Solutions:**

1. **Check Database Container:**
```bash
# Verify the database container is running
docker ps | grep langflow_db
```

2. **Check Database Logs:**
```bash
docker logs langflow_db
```

3. **Verify Environment Variables:**
Check if the database connection string in `.env` matches the database container configuration:
```bash
cat .env | grep DATABASE
```

4. **Reset Database:**
```bash
make clean
rm -rf ./data/postgres
make setup
make start
```

## Permission Issues

### Volume Mount Permission Errors

**Symptoms:**
- Permission denied errors in logs
- Containers exit with permission-related errors

**Solutions:**

1. **Run Setup Command:**
```bash
make setup
```

2. **Check Initialization Service Logs:**
```bash
docker logs docker_langflow-init-volumes-1
```

3. **Manual Permission Fix:**
```bash
# For macOS/Linux
sudo chown -R $(id -u):$(id -g) ./data
```

### Custom Components Permission Issues

**Symptoms:**
- Custom components not loading
- Permission errors in logs related to custom components

**Solutions:**

1. **Check Permissions:**
```bash
ls -la ./custom_components
```

2. **Fix Permissions:**
```bash
chmod -R 755 ./custom_components
```

## Network Issues

### Cannot Access Langflow Web Interface

**Symptoms:**
- Containers are running but the web interface is not accessible
- Browser shows connection refused or timeout

**Solutions:**

1. **Verify Port Mapping:**
```bash
docker port langflow_app
```

2. **Check Firewall Settings:**
Ensure your firewall allows connections to the Langflow port.

3. **Try Different Browser or Device:**
Sometimes browser caching or network settings can cause issues.

4. **Check Host Network:**
```bash
# For macOS/Linux
ifconfig

# For Windows
ipconfig
```

## Configuration Issues

### Environment Variables Not Applied

**Symptoms:**
- Configuration changes in `.env` file don't take effect
- Langflow uses default values instead of configured ones

**Solutions:**

1. **Verify .env File Format:**
Ensure there are no syntax errors in the `.env` file.

2. **Restart Containers:**
```bash
make restart
```

3. **Check if .env is Being Read:**
```bash
# View environment variables in the container
docker exec langflow_app env | grep LANGFLOW
```

4. **Recreate Containers:**
```bash
make clean
make start
```

### Port Configuration Issues

**Symptoms:**
- Langflow is accessible on a different port than configured
- Port conflicts with other services

**Solutions:**

1. **Check Current Port Mapping:**
```bash
docker port langflow_app
```

2. **Update .env File:**
```bash
# Edit the .env file
nano .env

# Change the port
LANGFLOW_PORT=7861
```

3. **Restart Containers:**
```bash
make restart
```

## Data Persistence Issues

### Data Not Persisting Between Restarts

**Symptoms:**
- Flows disappear after container restarts
- Settings reset to defaults

**Solutions:**

1. **Check Volume Mounts:**
```bash
docker inspect langflow_app | grep Mounts -A 20
```

2. **Verify Data Directories:**
```bash
ls -la ./data
ls -la ./data/postgres
ls -la ./data/langflow
```

3. **Check Docker Compose Configuration:**
Ensure volume mounts are correctly configured in `docker-compose.yml`.

4. **Reset Permissions:**
```bash
make setup
```

## Performance Issues

### Slow Performance

**Symptoms:**
- Langflow UI is slow to respond
- Flow execution takes longer than expected

**Solutions:**

1. **Check Resource Usage:**
```bash
docker stats
```

2. **Increase Docker Resources:**
In Docker Desktop settings, increase CPU and memory allocation.

3. **Check Logs for Errors:**
```bash
make logs
```

4. **Restart Containers:**
```bash
make restart
```

## Update Issues

### Problems After Updating

**Symptoms:**
- Errors after pulling new versions
- Incompatibility issues

**Solutions:**

1. **Clean and Rebuild:**
```bash
make clean
git pull  # If using git repository
make setup
make start
```

2. **Check for Breaking Changes:**
Review the changelog or release notes for any breaking changes.

3. **Backup and Restore Data:**
```bash
# Backup data before updating
cp -r ./data /path/to/backup

# After update, if needed:
make clean
rm -rf ./data
cp -r /path/to/backup/data ./data
make setup
make start
```

## Common Error Messages

### "Error starting userland proxy"

**Cause:** Port conflict with another service.

**Solution:**
Change the port in `.env` file:
```
LANGFLOW_PORT=7861
```

### "Permission denied"

**Cause:** Insufficient permissions for mounted volumes.

**Solution:**
```bash
make setup
```

### "Connection refused to database"

**Cause:** Database container not ready or misconfigured.

**Solution:**
```bash
# Check if database is running
docker ps | grep langflow_db

# Restart containers
make restart
```

### "No space left on device"

**Cause:** Insufficient disk space.

**Solution:**
```bash
# Check disk space
df -h

# Clean Docker system
docker system prune -a
```

## Getting Help

If you're still experiencing issues after trying these solutions:

1. **Check Full Logs:**
```bash
docker logs langflow_app --tail 100
```

2. **Check System Requirements:**
Ensure your system meets the minimum requirements for running Langflow.

3. **Search for Similar Issues:**
Check the Langflow GitHub repository for similar issues and solutions.

4. **Ask for Help:**
Reach out to the Langflow community or create an issue on GitHub with detailed information about your problem, including:
- Error messages
- Steps to reproduce
- System information
- Docker version
- Logs 