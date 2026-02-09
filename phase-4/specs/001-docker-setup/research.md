# Research: Docker Best Practices for Phase-4 Todo Application

**Feature**: Docker Containerization (001-docker-setup)
**Date**: 2026-02-08
**Purpose**: Research Docker best practices for containerizing Next.js frontend, FastAPI backend, and FastMCP server

## 1. Docker Multi-Stage Builds

### Decision: Use Multi-Stage Build for Frontend

**Rationale**:
- Next.js requires build-time dependencies (webpack, babel, etc.) that are not needed at runtime
- Multi-stage builds separate the build environment from the runtime environment
- Significantly reduces final image size by excluding build tools and intermediate artifacts

**Implementation Pattern**:
```dockerfile
# Stage 1: Builder
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Runner
FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
RUN npm ci --production
CMD ["npm", "start"]
```

**Expected Benefits**:
- Build stage: ~800MB (includes all dev dependencies)
- Runtime stage: ~250-350MB (only production dependencies and built artifacts)
- Savings: ~450-550MB per image

**Alternatives Considered**:
- Single-stage build: Rejected due to large image size (would include all dev dependencies)
- Standalone output mode: Considered but adds complexity; standard multi-stage is sufficient

## 2. Python Docker Best Practices

### Decision: Use python:3.13-slim Base Image

**Rationale**:
- `python:3.13-slim` provides a good balance between size and compatibility
- Includes necessary system libraries for common Python packages (psycopg2, cryptography)
- Alpine variant has known issues with Python packages that use C extensions

**Size Comparison**:
- `python:3.13`: ~1GB (full Debian with all build tools)
- `python:3.13-slim`: ~150MB (minimal Debian with Python)
- `python:3.13-alpine`: ~50MB (Alpine Linux, but compatibility issues)

**Implementation Pattern**:
```dockerfile
FROM python:3.13-slim

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy and install dependencies first (for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

USER appuser

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key Optimizations**:
1. **Layer Caching**: Copy requirements.txt before application code
   - Dependencies change less frequently than code
   - Rebuilds only reinstall dependencies when requirements.txt changes

2. **No Cache Dir**: `pip install --no-cache-dir` reduces image size by ~50MB
   - Pip cache is only useful for repeated installs in the same environment
   - Not needed in Docker images (each build is fresh)

3. **Non-Root User**: Security best practice
   - Limits potential damage if container is compromised
   - Required by many Kubernetes security policies

4. **Clean APT Lists**: `rm -rf /var/lib/apt/lists/*` saves ~20MB
   - APT package lists not needed after installation
   - Can be re-downloaded if needed (rare in containers)

**Alternatives Considered**:
- Alpine: Rejected due to compatibility issues with psycopg2-binary and cryptography
- Full python:3.13: Rejected due to excessive size (1GB vs 150MB)

## 3. Docker Compose Networking

### Decision: Use Bridge Network with Service Discovery

**Rationale**:
- Docker Compose automatically creates a bridge network for all services
- Services can communicate using service names as hostnames (DNS resolution)
- Simplifies configuration (no need to hardcode IP addresses)

**Network Architecture**:
```yaml
services:
  frontend:
    # Accessible as http://frontend:3000 from other containers
    # Accessible as http://localhost:3000 from host
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000  # For browser (client-side)

  backend:
    # Accessible as http://backend:8000 from other containers
    # Accessible as http://localhost:8000 from host
    ports:
      - "8000:8000"
    environment:
      - MCP_SERVER_URL=http://mcp-server:8001  # Container-to-container

  mcp-server:
    # Accessible as http://mcp-server:8001 from other containers
    # Accessible as http://localhost:8001 from host
    ports:
      - "8001:8001"
    environment:
      - BACKEND_API_URL=http://backend:8000  # Container-to-container

networks:
  default:
    name: todo-network
```

**Key Concepts**:
1. **Service Names as Hostnames**: Docker Compose DNS resolves service names to container IPs
2. **Port Mapping**: `host:container` format exposes container ports to host
3. **Internal vs External URLs**:
   - Internal (container-to-container): Use service names (http://backend:8000)
   - External (browser-to-backend): Use localhost (http://localhost:8000)

**Service Dependencies**:
```yaml
services:
  backend:
    depends_on:
      mcp-server:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 10s
      timeout: 5s
      retries: 5

  frontend:
    depends_on:
      backend:
        condition: service_healthy
```

**Benefits**:
- Services start in correct order (MCP → Backend → Frontend)
- Health checks ensure services are ready before dependents start
- Prevents connection errors during startup

**Alternatives Considered**:
- Host network mode: Rejected (less isolation, port conflicts)
- Custom bridge network: Not needed (default is sufficient)
- Links (deprecated): Use service names instead

## 4. Environment Variable Management

### Decision: Use .env File + Docker Compose env_file

**Rationale**:
- Centralizes all environment variables in one place
- Supports different environments (dev, staging, prod) with different .env files
- Keeps secrets out of version control (.env in .gitignore)
- Allows configuration changes without rebuilding images

**Implementation Pattern**:
```yaml
# docker-compose.yml
services:
  backend:
    env_file:
      - .env
    environment:
      # Override or add specific variables
      - MCP_SERVER_URL=http://mcp-server:8001
```

**Environment Variable Precedence** (highest to lowest):
1. Shell environment variables
2. `environment` section in docker-compose.yml
3. `env_file` in docker-compose.yml
4. Dockerfile ENV instructions

**Security Best Practices**:
1. **Never commit .env files**: Add to .gitignore
2. **Provide .env.example**: Template without sensitive values
3. **Exclude from Docker images**: Add .env to .dockerignore
4. **Use secrets for production**: Docker secrets or Kubernetes secrets (future phase)

**.env.example Template**:
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require

# JWT Authentication
JWT_SECRET=change-this-to-a-random-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# API Keys
API_KEY=your-api-key-here
MODEL_NAME=gemini-2.5-flash

# Service URLs (for Docker Compose)
MCP_SERVER_URL=http://mcp-server:8001/mcp/
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# CORS
ALLOWED_ORIGINS=*
```

**Alternatives Considered**:
- Hardcoded in Dockerfile: Rejected (not flexible, security risk)
- Command-line arguments: Rejected (too many variables, not maintainable)
- Config files: Rejected (environment variables are standard for containers)

## 5. Docker Layer Caching Optimization

### Decision: Optimize Layer Order for Maximum Cache Reuse

**Rationale**:
- Docker caches each layer (instruction in Dockerfile)
- Layers are reused if the instruction and all previous instructions haven't changed
- Proper ordering minimizes rebuilds when only code changes

**Optimization Strategy**:

**Frontend (Next.js)**:
```dockerfile
# 1. Base image (rarely changes)
FROM node:20-alpine AS builder

# 2. Working directory (never changes)
WORKDIR /app

# 3. Package files (changes occasionally)
COPY package*.json ./

# 4. Install dependencies (only rebuilds if package*.json changes)
RUN npm ci

# 5. Application code (changes frequently)
COPY . .

# 6. Build (only rebuilds if code or dependencies change)
RUN npm run build
```

**Backend/MCP (Python)**:
```dockerfile
# 1. Base image (rarely changes)
FROM python:3.13-slim

# 2. System dependencies (rarely changes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Working directory (never changes)
WORKDIR /app

# 4. Requirements file (changes occasionally)
COPY requirements.txt .

# 5. Install Python dependencies (only rebuilds if requirements.txt changes)
RUN pip install --no-cache-dir -r requirements.txt

# 6. Application code (changes frequently)
COPY . .
```

**Layer Ordering Principle**:
- Least frequently changing → Most frequently changing
- Base image → System packages → Dependencies → Application code

**.dockerignore Patterns**:
```
# Frontend
node_modules
.next
.git
.env
.env.local
npm-debug.log
README.md
.gitignore

# Backend/MCP
__pycache__
*.pyc
*.pyo
*.pyd
.Python
.venv
venv/
.git
.env
.pytest_cache
*.log
README.md
.gitignore
```

**Expected Performance**:
- First build: 3-5 minutes (download base images, install all dependencies)
- Code-only change: 30-60 seconds (only rebuild from COPY . . onwards)
- Dependency change: 1-2 minutes (reinstall dependencies + rebuild code)

**Alternatives Considered**:
- Copy everything first: Rejected (invalidates cache on every code change)
- BuildKit cache mounts: Considered for future optimization (more complex)

## 6. Health Checks and Readiness

### Decision: Implement HTTP Health Checks for All Services

**Rationale**:
- Ensures services are fully initialized before accepting traffic
- Enables proper startup ordering with depends_on conditions
- Provides visibility into service health for monitoring

**Implementation Pattern**:

**Docker Compose Health Checks**:
```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  mcp-server:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

  frontend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 40s
```

**Health Check Parameters**:
- `test`: Command to run (curl to root endpoint)
- `interval`: Time between checks (10 seconds)
- `timeout`: Max time for check to complete (5 seconds)
- `retries`: Number of consecutive failures before unhealthy (5)
- `start_period`: Grace period during startup (varies by service)

**Startup Order with Health Checks**:
```yaml
services:
  mcp-server:
    # No dependencies, starts first

  backend:
    depends_on:
      mcp-server:
        condition: service_healthy  # Waits for MCP to be healthy

  frontend:
    depends_on:
      backend:
        condition: service_healthy  # Waits for backend to be healthy
```

**Benefits**:
- Prevents "connection refused" errors during startup
- Services start in correct order: MCP → Backend → Frontend
- Docker Compose waits for health checks before starting dependent services

**Alternatives Considered**:
- No health checks: Rejected (race conditions during startup)
- TCP socket checks: Rejected (doesn't verify service is ready, only that port is open)
- Custom health check endpoints: Considered for future (more detailed health info)

## Summary of Decisions

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Frontend Base Image | node:20-alpine | Small size (~40MB), Next.js compatible |
| Backend/MCP Base Image | python:3.13-slim | Balance of size (~150MB) and compatibility |
| Multi-Stage Build | Yes (frontend only) | Reduces frontend image by ~450MB |
| Networking | Bridge with service discovery | Simple, standard, works out of the box |
| Environment Variables | .env file + env_file | Centralized, flexible, secure |
| Layer Caching | Dependencies before code | Minimizes rebuild time (30-60s for code changes) |
| Health Checks | HTTP checks on root endpoints | Ensures proper startup order |
| Non-Root User | Yes (all services) | Security best practice |
| .dockerignore | Comprehensive patterns | Reduces build context, faster builds |

## Implementation Checklist

- [ ] Create frontend Dockerfile with multi-stage build
- [ ] Create backend Dockerfile with python:3.13-slim
- [ ] Create MCP server Dockerfile with python:3.13-slim
- [ ] Create docker-compose.yml with health checks and dependencies
- [ ] Create .dockerignore files for all services
- [ ] Create .env.example template
- [ ] Test individual service builds
- [ ] Test full stack with docker-compose up
- [ ] Verify inter-service communication
- [ ] Validate image sizes (<500MB frontend, <300MB backend/MCP)
- [ ] Test on Windows, macOS, and Linux
- [ ] Document setup in quickstart.md

## References

- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker Compose Networking](https://docs.docker.com/compose/networking/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Next.js Docker Deployment](https://nextjs.org/docs/deployment#docker-image)
- [FastAPI Docker Deployment](https://fastapi.tiangolo.com/deployment/docker/)
