# Implementation Plan: Docker Containerization for Phase-4 Todo Application

**Branch**: `001-docker-setup` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-docker-setup/spec.md`

## Summary

Containerize the three-service architecture (Next.js frontend, FastAPI backend, FastMCP server) to enable developers to start the entire application stack with a single `docker-compose up --build` command. The implementation will create production-ready Dockerfiles for each service, configure inter-service networking, and establish environment-based configuration management following Docker best practices.

**Primary Goal**: Enable local development environment setup in under 5 minutes with zero manual dependency installation.

**Technical Approach**: Use multi-stage Docker builds for optimization, Docker Compose for orchestration, and environment variables for configuration management. Each service will be independently buildable and deployable while maintaining seamless communication through Docker networking.

## Technical Context

**Language/Version**:
- Frontend: Node.js 20+ (for Next.js 16+)
- Backend: Python 3.13+
- MCP Server: Python 3.13+

**Primary Dependencies**:
- Frontend: Next.js 16.1.1, React 19.2.3, TypeScript 5.9.3, Tailwind CSS 4.1.18
- Backend: FastAPI 0.104.1+, SQLModel 0.0.16+, uvicorn 0.24.0+, python-jose, passlib
- MCP Server: FastMCP 0.1.0+, FastAPI 0.128.0+, httpx 0.25.0+

**Storage**: External Neon Serverless PostgreSQL (not containerized)

**Testing**:
- Docker Compose health checks
- Manual verification of service communication
- Image size validation (<500MB frontend, <300MB backend/MCP)

**Target Platform**:
- Development: Docker Desktop on Windows/macOS/Linux
- Production: Container orchestration platforms (Kubernetes - future phase)

**Project Type**: Web application (frontend + backend + MCP server)

**Performance Goals**:
- Initial build: <5 minutes
- Subsequent builds with code changes: <2 minutes (via layer caching)
- Container startup: <30 seconds per service
- All services ready: <60 seconds total

**Constraints**:
- Frontend image: <500MB
- Backend image: <300MB
- MCP Server image: <300MB
- Must work on Windows, macOS, and Linux
- Must support hot-reload for development

**Scale/Scope**:
- 3 services to containerize
- 4 Docker configuration files (3 Dockerfiles + 1 docker-compose.yml)
- 3 .dockerignore files
- Environment variable management for all services

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Analysis

✅ **I. Spec-Driven Development**: Docker setup is specified in `/specs/001-docker-setup/spec.md` with clear requirements and acceptance criteria.

✅ **II. No Manual Coding**: Docker configuration files (Dockerfiles, docker-compose.yml) are infrastructure-as-code, not application business logic. This is permitted as it's configuration and deployment setup, not feature implementation.

✅ **III. Security & User Isolation**: Docker setup maintains existing JWT authentication. No changes to security model. Containers will not expose sensitive credentials.

✅ **IV. Persistent Storage**: Docker setup preserves connection to external Neon PostgreSQL. No changes to data persistence model.

✅ **V. Full-Stack Integration**: Docker orchestrates the existing Next.js frontend, FastAPI backend, and FastMCP server without modifying their integration patterns.

✅ **VI. Clarity First**: Dockerfiles will be well-commented and follow standard patterns. Docker Compose configuration will be organized and readable.

✅ **VII. Future-Compatible Architecture**: Docker setup supports future Kubernetes deployment (Phase V). Container images can be pushed to registries and deployed to orchestration platforms.

✅ **VIII. Test-First Development**: Acceptance criteria defined in spec. Testing approach: verify services start, communicate, and handle failures gracefully.

### Gate Status: ✅ PASSED

No constitution violations. Docker containerization is infrastructure setup that packages existing application code without modifying business logic or architectural principles.

## Project Structure

### Documentation (this feature)

```text
specs/001-docker-setup/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (architectural plan)
├── research.md          # Docker best practices and patterns
├── data-model.md        # Container architecture documentation
├── quickstart.md        # Docker setup and usage guide
├── contracts/           # Docker configuration contracts
│   ├── docker-compose.yml.template
│   ├── frontend.Dockerfile.template
│   ├── backend.Dockerfile.template
│   └── mcp-server.Dockerfile.template
├── checklists/
│   └── requirements.md  # Specification quality checklist (completed)
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
phase-4/
├── docker-compose.yml           # Orchestrates all three services
├── .env.example                 # Template for environment variables
│
├── frontend/
│   ├── Dockerfile               # Next.js production build
│   ├── .dockerignore            # Exclude node_modules, .next, etc.
│   ├── package.json             # Already exists
│   └── [existing frontend code]
│
├── backend/
│   ├── Dockerfile               # FastAPI backend
│   ├── .dockerignore            # Exclude .venv, __pycache__, etc.
│   ├── requirements.txt         # Already exists
│   ├── src/                     # Already exists
│   └── mcp-server/
│       ├── Dockerfile           # FastMCP server
│       ├── .dockerignore        # Exclude .venv, __pycache__, etc.
│       ├── pyproject.toml       # Already exists
│       └── src/                 # Already exists
│
└── specs/001-docker-setup/      # This feature's documentation
```

**Structure Decision**: Web application structure with three containerized services. Docker files are co-located with their respective services for clarity and maintainability. The docker-compose.yml at the root orchestrates all services.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. This section is not applicable.

## Phase 0: Research & Best Practices

### Research Topics

1. **Docker Multi-Stage Builds**
   - Purpose: Reduce final image size by separating build and runtime dependencies
   - Application: Frontend (build stage with npm, runtime stage with minimal Node.js)
   - Expected outcome: Frontend image <500MB

2. **Python Docker Best Practices**
   - Base image selection: python:3.13-slim vs python:3.13-alpine
   - Dependency caching: COPY requirements.txt before COPY src/
   - Non-root user setup for security
   - Expected outcome: Backend/MCP images <300MB each

3. **Docker Compose Networking**
   - Service discovery via DNS (service names as hostnames)
   - Port mapping (host:container)
   - Dependency management (depends_on with health checks)
   - Expected outcome: Services communicate via http://backend:8000, http://mcp-server:8001

4. **Environment Variable Management**
   - .env file loading in Docker Compose
   - Environment variable precedence (compose file vs .env vs shell)
   - Secrets handling (exclude from images via .dockerignore)
   - Expected outcome: Configuration changes without rebuilds

5. **Docker Layer Caching Optimization**
   - Dependency installation before code copy
   - .dockerignore to exclude unnecessary files
   - Build context minimization
   - Expected outcome: Subsequent builds <2 minutes

6. **Health Checks and Readiness**
   - Docker HEALTHCHECK instruction
   - Docker Compose healthcheck configuration
   - Startup dependency ordering
   - Expected outcome: Services start in correct order, ready within 60 seconds

### Research Deliverable

`research.md` will document:
- Chosen base images with rationale
- Multi-stage build strategy for frontend
- Python dependency caching approach
- Docker Compose networking configuration
- Environment variable management pattern
- Layer caching optimization techniques
- Health check implementation approach

## Phase 1: Design & Contracts

### Container Architecture (data-model.md)

Since this is infrastructure, `data-model.md` will document the **container architecture** instead of data entities:

**Container Definitions**:
- **Frontend Container**: Node.js 20-alpine base, multi-stage build (build + runtime), exposes port 3000, environment: NEXT_PUBLIC_API_URL
- **Backend Container**: Python 3.13-slim base, single-stage build, exposes port 8000, environment: DATABASE_URL, JWT_SECRET, API_KEY, MCP_SERVER_URL
- **MCP Server Container**: Python 3.13-slim base, single-stage build, exposes port 8001, environment: BACKEND_API_URL

**Network Architecture**:
- Docker network: `todo-network` (bridge mode)
- Service DNS: frontend, backend, mcp-server
- External access: All ports mapped to host (3000:3000, 8000:8000, 8001:8001)

**Volume Strategy**:
- Development: Mount source code for hot-reload
- Production: No volumes, code baked into images

**Dependency Graph**:
```
Frontend → Backend → MCP Server
         ↓
    Neon PostgreSQL (external)
```

### Docker Configuration Contracts (contracts/ directory)

**File**: `contracts/docker-compose.yml.template`
- Services: frontend, backend, mcp-server
- Networks: todo-network
- Environment: .env file loading
- Health checks: HTTP endpoints for each service
- Restart policies: on-failure

**File**: `contracts/frontend.Dockerfile.template`
- Stage 1 (builder): Install dependencies, build Next.js
- Stage 2 (runner): Copy build artifacts, serve with next start
- User: non-root (node user)
- Port: 3000

**File**: `contracts/backend.Dockerfile.template`
- Single stage: Install Python dependencies, copy source
- User: non-root (appuser)
- Port: 8000
- Command: uvicorn src.main:app --host 0.0.0.0 --port 8000

**File**: `contracts/mcp-server.Dockerfile.template`
- Single stage: Install Python dependencies, copy source
- User: non-root (appuser)
- Port: 8001
- Command: uvicorn src.main:app --host 0.0.0.0 --port 8001

### Quickstart Guide (quickstart.md)

Will include:
1. Prerequisites (Docker, Docker Compose installation)
2. Environment setup (.env file configuration)
3. Build and run commands (`docker-compose up --build`)
4. Verification steps (access frontend, test API)
5. Troubleshooting common issues
6. Development workflow (hot-reload, logs, debugging)
7. Stopping and cleaning up

### Agent Context Update

After Phase 1 completion, run:
```bash
.specify/scripts/bash/update-agent-context.sh claude
```

This will update `.claude/context.md` or `CLAUDE.md` with:
- Docker containerization technology added
- Docker Compose orchestration noted
- Container networking patterns documented

## Key Decisions

### 1. Base Image Selection

**Frontend**: `node:20-alpine`
- Rationale: Alpine variant is smaller (~40MB vs ~300MB for full Node image)
- Trade-off: Some native modules may have compatibility issues, but Next.js works well with Alpine

**Backend/MCP**: `python:3.13-slim`
- Rationale: Slim variant balances size (~150MB) with compatibility
- Trade-off: Alpine has issues with some Python packages (psycopg2, cryptography), slim is more reliable

### 2. Multi-Stage Build Strategy

**Frontend**: Yes (build stage + runtime stage)
- Rationale: Separates build tools (npm, webpack) from runtime, reduces final image size significantly
- Expected savings: ~200MB (build dependencies not needed in final image)

**Backend/MCP**: No (single stage)
- Rationale: Python applications don't have a separate build step like compiled languages
- Optimization: Install dependencies first, then copy code (for layer caching)

### 3. Development vs Production Mode

**Approach**: Single Dockerfile with environment-based behavior
- Development: Mount volumes for hot-reload, use development servers
- Production: Bake code into image, use production servers
- Configuration: Controlled via docker-compose.yml and environment variables

### 4. Service Startup Order

**Strategy**: Use `depends_on` with health checks
- MCP Server starts first (no dependencies)
- Backend starts after MCP Server is healthy
- Frontend starts after Backend is healthy
- Rationale: Prevents connection errors during startup

### 5. Environment Variable Management

**Pattern**: .env file + docker-compose.yml
- .env file: Contains all environment variables (DATABASE_URL, API keys, etc.)
- docker-compose.yml: References .env variables and passes to containers
- .env.example: Template for developers (no sensitive data)
- Security: .env excluded from Docker images via .dockerignore

## Risk Analysis

### Risk 1: Database Connection from Containers

**Issue**: Neon PostgreSQL may not be accessible from Docker containers due to network restrictions.

**Mitigation**:
- Test database connectivity early in implementation
- Ensure DATABASE_URL uses correct SSL mode (sslmode=require)
- Document any required firewall/network configuration

**Fallback**: If Neon is not accessible, document that Docker setup requires VPN or network configuration.

### Risk 2: Image Size Exceeds Targets

**Issue**: Final images may exceed size targets (500MB frontend, 300MB backend/MCP).

**Mitigation**:
- Use Alpine/slim base images
- Multi-stage builds for frontend
- Aggressive .dockerignore patterns
- Remove build caches in Dockerfile

**Fallback**: Document actual sizes and justify if targets cannot be met.

### Risk 3: Hot-Reload Not Working in Development

**Issue**: Volume mounts may not trigger hot-reload on Windows due to file system differences.

**Mitigation**:
- Use polling mode for file watchers (Next.js: WATCHPACK_POLLING=true)
- Document platform-specific configuration
- Test on all three platforms (Windows, macOS, Linux)

**Fallback**: Developers rebuild containers when code changes (slower but reliable).

### Risk 4: Build Time Exceeds 5 Minutes

**Issue**: Initial build may take longer than 5 minutes due to dependency downloads.

**Mitigation**:
- Optimize layer caching (dependencies before code)
- Use Docker BuildKit for parallel builds
- Document expected build times for first vs subsequent builds

**Fallback**: Adjust success criteria to reflect realistic build times.

## Success Metrics

From spec success criteria:

- **SC-001**: ✅ Single command startup in <5 minutes
- **SC-002**: ✅ All services ready within 60 seconds
- **SC-003**: ✅ Inter-service communication verified
- **SC-004**: ✅ Image sizes: frontend <500MB, backend <300MB, MCP <300MB
- **SC-005**: ✅ Stop/restart without data loss
- **SC-006**: ✅ Environment changes without rebuild
- **SC-007**: ✅ Cross-platform compatibility (Windows/macOS/Linux)
- **SC-008**: ✅ Subsequent builds <2 minutes with layer caching

## Next Steps

1. **Phase 0**: Create `research.md` with Docker best practices research
2. **Phase 1**: Create `data-model.md` (container architecture), `contracts/` (Dockerfile templates), `quickstart.md` (setup guide)
3. **Phase 1**: Run agent context update script
4. **Phase 2**: Run `/sp.tasks` to generate implementation tasks
5. **Implementation**: Execute tasks in red-green-refactor cycle
6. **Validation**: Verify all success criteria are met

## Appendix: Environment Variables Reference

### Frontend (.env)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
API_KEY=your-api-key
MODEL_NAME=gemini-2.5-flash
MCP_SERVER_URL=http://mcp-server:8001/mcp/
ALLOWED_ORIGINS=*
```

### MCP Server (.env)
```
BACKEND_API_URL=http://backend:8000
MCP_SERVER_PORT=8001
MCP_SERVER_HOST=0.0.0.0
```

**Note**: In Docker Compose, service names (backend, mcp-server) are used for inter-service communication instead of localhost.
