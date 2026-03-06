# Data Models — Failaka

## Overview

All domain entities inherit from an abstract `Resource` model that provides common fields. The database uses PostgreSQL with Django ORM. All primary keys are UUIDs.

## Entity Relationship Diagram

```
┌─────────┐       ┌───────────┐
│  User   │◄──────│ Resource  │ (abstract)
│ (auth)  │ author│  uuid PK  │
└─────────┘       │  name     │
                  │  desc     │
                  │  thumbnail│
                  └─────┬─────┘
                        │ extends
        ┌───────┬───────┼───────┬──────────┬──────────┐
        ▼       ▼       ▼       ▼          ▼          ▼
    ┌──────┐ ┌───────┐ ┌────┐ ┌───────┐ ┌────────┐ ┌───────┐
    │ Site │ │Subsite│ │Item│ │Mission│ │Notable │ │Comment│
    └──┬───┘ └───┬───┘ └─┬──┘ └───────┘ └────────┘ └───┬───┘
       │         │       │                              │
       │   FK────┘  FK───┘                         FK───┘
       │  (site)    (site, subsite)                (item)
       │
       └──── M2M ────► Mission
```

## Model Definitions

### Resource (Abstract Base)

| Field | Type | Constraints |
|---|---|---|
| `uuid` | UUIDField | PK, auto-generated, not editable |
| `author` | ForeignKey → User | CASCADE, required |
| `name` | CharField(150) | required |
| `description` | TextField | nullable |
| `thumbnail` | ImageField | nullable, upload to `resources/` |

### User (authentication.User)

| Field | Type | Constraints |
|---|---|---|
| `id` | UUIDField | PK, auto-generated |
| `email` | EmailField | unique, used as USERNAME_FIELD |
| `first_name` | CharField(150) | optional |
| `last_name` | CharField(150) | optional |
| `thumbnail` | ImageField | nullable, upload to `users/` |
| `username` | — | **Removed** (set to None) |

**Notes:**
- Custom `CustomUserManager` for `create_user` / `create_superuser`
- User can belong to only one group at a time (enforced in `save()`)
- `REQUIRED_FIELDS = []` (only email + password needed)

### Site

| Field | Type | Constraints |
|---|---|---|
| `type` | CharField(150) | required |
| `keywords` | JSONField | nullable |
| `chrono` | JSONField | nullable (date range as array) |
| `location` | JSONField | nullable (coordinates as array) |
| `location_name` | CharField(150) | nullable |
| `geology` | CharField(150) | nullable |
| `geo_description` | TextField | nullable |
| `historio` | TextField | nullable |
| `missions` | ManyToManyField → Mission | optional |
| `justification` | TextField | nullable |

### Subsite

| Field | Type | Constraints |
|---|---|---|
| `site` | ForeignKey → Site | CASCADE, required |
| `location` | JSONField | nullable |
| `chrono` | JSONField | nullable |
| `justification` | TextField | nullable |
| `settle_type` | CharField(150) | nullable |
| `material` | CharField(150) | nullable |
| `remains` | TextField | nullable |

### Item

| Field | Type | Constraints |
|---|---|---|
| `type` | CharField(150) | required |
| `identification` | CharField(150) | nullable |
| `site` | ForeignKey → Site | CASCADE, nullable |
| `subsite` | ForeignKey → Subsite | CASCADE, nullable, related_name=`subsite` |
| `item_date` | JSONField | nullable (date range as array) |
| `family` | CharField(150) | nullable |
| `scient_name` | CharField(150) | nullable |
| `material` | CharField(150) | nullable |
| `current_location` | CharField(150) | nullable |
| `references` | TextField | nullable |
| `citation` | TextField | nullable |

### Mission

| Field | Type | Constraints |
|---|---|---|
| `mission_members` | CharField(150) | nullable |
| `type` | CharField(150) | nullable |
| `period` | CharField(150) | nullable |
| `biblio` | TextField | nullable |
| `citation` | TextField | nullable |

### Notable

| Field | Type | Constraints |
|---|---|---|
| `first_name` | CharField(255) | nullable |
| `last_name` | CharField(255) | nullable |

### Comment

| Field | Type | Constraints |
|---|---|---|
| `item` | ForeignKey → Item | CASCADE, related_name=`comments` |
| `status` | CharField(9) | choices: `pending`, `validated`, `rejected`, `deleted`; default: `pending` |

## Key Data Patterns

1. **UUID Primary Keys** — All models use `uuid4()` as primary key, never auto-increment
2. **JSONField Usage** — Complex structured data (coordinates, date ranges, keyword lists) stored as JSON arrays/objects
3. **Cascade Deletes** — All ForeignKey relationships use `CASCADE` on delete
4. **Author is Required** — Every Resource must have an author (enforced at model level)
5. **Single Group per User** — The User `save()` method enforces that a user belongs to at most one group

## Permission Groups

| Group | Created By | Purpose |
|---|---|---|
| `admins` | `initdata` command | Full access to all resources and user management |
| `validators` | `initdata` command | Can create resources and validate comments |
| `visitors` | `initdata` command | Default group for new registrations, read-only + comment submission |

## Fixtures

Development fixtures are loaded via `python manage.py initdata` (only in DEBUG mode):

| Fixture File | Content |
|---|---|
| `initial_data_users.json` | Test users with group assignments |
| `initial_data_missions.json` | Sample missions |
| `initial_data_sites.json` | Sample archaeological sites |
| `initial_data_items.json` | Sample items linked to sites |
| `initial_data_others.json` | Subsites, notables, comments |
