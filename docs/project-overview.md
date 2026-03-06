# Project Overview — Failaka

## Executive Summary

Failaka is a digital archiving and public valorization platform for archaeological resources from the Failaka excavation site in Kuwait. It centralizes, preserves, and provides structured access to historical data, excavation reports, images, and metadata.

The platform consists of a Django REST API backend serving archaeological data, a server-rendered frontend using Django templates with Bootstrap, and Swagger/ReDoc API documentation.

## Project Information

| Field | Value |
|---|---|
| **Project Name** | Failaka |
| **Repository** | [github.com/DaGuinci/failalka](https://github.com/DaGuinci/failalka) |
| **Repository Type** | Monolith |
| **Project Type** | Backend (Django REST API with server-rendered templates) |
| **Primary Language** | Python 3.10 |
| **Framework** | Django 3.2.25 (LTS) |
| **API Framework** | Django REST Framework 3.14.0 |
| **Database** | PostgreSQL 15 |
| **Production Host** | O2switch (failaka.evendev.net) |
| **Status** | In development |

## Technology Stack Summary

| Category | Technology | Version |
|---|---|---|
| Language | Python | 3.10 |
| Web Framework | Django | 3.2.25 (LTS) |
| API Framework | Django REST Framework | 3.14.0 |
| Authentication | djangorestframework-simplejwt | 5.3.0 |
| API Documentation | drf-spectacular | 0.26.5 |
| Database | PostgreSQL | 15 |
| WSGI Server | Gunicorn | 23.0.0 |
| Static Files | WhiteNoise | — |
| JS Bundler | Webpack | 5.95.0 |
| CSS Framework | Bootstrap | 5.3.3 |
| CSS Pre-processor | SASS/SCSS | 1.93.2 |
| Icons | Bootstrap Icons | 1.11.3 |
| Tables | Bootstrap Table | 1.24.1 |
| JS Library | jQuery | 3.7.1 |
| Image Processing | Pillow | 11.2.1 |
| Containers | Docker + Docker Compose | — |
| Documentation | Sphinx | 7.1.2 |

## Architecture Type

**Layered monolith** with clear separation between:
- **API Layer** — DRF ViewSets exposing RESTful endpoints
- **Business Layer** — Django models with abstract `Resource` base class
- **Presentation Layer** — Django templates consuming the API via `coreapi`
- **Data Layer** — PostgreSQL with Django ORM

## Domain Model Summary

The core domain revolves around archaeological resources organized as:
- **Site** → **Subsite** → **Item** (hierarchical location model)
- **Mission** (linked to Sites via M2M)
- **Notable** (people associated with missions)
- **Comment** (user contributions on Items, with validation workflow)

All entity models inherit from an abstract `Resource` base class providing UUID primary keys, author tracking, name, description, and thumbnail.

## Links to Detailed Documentation

- [Architecture](./architecture.md)
- [Source Tree Analysis](./source-tree-analysis.md)
- [Data Models](./data-models.md)
- [API Contracts](./api-contracts.md)
- [Development Guide](./development-guide.md)
- [Deployment Guide](./deployment-guide.md)
