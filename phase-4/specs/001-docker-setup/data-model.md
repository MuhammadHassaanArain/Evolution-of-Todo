# Container Architecture: Docker Containerization

**Feature**: Docker Containerization (001-docker-setup)
**Date**: 2026-02-08
**Purpose**: Document the container architecture for the three-service todo application

## Overview

This document describes the container architecture for the phase-4 todo application, which consists of three containerized services: Frontend (Next.js), Backend (FastAPI), and MCP Server (FastMCP). Each service runs in its own isolated container and communicates with others through a Docker bridge network.

## Container Definitions

### Frontend Container

**Base Image**: `node:20-alpine`
**Build Strategy**: Multi-stage (builder + runner)
**Exposed Port**: 3000
**Purpose**: Serves the Next.js web application to users' browsers

**Architecture**:
```
┌─────────────────────────────────────┐
│   Frontend Container (node:20-alpine)│
│                                     │
│   Stage 1: Builder                  │
│   - Install all dependencies        │
│   - Build Next.js application       │
│   - Generate optimized bundles      │
│                                     │
│   Stage 2: Runner                   │
│   - Copy built artifacts            │
│   - Install production deps only    │
│   - Serve with next start           │
│                                     │
│   Port: 3000                        │
│   User: node (non-root)             │
└─────────────────────────────────────┘
```

**Environment Variables**:
- `NEXT_PUBLIC_API_URL`: Backend API URL for browser requests (http://localhost:8000)
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL (http://localhost:8000)
- `NODE_ENV`: Environment mode (production/development)

**Resource Profile**:
- Image Size: <500MB (target)
- Memory: ~200MB runtime
- CPU: Low (mostly I/O bound)
- Startup Time: ~10-15 seconds

**Dependencies**:
- Depends on Backend being healthy before starting
- No direct container-to-container communication (browser makes API calls)

### Backend Container

**Base Image**: `python:3.13-slim`
**Build Strategy**: Single-stage with optimized layer caching
**Exposed Port**: 8000
**Purpose**: Provides REST API for todo operations, authentication, and chat functionality

**Architecture**:
```
┌─────────────────────────────────────┐
│  Backend Container (python:3.13-slim)│
│                                     │
│   - Install system dependencies     │
│   - Install Python packages         │
│   - Copy application code           │
│   - Run FastAPI with uvicorn        │
│                                     │
│   Port: 8000                        │
│   User: appuser (non-root)          │
│                                     │
│   Connections:                      │
│   → Neon PostgreSQL (external)      │
│   → MCP Server (http://mcp-server:8001)│
└─────────────────────────────────────┘
```

**Environment Variables**:
- `DATABASE_URL`: PostgreSQL connection string (Neon)
- `JWT_SECRET`: Secret key for JWT token signing
- `JWT_ALGORITHM`: JWT algorithm (HS256)
- `JWT_EXPIRATION_MINUTES`: Token expiration time (30)
- `API_KEY`: External API key (Gemini)
- `MODEL_NAME`: AI model name (gemini-2.5-flash)
- `MCP_SERVER_URL`: MCP server URL (http://mcp-server:8001/mcp/)
- `ALLOWED_ORIGINS`: CORS allowed origins (*)

**Resource Profile**:
- Image Size: <300MB (target)
- Memory: ~300-400MB runtime
- CPU: Medium (API processing, database queries)
- Startup Time: ~15-20 seconds

**Dependencies**:
- Depends on MCP Server being healthy before starting
- Connects to external Neon PostgreSQL database
- Communicates with MCP Server for task operations

### MCP Server Container

**Base Image**: `python:3.13-slim`
**Build Strategy**: Single-stage with optimized layer caching
**Exposed Port**: 8001
**Purpose**: Provides MCP tools for task management operations

**Architecture**:
```
┌─────────────────────────────────────┐
│ MCP Server Container (python:3.13-slim)│
│                                     │
│   - Install Python packages         │
│   - Copy application code           │
│   - Run FastMCP with uvicorn        │
│                                     │
│   Port: 8001                        │
│   User: appuser (non-root)          │
│                                     │
│   Connections:                      │
│   → Backend API (http://backend:8000)│
└─────────────────────────────────────┘
```

**Environment Variables**:
- `BACKEND_API_URL`: Backend API URL (http://backend:8000)
- `MCP_SERVER_PORT`: Server port (8001)
- `MCP_SERVER_HOST`: Server host (0.0.0.0)

**Resource Profile**:
- Image Size: <300MB (target)
- Memory: ~200-300MB runtime
- CPU: Low (lightweight tool server)
- Startup Time: ~10-15 seconds

**Dependencies**:
- No startup dependencies (starts first)
- Communicates with Backend API for task operations

## Network Architecture

### Docker Network Configuration

**Network Name**: `todo-network`
**Network Type**: Bridge (default)
**Driver**: bridge

**Network Diagram**:
```
┌─────────────────────────────────────────────────────────────┐
│                        Host Machine                          │
│                                                              │
│  Browser ──→ localhost:3000 ──→ Frontend Container          │
│         ──→ localhost:8000 ──→ Backend Container            │
│         ──→ localhost:8001 ──→ MCP Server Container         │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Docker Network (todo-network)             │ │
│  │                                                        │ │
│  │  ┌──────────┐      ┌──────────┐      ┌──────────┐   │ │
│  │  │ Frontend │      │ Backend  │      │   MCP    │   │ │
│  │  │  :3000   │─────→│  :8000   │─────→│  Server  │   │ │
│  │  │          │      │          │      │  :8001   │   │ │
│  │  └──────────┘      └──────────┘      └──────────┘   │ │
│  │                          │                           │ │
│  │                          ↓                           │ │
│  │                  Neon PostgreSQL                     │ │
│  │                    (external)                        │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Service Discovery

**DNS Resolution**:
- Services can reach each other using service names as hostnames
- Docker Compose automatically configures DNS for service discovery
- Example: Backend can reach MCP Server at `http://mcp-server:8001`

**Service Name Mapping**:
| Service Name | Container Hostname | Internal URL | External URL |
|--------------|-------------------|--------------|--------------|
| frontend | frontend | http://frontend:3000 | http://localhost:3000 |
| backend | backend | http://backend:8000 | http://localhost:8000 |
| mcp-server | mcp-server | http://mcp-server:8001 | http://localhost:8001 |

### Port Mapping

**Port Mapping Strategy**: Direct mapping (host:container)
- Frontend: 3000:3000
- Backend: 8000:8000
- MCP Server: 8001:8001

**Rationale**: Simple and predictable for local development. No port conflicts expected.

## Communication Patterns

### 1. Browser → Frontend (HTTP)
- **Protocol**: HTTP
- **Direction**: External → Container
- **URL**: http://localhost:3000
- **Purpose**: User accesses web application

### 2. Browser → Backend (HTTP)
- **Protocol**: HTTP
- **Direction**: External → Container
- **URL**: http://localhost:8000/api/*
- **Purpose**: Frontend makes API calls from browser (client-side)
- **Authentication**: JWT token in Authorization header

### 3. Backend → MCP Server (HTTP)
- **Protocol**: HTTP
- **Direction**: Container → Container
- **URL**: http://mcp-server:8001/mcp/*
- **Purpose**: Backend invokes MCP tools for task operations
- **Authentication**: None (internal communication)

### 4. Backend → PostgreSQL (TCP)
- **Protocol**: PostgreSQL wire protocol (TCP)
- **Direction**: Container → External
- **URL**: postgresql://host:5432/db?sslmode=require
- **Purpose**: Database operations (CRUD, queries)
- **Authentication**: Username/password in connection string

## Volume Strategy

### Development Mode

**Source Code Volumes** (for hot-reload):
```yaml
frontend:
  volumes:
    - ./frontend:/app
    - /app/node_modules  # Anonymous volume to preserve node_modules

backend:
  volumes:
    - ./backend:/app
    - /app/.venv  # Anonymous volume to preserve virtual environment

mcp-server:
  volumes:
    - ./backend/mcp-server:/app
    - /app/.venv  # Anonymous volume to preserve virtual environment
```

**Benefits**:
- Code changes reflected immediately without rebuilding
- Faster development iteration
- Preserves installed dependencies in anonymous volumes

### Production Mode

**No Volumes**: Code is baked into images
- Images are self-contained and portable
- No dependency on host filesystem
- Consistent across environments

## Startup Sequence

### Dependency Chain

```
1. MCP Server starts (no dependencies)
   ↓ (waits for health check)
2. Backend starts (depends on MCP Server healthy)
   ↓ (waits for health check)
3. Frontend starts (depends on Backend healthy)
```

### Health Check Configuration

**MCP Server**:
- Check: `curl -f http://localhost:8001/`
- Interval: 10s
- Start Period: 20s
- Retries: 5

**Backend**:
- Check: `curl -f http://localhost:8000/`
- Interval: 10s
- Start Period: 30s (longer due to database connection)
- Retries: 5

**Frontend**:
- Check: `curl -f http://localhost:3000/`
- Interval: 10s
- Start Period: 40s (longest due to Next.js initialization)
- Retries: 5

### Expected Startup Timeline

```
T+0s:   docker-compose up --build
T+5s:   MCP Server container starts
T+15s:  MCP Server healthy ✓
T+15s:  Backend container starts
T+30s:  Backend healthy ✓ (connected to database)
T+30s:  Frontend container starts
T+50s:  Frontend healthy ✓
T+60s:  All services ready
```

## Security Considerations

### Non-Root Users

All containers run as non-root users:
- **Frontend**: `node` user (UID 1000)
- **Backend**: `appuser` user (UID 1000)
- **MCP Server**: `appuser` user (UID 1000)

**Rationale**: Limits potential damage if container is compromised

### Secrets Management

**Development**:
- Secrets in .env file (excluded from version control)
- .env file excluded from Docker images via .dockerignore

**Production** (future):
- Use Docker secrets or Kubernetes secrets
- Never bake secrets into images

### Network Isolation

- Containers only expose necessary ports
- Internal communication uses Docker network (not exposed to host)
- External database connection uses SSL (sslmode=require)

## Scalability Considerations

### Horizontal Scaling (Future)

**Stateless Services**: All three services are stateless
- Frontend: Can scale to multiple replicas (load balancer needed)
- Backend: Can scale to multiple replicas (shared database)
- MCP Server: Can scale to multiple replicas (stateless tools)

**Database**: External Neon PostgreSQL handles connection pooling

### Resource Limits (Future)

Can add resource limits in docker-compose.yml:
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

## Monitoring and Observability

### Health Endpoints

All services expose health check endpoints:
- Frontend: `GET /` (returns 200 if Next.js is serving)
- Backend: `GET /` (returns 200 with welcome message)
- MCP Server: `GET /` (returns 200 if FastMCP is running)

### Logs

**Access Logs**:
```bash
docker-compose logs -f frontend   # Frontend logs
docker-compose logs -f backend    # Backend logs
docker-compose logs -f mcp-server # MCP Server logs
docker-compose logs -f            # All logs
```

**Log Format**: Standard output (stdout/stderr)
- Docker captures and stores logs
- Can be forwarded to log aggregation systems (future)

## Disaster Recovery

### Container Failure

**Restart Policy**: `on-failure`
- Containers automatically restart if they crash
- Max retries: 3 (configurable)

### Data Persistence

**Database**: External Neon PostgreSQL
- Data persists even if all containers are destroyed
- No data loss on container restart

**Stateless Services**: No local state
- Containers can be destroyed and recreated without data loss

## Summary

The container architecture provides:
- ✅ Isolated, independently deployable services
- ✅ Automatic service discovery via DNS
- ✅ Health-check-based startup ordering
- ✅ Development mode with hot-reload
- ✅ Production-ready with security best practices
- ✅ Scalable and stateless design
- ✅ Simple local development setup (single command)
