# API Contracts — Failaka

## Base URL

- **Development**: `http://localhost:8000/api/`
- **Production**: `https://failaka.evendev.net/api/`
- **Swagger UI**: `/docs/swagger-ui/`
- **ReDoc**: `/docs/redoc/`
- **OpenAPI Schema**: `/docs/swagger/` (JSON)

## Authentication

All write operations require JWT authentication. Read operations (list, retrieve) are public.

### Token Endpoints

| Method | Path | Description | Auth Required |
|---|---|---|---|
| POST | `/api/auth/token/` | Obtain JWT access + refresh tokens | No (email + password in body) |
| POST | `/api/auth/token/refresh/` | Refresh access token | No (refresh token in body) |

**Token Lifetimes:**
- Access: 5 minutes
- Refresh: 1 day

**Usage:** `Authorization: Bearer <access_token>`

## API Conventions

- **Pagination**: `LimitOffsetPagination` — responses include `count`, `next`, `previous`, `results`
- **Page size**: 5 items per page (configurable via `?limit=` and `?offset=`)
- **No PUT**: Only PATCH for partial updates
- **Date format**: `YYYY-MM-DD`
- **Author auto-assignment**: `author` field is read-only, set from authenticated user on creation

## User Endpoints

| Method | Path | Description | Auth |
|---|---|---|---|
| GET | `/api/users/` | List all users | Admin, Superuser |
| POST | `/api/users/` | Register new user | Anyone |
| GET | `/api/users/{uuid}/` | Retrieve user profile | Admin, Superuser, Owner |
| PATCH | `/api/users/{uuid}/` | Update user profile | Admin, Superuser, Owner |
| DELETE | `/api/users/{uuid}/` | Delete user | Admin, Superuser, Owner |
| POST | `/api/users/{uuid}/add-to-group/` | Assign user to group | Admin, Superuser |

### Register (POST /api/users/)

**Request Body:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string (unique)",
  "password": "string"
}
```

**Notes:**
- New users automatically assigned to `visitors` group
- Email must be unique
- Cannot self-assign to groups other than `visitors`

### Add to Group (POST /api/users/{uuid}/add-to-group/)

**Request Body:**
```json
{
  "group_name": "admins|validators|visitors"
}
```

## Entity Endpoints (Sites, Subsites, Items, Missions, Notables, Comments)

All entity endpoints follow the same pattern using DRF `ModelViewSet` with `ResourcePermission`.

### Common Pattern

| Method | Path | Description | Auth |
|---|---|---|---|
| GET | `/api/{entity}/` | List all | Anyone |
| POST | `/api/{entity}/` | Create new | Admin, Validator |
| GET | `/api/{entity}/{uuid}/` | Retrieve by UUID | Anyone |
| PATCH | `/api/{entity}/{uuid}/` | Partial update | Admin, Author |
| DELETE | `/api/{entity}/{uuid}/` | Delete | Admin, Author |

### Entity Paths

| Entity | Base Path | Router Basename |
|---|---|---|
| Sites | `/api/sites/` | `site` |
| Subsites | `/api/subsites/` | `subsite` |
| Items | `/api/items/` | `item` |
| Missions | `/api/missions/` | `mission` |
| Notables | `/api/notables/` | `notable` |
| Comments | `/api/comments/` | `comment` |

### Permission Matrix

| Action | Unauthenticated | Visitor | Validator | Admin | Superuser | Author |
|---|---|---|---|---|---|---|
| List | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Retrieve | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create | ❌ | ❌ | ✅ | ✅ | ✅ | — |
| Update (PATCH) | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Delete | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |

### Response Fields

**Common computed fields (via SerializerMethodField):**
- `author_name` — Full name of the resource author
- `site_name` — Name of the related site (on Items)
- `site_uuid` — UUID of the related site (on Items)
- `item_name` — Name of the related item (on Comments)

### Paginated List Response Format

```json
{
  "count": 42,
  "next": "http://host/api/items/?limit=5&offset=5",
  "previous": null,
  "results": [
    {
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "author": "user-uuid",
      "author_name": "John Doe",
      "name": "Resource Name",
      "description": "...",
      "thumbnail": null
    }
  ]
}
```

## Client Routes (Server-Rendered)

| Method | Path | View | Template |
|---|---|---|---|
| GET | `/` | `items_list` | `client/home.html` |
| GET | `/items/{uuid}/` | `item_detail` | `client/item_detail.html` |
| GET | `/sites/` | `sites_list` | `client/sites.html` |
| GET | `/sites/{uuid}/` | `site_detail` | `client/site_detail.html` |

## Documentation Routes

| Method | Path | View | Description |
|---|---|---|---|
| GET | `/docs/swagger/` | `SpectacularAPIView` | OpenAPI 3.0 schema (JSON) |
| GET | `/docs/swagger-ui/` | `SpectacularSwaggerView` | Interactive Swagger UI |
| GET | `/docs/redoc/` | `SpectacularRedocView` | ReDoc documentation |
| GET | `/admin/` | Django Admin | Admin interface |
