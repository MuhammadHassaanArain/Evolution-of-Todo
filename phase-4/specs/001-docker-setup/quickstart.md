# Docker Setup Quickstart Guide

**Feature**: Docker Containerization (001-docker-setup)
**Last Updated**: 2026-02-08

## Overview

This guide will help you set up and run the entire Phase-4 Todo application stack using Docker. With a single command, you'll have the frontend, backend, and MCP server running and communicating with each other.

## Prerequisites

### Required Software

1. **Docker Desktop** (version 20.10 or higher)
   - Windows: [Download Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
   - macOS: [Download Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
   - Linux: [Install Docker Engine](https://docs.docker.com/engine/install/)

2. **Docker Compose** (version 2.0 or higher)
   - Included with Docker Desktop on Windows/macOS
   - Linux: Install separately following [Docker Compose installation guide](https://docs.docker.com/compose/install/)

### Verify Installation

```bash
# Check Docker version
docker --version
# Expected: Docker version 20.10.x or higher

# Check Docker Compose version
docker-compose --version
# Expected: Docker Compose version 2.x.x or higher

# Verify Docker is running
docker ps
# Should show empty list or running containers (no errors)
```

## Initial Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd phase-4
```

### Step 2: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your configuration:
   ```bash
   # Use your preferred text editor
   nano .env
   # or
   code .env
   ```

3. **Required Variables** (update these):
   ```bash
   # Database Configuration
   DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require

   # JWT Authentication
   JWT_SECRET=your-super-secret-key-change-this-in-production
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_MINUTES=30

   # API Keys
   API_KEY=your-api-key-here
   MODEL_NAME=gemini-2.5-flash
   ```

4. **Service URLs** (these are pre-configured for Docker):
   ```bash
   # These should already be set correctly in .env.example
   MCP_SERVER_URL=http://mcp-server:8001/mcp/
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ALLOWED_ORIGINS=*
   ```

### Step 3: Build and Start Services

```bash
# Build images and start all services
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d
```

**Expected Output**:
```
[+] Building 120.5s (45/45) FINISHED
[+] Running 4/4
 ✔ Network todo-network        Created
 ✔ Container todo-mcp-server    Started
 ✔ Container todo-backend       Started
 ✔ Container todo-frontend      Started
```

**Wait Time**: First build takes 3-5 minutes. Subsequent builds take 30-60 seconds.

### Step 4: Verify Services are Running

```bash
# Check container status
docker-compose ps

# Expected output:
# NAME                STATUS              PORTS
# todo-frontend       Up (healthy)        0.0.0.0:3000->3000/tcp
# todo-backend        Up (healthy)        0.0.0.0:8000->8000/tcp
# todo-mcp-server     Up (healthy)        0.0.0.0:8001->8001/tcp
```

### Step 5: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Backend API Docs**: http://localhost:8000/api/docs
- **MCP Server**: http://localhost:8001

## Common Commands

### Starting and Stopping

```bash
# Start services (if already built)
docker-compose up

# Start in background
docker-compose up -d

# Stop services (keeps containers)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes + networks
docker-compose down -v
```

### Rebuilding

```bash
# Rebuild all services
docker-compose build

# Rebuild specific service
docker-compose build frontend

# Rebuild and restart
docker-compose up --build
```

### Viewing Logs

```bash
# View all logs
docker-compose logs

# Follow logs (live updates)
docker-compose logs -f

# View logs for specific service
docker-compose logs frontend
docker-compose logs backend
docker-compose logs mcp-server

# Follow logs for specific service
docker-compose logs -f backend

# View last 100 lines
docker-compose logs --tail=100
```

### Executing Commands in Containers

```bash
# Open shell in backend container
docker-compose exec backend bash

# Run a command in backend container
docker-compose exec backend python -c "print('Hello')"

# Open shell in frontend container
docker-compose exec frontend sh

# Run npm command in frontend
docker-compose exec frontend npm run lint
```

### Inspecting Services

```bash
# View container details
docker-compose ps

# View resource usage
docker stats

# View networks
docker network ls

# Inspect specific container
docker inspect todo-backend
```

## Development Workflow

### Hot-Reload Setup (Optional)

For development with hot-reload, uncomment the volume mounts in `docker-compose.yml`:

```yaml
# Backend service
backend:
  volumes:
    - ./backend:/app
    - /app/.venv

# Frontend service
frontend:
  volumes:
    - ./frontend:/app
    - /app/node_modules
    - /app/.next
```

Then restart services:
```bash
docker-compose down
docker-compose up
```

**Note**: On Windows, you may need to enable file watching polling:
```yaml
frontend:
  environment:
    - WATCHPACK_POLLING=true
```

### Making Code Changes

**With Hot-Reload** (volumes mounted):
1. Edit code in your local editor
2. Changes are automatically reflected in containers
3. Frontend/backend automatically reload

**Without Hot-Reload** (production mode):
1. Edit code in your local editor
2. Rebuild the affected service:
   ```bash
   docker-compose build frontend
   docker-compose up -d frontend
   ```

### Running Tests

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests (if configured)
docker-compose exec frontend npm test
```

## Troubleshooting

### Issue: Port Already in Use

**Error**: `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution**:
```bash
# Find process using the port (example: port 3000)
# Windows
netstat -ano | findstr :3000

# macOS/Linux
lsof -i :3000

# Kill the process or change port in docker-compose.yml
```

### Issue: Services Not Healthy

**Error**: Container shows as "unhealthy" in `docker-compose ps`

**Solution**:
```bash
# Check logs for the unhealthy service
docker-compose logs backend

# Common causes:
# 1. Database connection failed - check DATABASE_URL
# 2. Missing environment variables - check .env file
# 3. Service crashed - check logs for errors

# Restart the service
docker-compose restart backend
```

### Issue: Database Connection Failed

**Error**: `could not connect to server: Connection refused`

**Solution**:
1. Verify DATABASE_URL is correct in `.env`
2. Ensure Neon PostgreSQL is accessible from your network
3. Check SSL mode is set: `?sslmode=require`
4. Test connection manually:
   ```bash
   docker-compose exec backend python -c "from src.database.connection import engine; print(engine)"
   ```

### Issue: Frontend Can't Reach Backend

**Error**: `Failed to fetch` or `Network error` in browser console

**Solution**:
1. Verify backend is running: `docker-compose ps`
2. Check backend logs: `docker-compose logs backend`
3. Verify NEXT_PUBLIC_API_URL in `.env` is `http://localhost:8000`
4. Try accessing backend directly: http://localhost:8000/api/docs

### Issue: Build Fails

**Error**: `failed to solve: process "/bin/sh -c npm ci" did not complete successfully`

**Solution**:
```bash
# Clear Docker build cache
docker builder prune

# Remove all containers and images
docker-compose down
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up
```

### Issue: Out of Disk Space

**Error**: `no space left on device`

**Solution**:
```bash
# Remove unused Docker resources
docker system prune -a --volumes

# Check Docker disk usage
docker system df
```

### Issue: Slow Build on Windows

**Problem**: Builds take 10+ minutes

**Solution**:
1. Ensure WSL 2 backend is enabled in Docker Desktop settings
2. Move project to WSL 2 filesystem (not /mnt/c/)
3. Add exclusions to Windows Defender for Docker directories

## Advanced Usage

### Custom Network Configuration

```bash
# Create custom network
docker network create my-custom-network

# Update docker-compose.yml to use it
networks:
  default:
    external: true
    name: my-custom-network
```

### Resource Limits

Add resource limits to `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Environment-Specific Configurations

```bash
# Use different compose files for different environments
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Use different .env files
docker-compose --env-file .env.staging up
```

## Cleanup

### Remove Everything

```bash
# Stop and remove containers, networks, volumes
docker-compose down -v

# Remove all Docker images for this project
docker images | grep todo | awk '{print $3}' | xargs docker rmi

# Remove all unused Docker resources
docker system prune -a --volumes
```

### Selective Cleanup

```bash
# Remove only containers
docker-compose down

# Remove containers and networks (keep volumes)
docker-compose down

# Remove specific service
docker-compose rm frontend
```

## Performance Tips

1. **Use BuildKit**: Enable Docker BuildKit for faster builds
   ```bash
   export DOCKER_BUILDKIT=1
   docker-compose build
   ```

2. **Layer Caching**: Don't modify Dockerfiles unnecessarily
   - Dependencies are cached when requirements.txt/package.json don't change
   - Code changes only rebuild from COPY . . onwards

3. **Parallel Builds**: Docker Compose builds services in parallel by default

4. **Prune Regularly**: Clean up unused resources weekly
   ```bash
   docker system prune -a
   ```

## Next Steps

- **Production Deployment**: See Kubernetes deployment guide (future phase)
- **CI/CD Integration**: See CI/CD pipeline setup (future phase)
- **Monitoring**: Add Prometheus/Grafana for metrics (future phase)

## Getting Help

- Check logs: `docker-compose logs -f`
- Inspect containers: `docker-compose ps`
- View documentation: `docker-compose --help`
- Report issues: [GitHub Issues](repository-url/issues)

## Summary

**Quick Reference**:
```bash
# First time setup
cp .env.example .env
# Edit .env with your configuration
docker-compose up --build

# Daily usage
docker-compose up          # Start
docker-compose down        # Stop
docker-compose logs -f     # View logs

# Troubleshooting
docker-compose ps          # Check status
docker-compose restart     # Restart all
docker system prune -a     # Clean up
```

**Service URLs**:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- MCP Server: http://localhost:8001

**Expected Performance**:
- First build: 3-5 minutes
- Subsequent builds: 30-60 seconds
- Startup time: <60 seconds
- All services healthy within 1 minute
