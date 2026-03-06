# Failaka — Project Documentation Index

> Digital archiving and public valorization of archaeological resources from the Failaka excavation site, Kuwait.

## Project Overview

- **Type:** Monolith — Django REST Backend with server-rendered templates
- **Primary Language:** Python 3.10
- **Framework:** Django 3.2.25 (LTS) + Django REST Framework 3.14.0
- **Database:** PostgreSQL 15
- **Architecture:** Layered monolith (API + server-rendered frontend)

## Quick Reference

- **Entry Point:** `failaka/settings.py` (config), `failaka/urls.py` (routes)
- **API Base:** `/api/` (DRF ViewSets with JWT auth)
- **Frontend:** Django templates at `/` (Bootstrap 5 + Webpack-compiled SCSS)
- **Auth:** JWT (SimpleJWT) with email-based custom User model
- **Permission Groups:** `admins`, `validators`, `visitors`
- **Tests:** `python manage.py test tests`
- **Dev Server:** `python manage.py runserver` or `docker-compose up`

## Generated Documentation

- [Project Overview](./project-overview.md) — Executive summary, tech stack, domain model
- [Architecture](./architecture.md) — System architecture, patterns, auth, deployment
- [Source Tree Analysis](./source-tree-analysis.md) — Annotated directory structure
- [Data Models](./data-models.md) — Database schema, entity relationships, fixtures
- [API Contracts](./api-contracts.md) — All endpoints, permissions, request/response formats
- [Development Guide](./development-guide.md) — Setup, commands, testing, code conventions
- [Deployment Guide](./deployment-guide.md) — Docker, O2switch, CI/CD, production checklist

## Existing Documentation

- [README.md](../README.md) — Project overview and quick setup
- [Sphinx Documentation](./index.rst) — RST-based documentation (development context, user stories, class diagrams)
  - [Development](./source/development.rst) — Context, user stories, class diagram, class tables
  - [User Manual](./source/use.rst) — Usage instructions
  - [Class Diagram](./source/class_diag.md) — PlantUML class diagram (with PNG)

## Getting Started

### For Development

1. Read [Development Guide](./development-guide.md) for setup instructions
2. Use Docker: `docker-compose up --build` (handles everything)
3. Or set up locally: Python venv + npm install + PostgreSQL

### For Understanding the Codebase

1. Start with [Architecture](./architecture.md) for the big picture
2. Review [Data Models](./data-models.md) for the domain model
3. Check [API Contracts](./api-contracts.md) for all available endpoints
4. Browse [Source Tree](./source-tree-analysis.md) to navigate the code

### For AI-Assisted Development

When using AI agents to implement new features on this project:
1. **Always reference this index** as the starting point for project context
2. **Check [Architecture](./architecture.md)** for patterns to follow (ViewSet pattern, serializer pattern, permission classes)
3. **Check [Data Models](./data-models.md)** before creating new models (must extend `Resource`, use UUID PKs)
4. **Check [API Contracts](./api-contracts.md)** before adding endpoints (no PUT, author auto-assigned, pagination conventions)
5. **Check [Development Guide](./development-guide.md)** for naming conventions and code organization
