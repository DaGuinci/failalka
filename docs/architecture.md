# Architecture — Failaka

## Executive Summary

Failaka is a layered Django monolith serving as both a REST API and a server-rendered web application. The API layer uses Django REST Framework with JWT authentication and role-based permissions. The presentation layer uses Django templates consuming the API internally via `coreapi`. Frontend assets (SCSS/Bootstrap/jQuery) are compiled via Webpack.

## Architecture Pattern

**Layered Monolith** with the following tiers:

1. **Presentation Layer** — Django templates (server-rendered HTML with Bootstrap)
2. **API Layer** — DRF ModelViewSets exposing RESTful endpoints
3. **Business/Domain Layer** — Django models with abstract `Resource` inheritance
4. **Data Layer** — PostgreSQL via Django ORM

```
┌─────────────────────────────────────────────────┐
│  Client Browser                                 │
│  (HTML + Bootstrap + jQuery)                    │
└──────────┬────────────────────┬─────────────────┘
           │ HTML pages          │ REST API (JSON)
           ▼                    ▼
┌──────────────────┐  ┌──────────────────────────┐
│  client/ app     │  │  DRF ViewSets            │
│  (Django views   │  │  (entities/views/)        │
│   + templates)   │  │  (authentication/views.py)│
│  Uses coreapi    │  │  JWT + Permissions        │
└────────┬─────────┘  └────────┬─────────────────┘
         │                     │
         ▼                     ▼
┌─────────────────────────────────────────────────┐
│  Django ORM                                     │
│  entities/models/ (Resource → Site, Item, etc.) │
│  authentication/models.py (Custom User)         │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
              ┌──────────────┐
              │ PostgreSQL   │
              │ (port 5432)  │
              └──────────────┘
```

## Technology Stack

| Category | Technology | Version | Justification |
|---|---|---|---|
| Language | Python | 3.10 | Mature, well-supported for Django |
| Web Framework | Django | 3.2.25 | LTS release, compatible with PostgreSQL 9.6+ |
| API Framework | Django REST Framework | 3.14.0 | Industry standard for Django REST APIs |
| Auth | djangorestframework-simplejwt | 5.3.0 | Stateless JWT tokens for API auth |
| API Docs | drf-spectacular | 0.26.5 | OpenAPI 3.0 schema generation + Swagger UI |
| Database | PostgreSQL | 15 | Robust relational DB for structured archaeological data |
| WSGI Server | Gunicorn | 23.0.0 | Production-grade Python WSGI server |
| Static Files | WhiteNoise | — | Serves static files without separate web server |
| JS Bundler | Webpack | 5.95.0 | Compiles SCSS and bundles JS/CSS for production |
| CSS Framework | Bootstrap | 5.3.3 | Responsive UI framework |
| CSS Pre-processor | SASS/SCSS | 1.93.2 | Modular CSS with variables, mixins, nesting |
| Icons | Bootstrap Icons | 1.11.3 | Icon font library |
| Tables | Bootstrap Table | 1.24.1 | Enhanced data table component |
| JS Library | jQuery | 3.7.1 | DOM manipulation and AJAX |
| Images | Pillow | 11.2.1 | Image processing for thumbnails |
| Containers | Docker + Docker Compose | — | Consistent dev/prod environments |
| Documentation | Sphinx | 7.1.2 | RST-based project documentation |

## Data Architecture

### Model Inheritance Pattern

All domain entities inherit from an abstract `Resource` base class:

```
Resource (abstract)
├── uuid: UUID (PK, auto-generated)
├── author: FK → User (CASCADE)
├── name: CharField(150)
├── description: TextField (nullable)
└── thumbnail: ImageField (nullable)

Site (extends Resource)
├── type, keywords (JSON), chrono (JSON), location (JSON)
├── location_name, geology, geo_description, historio, justification
└── missions: M2M → Mission

Subsite (extends Resource)
├── site: FK → Site (CASCADE)
├── location (JSON), chrono (JSON), justification
└── settle_type, material, remains

Item (extends Resource)
├── type, identification
├── site: FK → Site, subsite: FK → Subsite
├── item_date (JSON), family, scient_name, material
└── current_location, references, citation

Mission (extends Resource)
├── mission_members, type, period
└── biblio, citation

Notable (extends Resource)
└── first_name, last_name

Comment (extends Resource)
├── item: FK → Item (CASCADE)
└── status: TextChoices (pending/validated/rejected/deleted)
```

### Key Data Patterns

- **UUIDs everywhere** — All models use UUID primary keys (not auto-increment integers)
- **JSONField for complex data** — `chrono`, `location`, `keywords`, `item_date` are stored as JSON
- **Author tracking** — Every resource has a mandatory `author` FK to User
- **Soft status workflow** — Comments use a `status` field (pending → validated/rejected/deleted)

## API Design

### URL Structure

```
/api/auth/token/          → JWT token obtain (POST)
/api/auth/token/refresh/  → JWT token refresh (POST)
/api/users/               → User CRUD (GET, POST, PATCH, DELETE)
/api/users/{id}/add-to-group/  → Assign user to group (POST)
/api/sites/               → Site CRUD
/api/subsites/            → Subsite CRUD
/api/items/               → Item CRUD
/api/missions/            → Mission CRUD
/api/notables/            → Notable CRUD
/api/comments/            → Comment CRUD
/docs/swagger/            → OpenAPI schema (JSON)
/docs/swagger-ui/         → Swagger UI
/docs/redoc/              → ReDoc
```

### API Conventions

- **No PUT** — Only PATCH for partial updates (`http_method_names = ['get', 'post', 'patch', 'delete']`)
- **Author auto-assigned** — `perform_create()` assigns `request.user` as author; `author` field is read-only
- **Computed fields** — Serializers provide `author_name`, `site_name`, `item_name` via `SerializerMethodField`
- **Pagination** — `LimitOffsetPagination` with `PAGE_SIZE = 5`
- **Date format** — API returns dates as `YYYY-MM-DD`

## Authentication & Authorization

### User Model

Custom `User` model extending `AbstractUser`:
- **No username** — Email is the unique identifier (`USERNAME_FIELD = 'email'`)
- **UUID primary key**
- **Single group enforcement** — User can belong to only one group at a time

### Permission Groups

| Group | Capabilities |
|---|---|
| `admins` | Full CRUD on all resources + user management |
| `validators` | Create resources, validate comments |
| `visitors` | Read-only access, submit comments |

### Permission Classes

- **`ResourcePermission`** — Used by all entity viewsets: admins/validators can create, authors can edit/delete their own, anyone can list/retrieve
- **`UserPermission`** — Used by user viewset: admins list users, anyone can register, owners can edit profile

### JWT Configuration

- Access token lifetime: 5 minutes
- Refresh token lifetime: 1 day

## Frontend Architecture

### Template-based Rendering

The `client` app serves HTML pages by consuming the Django API internally using `coreapi`:
- `items_list` — Paginates through all items
- `item_detail` — Shows single item by UUID
- `sites_list` — Lists all sites
- `site_detail` — Shows single site by UUID

### Asset Pipeline

```
src/scss/main.scss ──┐
                     ├──→ Webpack ──→ static/styles.css
assets/js/index.js ──┘              static/bundle.js
                                    static/fonts/
```

SCSS is organized modularly: `utils/` (variables, mixins, overrides), `components/`, `pages/`.

### Base Template

`client/templates/client/base.html` provides the layout:
- Loads `styles.css` (compiled SCSS + Bootstrap)
- Includes header and login form partials
- Loads `bundle.js` (jQuery + Bootstrap JS + custom scripts)

## Testing Strategy

- **Framework**: Django `APITestCase` from DRF
- **Organization**: One test file per entity in `tests/tests_api/`
- **Shared setup**: `TestSetupAPITestCase` in `tests_data_setup.py` creates groups, users (with Greek mythology names), and test data
- **Auth in tests**: JWT tokens obtained per test via helper `get_token(role)` method
- **Coverage**: Tests cover CRUD operations per role (unauthenticated, visitor, validator, admin)

## Deployment Architecture

### Docker (Development)

- `Dockerfile`: Python 3.10-slim + Node 18, installs pip + npm deps
- `docker-compose.yml`: `web` (Django + Gunicorn) + `db` (PostgreSQL 15)
- `scripts/init.sh`: Migrations → fixtures → npm build → collectstatic → Gunicorn (4 workers)

### O2switch (Production)

- Hosted on shared hosting via Passenger WSGI (`cgi-bin/django.py`)
- SFTP deployment via `scripts/deploy-o2switch.sh`
- Static files served by WhiteNoise with `CompressedManifestStaticFilesStorage`
- Environment: `.env` for secrets, `.env.preprod` for staging

### Environment Configuration

- `DJANGO_ENV`: `dev` / `preprod` / `prod`
- `DEBUG` auto-set based on environment
- Database credentials via environment variables (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`)
- `SECRET_KEY` from `SECRET` env var
