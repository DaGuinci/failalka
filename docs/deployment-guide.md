# Deployment Guide — Failaka

## Environments

| Environment | Domain | DJANGO_ENV | DEBUG |
|---|---|---|---|
| Development | `localhost:8000` | `dev` | `True` |
| Pre-production | `failaka.evendev.net` | `preprod` | `True` |
| Production | `failaka.evendev.net` | `prod` | `False` |

## Docker Deployment (Development)

### Docker Compose Services

| Service | Image | Port | Purpose |
|---|---|---|---|
| `web` | Custom (Python 3.10 + Node 18) | `8000:8000` | Django + Gunicorn |
| `db` | `postgres:15` | `5433:5432` | PostgreSQL database |

### Startup Process

`scripts/init.sh` runs on container start:
1. `makemigrations --merge` + `migrate --noinput`
2. `python manage.py initdata` (groups + fixtures in DEBUG)
3. `npm run build` (Webpack compilation)
4. `collectstatic --noinput`
5. Gunicorn: 4 workers, port 8000, 600s timeout, auto-reload

### Environment File

Docker uses `.dockerenv`:
```
SECRET=your-secret-key
DJANGO_ENV=dev
DB_NAME=local-failaka
DB_USER=turist
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432
```

## O2switch Production Deployment

### Hosting Architecture

- **Provider**: O2switch (French shared hosting)
- **WSGI**: Passenger (via `cgi-bin/django.py`)
- **Static files**: WhiteNoise (`CompressedManifestStaticFilesStorage`)
- **Upload method**: SFTP

### Deployment Script

`scripts/deploy-o2switch.sh` automates deployment:

1. **Build assets**: `npm run build`
2. **Collect static files**: `python manage.py collectstatic --noinput`
3. **Create deployment package**: Copies Django apps, config files, sources
4. **Create build script**: For remote asset rebuild on server
5. **Generate version file**: Timestamp + git commit hash
6. **SFTP upload**: Uploads package to server

### Required Environment Variables for Deployment

```bash
export O2SWITCH_SFTP_HOST="failaka.evendev.net"
export O2SWITCH_SFTP_USERNAME="github-deploy"
export O2SWITCH_SFTP_PASSWORD="your_password"
export O2SWITCH_SFTP_PORT=21
```

### Allowed Hosts

- Production: `failaka.evendev.net`, `evendev.net`
- Development: + `localhost`, `127.0.0.1`

### Static Files Configuration

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

WhiteNoise middleware is added after `SecurityMiddleware` to serve compressed static files directly from the Django process.

## CI/CD

The project is hosted on GitHub at `github.com/DaGuinci/failalka`. CI/CD configuration should be set up in `.github/workflows/` (check repository for current state).

## Production Checklist

- [ ] Set `DJANGO_ENV=prod` (ensures `DEBUG=False`)
- [ ] Set strong `SECRET` key
- [ ] Configure PostgreSQL credentials
- [ ] Run `collectstatic --noinput`
- [ ] Verify `ALLOWED_HOSTS` includes production domain
- [ ] Ensure WhiteNoise is in `MIDDLEWARE`
- [ ] Check Gunicorn worker count for server capacity
