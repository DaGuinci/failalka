# Development Guide — Failaka

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.10+ | Used in Docker image |
| Node.js | 18+ | For Webpack asset compilation |
| npm | 8+ | Package manager for frontend deps |
| PostgreSQL | 15+ | Primary database |
| Docker & Docker Compose | Latest | For containerized development |
| Git | Latest | Version control |

## Quick Start (Docker — Recommended)

```bash
# Clone the repository
git clone https://github.com/DaGuinci/failalka.git
cd failaka

# Create environment file
cp .dockerenv.example .dockerenv
# Edit .dockerenv with your settings

# Start the application
docker-compose up --build
```

The Docker setup handles everything: migrations, fixtures, asset building, static collection, and starting Gunicorn on port 8000.

**What `scripts/init.sh` does on startup:**
1. Runs `makemigrations --merge` and `migrate --noinput`
2. Runs `python manage.py initdata` (creates groups + loads fixtures in DEBUG mode)
3. Runs `npm run build` (compiles SCSS/JS via Webpack)
4. Runs `collectstatic --noinput` (WhiteNoise static files)
5. Starts Gunicorn with 4 workers on `0.0.0.0:8000`

## Quick Start (Local — Without Docker)

```bash
# Clone and enter project
git clone https://github.com/DaGuinci/failalka.git
cd failaka

# Create and activate virtual environment
python -m venv env
source env/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Create .env file at project root
cat > .env << EOF
SECRET=your-secret-key
DJANGO_ENV=dev
DB_NAME=local-failaka
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=127.0.0.1
DB_PORT=5432
EOF

# Create PostgreSQL database
createdb local-failaka

# Run migrations
python manage.py migrate

# Initialize groups and seed data
python manage.py initdata

# Build frontend assets
npm run build

# Collect static files
python manage.py collectstatic --noinput

# Start development server
python manage.py runserver
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET` | Yes | fallback key | Django secret key |
| `DJANGO_ENV` | No | `prod` | Environment: `dev`, `preprod`, `prod` |
| `DB_NAME` | Yes | — | PostgreSQL database name |
| `DB_USER` | Yes | — | PostgreSQL username |
| `DB_PASSWORD` | Yes | — | PostgreSQL password |
| `DB_HOST` | No | `127.0.0.1` | PostgreSQL host |
| `DB_PORT` | No | `5432` | PostgreSQL port |

## Development Commands

### Django

```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Initialize groups + seed data (DEBUG only)
python manage.py initdata

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run tests
python manage.py test tests
```

### Frontend Assets (Webpack)

```bash
# Production build
npm run build

# Development build
npm run build:dev

# Watch mode (auto-rebuild on change)
npm run watch

# Dev server with hot reload
npm run dev
```

### Docker

```bash
# Start all services
docker-compose up

# Rebuild and start
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f web
```

## Testing

### Test Organization

Tests are located in `tests/tests_api/` and organized by entity:

| File | Tests |
|---|---|
| `tests_data_setup.py` | Shared test setup (users, groups, entities) |
| `tests_authentication.py` | Login/token tests |
| `tests_users.py` | User CRUD + permissions |
| `tests_items.py` | Item CRUD + permissions per role |
| `tests_sites.py` | Site CRUD + permissions per role |
| `tests_subsites.py` | Subsite CRUD + permissions per role |
| `tests_missions.py` | Mission CRUD + permissions per role |
| `tests_notables.py` | Notable CRUD + permissions per role |
| `tests_comments.py` | Comment CRUD + permissions per role |

### Test Setup Pattern

All test classes extend `TestSetupAPITestCase` which provides:
- **Groups**: `admins`, `validators`, `visitors`
- **Users**: `zeus` (superuser), `hera` (admin), `athena` (validator), `hades` (visitor), `ares` (visitor)
- **Entities**: `site_1`, `subsite_1`, sample items

### Running Tests

```bash
# Run all tests
python manage.py test tests

# Run specific test file
python manage.py test tests.tests_api.tests_items

# Run specific test class
python manage.py test tests.tests_api.tests_items.ItemssAPITestCase

# Run with verbosity
python manage.py test tests -v 2
```

### Test Auth Pattern

Tests authenticate using JWT tokens obtained via helper method:

```python
def get_token(self, role):
    url = reverse_lazy('auth_token')
    response = self.client.post(url, {'email': '...', 'password': 'pass'}, format='json')
    return response.json()['access']

# Usage in test
token = self.get_token('admin')
response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {token}')
```

## Code Organization Conventions

### File Naming

- Models: `{entity}_model.py` (e.g., `site_model.py`)
- Views: `{entity}_views.py` (e.g., `site_views.py`)
- Serializers: `{entity}_serializer.py` (e.g., `site_serializer.py`)
- Tests: `tests_{entity}.py` (e.g., `tests_items.py`)
- SCSS components: `_{component}.scss` (e.g., `_buttons.scss`)

### Package Pattern

The `entities` app uses Python packages (directories with `__init__.py`) for models, views, and serializers. Each `__init__.py` re-exports all classes:

```python
# entities/models/__init__.py
from .resource_model import Resource
from .site_model import Site
from .item_model import Item
# ...
```

### ViewSet Pattern

All entity viewsets follow the same structure:

```python
class EntityViewset(ModelViewSet):
    permission_classes = [ResourcePermission]
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    http_method_names = ['get', 'post', 'patch', 'delete']  # No PUT

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

### Serializer Pattern

All entity serializers follow the same structure:

```python
class EntitySerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Entity
        fields = '__all__'
        read_only_fields = ['author']

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.first_name + ' ' + obj.author.last_name
        return None
```
