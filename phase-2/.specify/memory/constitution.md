<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 2.0.0
Modified principles: I. Spec-Driven Development (expanded), II. No Manual Coding (maintained), III. In-Memory Only (replaced with persistence requirement), IV. Clarity First (maintained), V. Future-Compatible Architecture (updated for web app), VI. Test-First Development (maintained)
Added sections: Security & User Isolation, Full-Stack Integration, Functional Standards, Persistent Storage, Authentication Requirements, Frontend Standards, Backend Standards, Project Purpose, Additional Requirements
Removed sections: III. In-Memory Only (replaced with new principles)
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ✅ reviewed
Follow-up TODOs: None
-->

# Full-Stack Todo Web Application Constitution

## Core Principles

### I. Spec-Driven Development
All code must originate from written specs. Application logic is generated exclusively by Claude Code based on clear, detailed specifications before any implementation work begins. All features must originate from written specs in `/specs`. Claude Code generates all frontend and backend logic.

### II. No Manual Coding
Application logic is generated exclusively by Claude Code. No handwritten business logic is permitted - all features must be implemented through AI-assisted generation from specifications. Human-written application logic is prohibited. Only configuration, documentation, and spec refinements are allowed.

### III. Security & User Isolation
Use Better Auth with JWT for authentication. Each user can only access their own tasks. All API requests must include valid JWT tokens; invalid or missing tokens return `401 Unauthorized`. Backend must not trust frontend session; all verification via JWT. Task ownership enforced on backend for every operation.

### IV. Persistent Storage
Tasks must be stored in Neon Serverless PostgreSQL. Backend uses SQLModel ORM for database interaction. All tasks are user-specific and filtered by authenticated user.

### V. Full-Stack Integration
Frontend: Next.js 16+, TypeScript, Tailwind CSS, responsive and modern UI. Backend: FastAPI REST API with secure endpoints. API endpoints must follow specifications exactly. Frontend communicates via API client with Authorization header.

### VI. Clarity First
Simple, readable, maintainable structure is prioritized over complexity. Code must be easily understood and maintained, with clear naming conventions and type hints throughout.

### VII. Future-Compatible Architecture
The implementation must allow future expansion (Phase III-V). Project structure and conventions must allow future expansion (Phase III-V). Clear folder separation: `/frontend`, `/backend`, `/specs`, `/CLAUDE.md`.

### VIII. Test-First Development
All features must have comprehensive tests written before implementation. Each feature requires dedicated spec and acceptance criteria to ensure proper functionality.

## Project Purpose
Transform the Phase I console app into a modern, multi-user web application with persistent storage, responsive frontend, RESTful APIs, and user authentication, using Spec-Driven Development with Claude Code and Spec-Kit Plus. No manual coding is allowed.

## Functional Standards
All Basic Level features must be implemented for each user:
- Add Task
- View Task List (filterable, sortable)
- Update Task
- Delete Task
- Mark Task Complete/Incomplete

## Additional Requirements
- RESTful API endpoints secured with JWT.
- Frontend communicates via API client with Authorization header.
- Task ownership enforced on backend for every operation.
- UI must be modern, responsive, and user-friendly.

## Technical Standards
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: FastAPI, Python 3.13+, SQLModel ORM
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth + JWT
- Spec-Driven: Claude Code + Spec-Kit Plus
- Project Structure: Monorepo

## Authentication Requirements
- Use Better Auth with JWT for authentication
- All API requests must include valid JWT tokens
- Invalid or missing tokens return `401 Unauthorized`
- Backend must not trust frontend session; all verification via JWT

## Frontend Standards
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Responsive and modern UI
- Modern, responsive, and user-friendly UI
- UI must be responsive across devices

## Backend Standards
- FastAPI REST API with secure endpoints
- SQLModel ORM for database interaction
- RESTful API endpoints secured with JWT
- API endpoints must follow specifications exactly
- Task ownership enforced on backend for every operation

## Specification Rules
- Specs written in Markdown format
- Stored in `/specs/`
- Specs must fully describe behavior before code generation
- Each feature must have acceptance criteria defined
- All API endpoints must follow specifications exactly

## Persistent Storage
- Tasks must be stored in Neon Serverless PostgreSQL
- Backend uses SQLModel ORM for database interaction
- Tasks are stored persistently in Neon PostgreSQL
- All tasks are user-specific and filtered by authenticated user

## Constraints
- ❌ No manual coding of business logic
- ❌ Backend must not trust frontend session; all verification via JWT
- ❌ Frontend must call backend API for all data
- ✅ All tasks are user-specific and filtered by authenticated user
- ✅ UI must be responsive across devices

## Deliverables
Repository must contain:
- `/specs/` with all feature, API, database, and UI specifications
- `/frontend` and `/backend` folders with Claude-generated code
- `CLAUDE.md` (root, frontend, backend)
- `README.md` with setup and run instructions
- Working modern and responsive web application
- Secure REST API enforcing user ownership

## Success Criteria
Phase II is considered successful if:
- All 5 basic features work for authenticated users
- REST API endpoints follow spec and JWT security
- Tasks are stored persistently in Neon PostgreSQL
- Frontend is responsive, user-friendly, and fully functional
- All code is generated via Claude Code, following specs
- Project structure supports future phases (chatbot, Kubernetes, cloud)

## Enforcement
Any violation of this constitution:
- Invalidates the phase
- Requires spec revision and regeneration
- May result in disqualification from hackathon review

## Governance
This constitution supersedes all other development practices. All development work must comply with these principles. Amendments require documentation of the change, approval process, and migration plan if needed. All PRs and reviews must verify compliance with these principles.

**Version**: 2.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2026-01-02