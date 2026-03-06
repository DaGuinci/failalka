# Source Tree Analysis — Failaka

## Directory Structure

```
failaka/                          # Project root
├── manage.py                     # Django management entry point
├── requirements.txt              # Python dependencies
├── package.json                  # Node.js dependencies (frontend build)
├── webpack-config.js             # Webpack bundler configuration
├── Dockerfile                    # Docker image definition (Python 3.10 + Node 18)
├── docker-compose.yml            # Docker Compose (web + postgres services)
├── .env                          # Environment variables (DB credentials, secrets)
├── .env.preprod                  # Pre-production environment config
├── .htaccess                     # Apache config (O2switch hosting)
├── README.md                     # Project overview and setup instructions
│
├── failaka/                      # 🔧 Django project configuration
│   ├── __init__.py
│   ├── settings.py               # ⚡ ENTRY POINT: Django settings (DB, apps, middleware, JWT, DRF)
│   ├── urls.py                   # ⚡ ENTRY POINT: Root URL routing (API + client + docs)
│   ├── wsgi.py                   # WSGI application (Gunicorn entry)
│   └── asgi.py                   # ASGI application (not actively used)
│
├── authentication/               # 🔐 Authentication app
│   ├── models.py                 # Custom User model (email-based, UUID PK)
│   ├── views.py                  # UserViewset (CRUD + add-to-group action)
│   ├── serializers.py            # UserSerializer, RegisterSerializer, UpdateUserSerializer
│   ├── permissions.py            # UserPermission (role-based: admins, visitors)
│   ├── admin.py                  # Django admin registration
│   └── migrations/               # Database migrations
│
├── entities/                     # 📦 Core domain entities app
│   ├── models/                   # Package-based model organization
│   │   ├── __init__.py           # Re-exports all models
│   │   ├── resource_model.py     # 🏗️ Abstract base class (UUID, author, name, desc, thumbnail)
│   │   ├── site_model.py         # Site entity (extends Resource)
│   │   ├── subsite_model.py      # Subsite entity (FK → Site)
│   │   ├── item_model.py         # Item entity (FK → Site, FK → Subsite)
│   │   ├── mission_model.py      # Mission entity (extends Resource)
│   │   ├── notable_model.py      # Notable entity (extends Resource)
│   │   └── comment_model.py      # Comment entity (FK → Item, status workflow)
│   ├── views/                    # Package-based viewset organization
│   │   ├── __init__.py           # Re-exports all viewsets
│   │   ├── site_views.py         # SiteViewset (ModelViewSet)
│   │   ├── subsite_views.py      # SubsiteViewset
│   │   ├── item_views.py         # ItemViewset
│   │   ├── mission_views.py      # MissionViewset
│   │   ├── notable_views.py      # NotableViewset
│   │   └── comment_views.py      # CommentViewset
│   ├── serializers/              # Package-based serializer organization
│   │   ├── __init__.py           # Re-exports all serializers
│   │   ├── site_serializer.py    # SiteSerializer (ModelSerializer)
│   │   ├── subsite_serializer.py
│   │   ├── item_serializer.py    # ItemSerializer (with computed fields)
│   │   ├── mission_serializer.py
│   │   ├── notable_serializer.py
│   │   └── comment_serializer.py # CommentSerializer (with status workflow)
│   ├── permissions.py            # ResourcePermission (admins/validators can create, authors can edit)
│   ├── admin.py                  # Django admin: ItemAdmin (custom), others registered
│   ├── fixtures/                 # JSON fixtures for dev data seeding
│   │   ├── initial_data_users.json
│   │   ├── initial_data_sites.json
│   │   ├── initial_data_items.json
│   │   ├── initial_data_missions.json
│   │   └── initial_data_others.json
│   └── management/commands/
│       └── initdata.py           # Custom command: creates groups + loads fixtures in DEBUG mode
│
├── client/                       # 🖥️ Server-rendered frontend app
│   ├── urls.py                   # Client URL routing (home, item detail, sites, site detail)
│   ├── views.py                  # Function-based views consuming API via coreapi
│   ├── models.py                 # Empty (no client-specific models)
│   └── templates/client/         # Django templates
│       ├── base.html             # Base layout (Bootstrap + Webpack bundle)
│       ├── home.html             # Items listing page
│       ├── item_detail.html      # Single item detail page
│       ├── sites.html            # Sites listing page
│       ├── site_detail.html      # Single site detail page
│       └── partials/             # Template fragments (header, login form)
│
├── assets/                       # 📁 Frontend source assets
│   ├── js/
│   │   ├── index.js              # ⚡ Webpack entry point (imports SCSS + JS)
│   │   ├── jquery.js             # jQuery setup
│   │   ├── login.js              # Login form logic
│   │   └── bootstrap.bundle.min.js.map
│   └── css/                      # (empty — CSS handled via SCSS)
│
├── src/scss/                     # 🎨 SCSS source files
│   ├── main.scss                 # Main SCSS entry (imports all partials)
│   ├── _base.scss                # Base styles
│   ├── utils/
│   │   ├── _variables.scss       # Design tokens and variables
│   │   ├── _bootstrap-overrides.scss  # Bootstrap customizations
│   │   ├── _mixins.scss          # SCSS mixins
│   │   └── _functions.scss       # SCSS functions
│   ├── components/
│   │   ├── _header.scss
│   │   ├── _buttons.scss
│   │   ├── _forms.scss
│   │   ├── _navigation.scss
│   │   ├── _cards.scss
│   │   └── _tables.scss
│   └── pages/
│       └── _home.scss
│
├── static/                       # 📦 Webpack output (compiled assets)
│   ├── bundle.js                 # Compiled JS bundle
│   ├── styles.css                # Compiled CSS
│   └── fonts/                    # Font files (Bootstrap Icons)
│
├── staticfiles/                  # 📦 Django collectstatic output (WhiteNoise)
│
├── tests/                        # 🧪 Test suite
│   └── tests_api/
│       ├── tests_data_setup.py   # Shared test setup (users, groups, fixtures)
│       ├── tests_authentication.py
│       ├── tests_users.py
│       ├── tests_items.py
│       ├── tests_sites.py
│       ├── tests_subsites.py
│       ├── tests_missions.py
│       ├── tests_notables.py
│       └── tests_comments.py
│
├── scripts/                      # 🔧 Operational scripts
│   ├── init.sh                   # Docker init: migrations, fixtures, collectstatic, gunicorn
│   └── deploy-o2switch.sh        # SFTP deployment to O2switch hosting
│
├── docs/                         # 📚 Sphinx documentation
│   ├── index.rst                 # Sphinx doc root
│   ├── conf.py                   # Sphinx configuration
│   ├── source/
│   │   ├── development.rst       # Dev context, user stories, class diagrams
│   │   ├── use.rst               # User manual
│   │   └── class_diag.md         # PlantUML class diagram
│   └── _static/                  # Static assets for docs
│
├── cgi-bin/                      # O2switch CGI scripts
│   ├── django.py                 # Passenger WSGI wrapper
│   └── debug.py                  # Debug endpoint
│
└── resources/                    # Additional resources (images, etc.)
```

## Critical Folders

| Folder | Purpose | Criticality |
|---|---|---|
| `failaka/` | Django project configuration (settings, URLs, WSGI) | 🔴 Critical |
| `authentication/` | Custom User model, JWT auth, role-based permissions | 🔴 Critical |
| `entities/` | All domain models, API viewsets, serializers | 🔴 Critical |
| `entities/models/` | Domain model definitions with abstract Resource base | 🔴 Critical |
| `entities/views/` | DRF ModelViewSet implementations | 🔴 Critical |
| `entities/serializers/` | DRF serializer definitions | 🟡 Important |
| `client/` | Server-rendered frontend templates and views | 🟡 Important |
| `tests/tests_api/` | API test suite with shared setup | 🟡 Important |
| `src/scss/` | SCSS source files (Bootstrap customizations) | 🟢 Standard |
| `assets/js/` | JavaScript source files (minimal) | 🟢 Standard |
| `scripts/` | Deployment and initialization scripts | 🟡 Important |

## Entry Points

| Entry Point | File | Purpose |
|---|---|---|
| Django Management | `manage.py` | CLI entry for migrations, runserver, etc. |
| Django Settings | `failaka/settings.py` | All Django/DRF/JWT configuration |
| URL Routing | `failaka/urls.py` | API routes, auth endpoints, docs, client routes |
| WSGI Application | `failaka/wsgi.py` | Gunicorn entry point |
| Webpack Entry | `assets/js/index.js` | Frontend asset compilation entry |
| Docker Init | `scripts/init.sh` | Container startup (migrate, seed, build, serve) |
