# Deployment Guide

Deployment procedures and environment configuration.

---

## Environment Configuration

### Required Environment Variables

```bash
# Security
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgres://user:password@host:port/dbname

# Email
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_FROM_USER=noreply@domain.com

# Frontend
FRONTEND_URL=https://your-frontend.com
APP_SCHEME=yourappscheme

# OAuth (optional)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
TWITTER_API_KEY=...
TWITTER_CONSUMER_SECRET=...
SOCIAL_SECRET=...
```

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | - | Django secret key (50+ chars recommended) |
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `DEBUG` | Yes | False | Enable debug mode (always False in production) |
| `EMAIL_HOST_USER` | Yes | - | SMTP email username |
| `EMAIL_HOST_PASSWORD` | Yes | - | SMTP email password |
| `EMAIL_FROM_USER` | Yes | - | From address for emails |
| `FRONTEND_URL` | Yes | - | Frontend application URL |
| `APP_SCHEME` | No | - | Mobile app URL scheme |
| `GOOGLE_CLIENT_ID` | No | - | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | No | - | Google OAuth client secret |

---

## Deployment Targets

### Primary: Heroku

**URL:** `yields-room.herokuapp.com`

#### Heroku Deployment

```bash
# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-database-url
heroku config:set DEBUG=False
heroku config:set EMAIL_HOST_USER=your-email@domain.com
heroku config:set EMAIL_HOST_PASSWORD=your-password
heroku config:set FRONTEND_URL=https://your-frontend.com

# Deploy to staging
git push heroku staging

# Deploy to production
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Collect static files
heroku run python manage.py collectstatic --noinput

# Create superuser
heroku run python manage.py createsuperuser

# View logs
heroku logs --tail
```

#### Heroku Configuration

**Procfile:**
```
web: gunicorn dividends.wsgi
```

**runtime.txt:**
```
python-3.9.18
```

### Frontends

- **Netlify:** Static site hosting
- **Vercel:** Frontend deployment
- **Render:** Alternative hosting

### Custom Domains

- `nairametrix.com`
- `yieldroom.africa`
- `yieldroom.ng`
- `nairametrics.com`

---

## Deployment Checklist

### Pre-Deployment

- [ ] All environment variables set
- [ ] Database URL is correct
- [ ] Email credentials tested
- [ ] Frontend URL configured
- [ ] Secret key is strong (50+ random chars)
- [ ] DEBUG set to False

### Database

- [ ] Migrations run successfully
- [ ] No pending migrations
- [ ] Database backups configured
- [ ] Database indexes created

### Static & Media Files

- [ ] Static files collected
- [ ] Whitenoise configured
- [ ] Media storage configured (S3/Cloudinary for production)
- [ ] File upload limits tested

### Security

- [ ] Allowed hosts configured
- [ ] CORS origins set
- [ ] CSRF trusted origins set
- [ ] HTTPS enforced
- [ ] Secure cookie settings

### Post-Deployment

- [ ] Health check endpoint responding
- [ ] API documentation accessible
- [ ] Admin panel accessible
- [ ] Email sending working
- [ ] OAuth providers configured (if used)
- [ ] Superuser created
- [ ] Error monitoring configured (Sentry recommended)

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD gunicorn dividends.wsgi:application --bind 0.0.0.0:$PORT
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/dividends
      - SECRET_KEY=your-secret-key
      - DEBUG=False
    depends_on:
      - db
    volumes:
      - ./media:/app/media

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=dividends
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Docker Commands

```bash
# Build and run
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static
docker-compose exec web python manage.py collectstatic --noinput
```

---

## Database Operations

### Backups

#### Heroku

```bash
# Create backup
heroku pg:backups:capture

# Download backup
heroku pg:backups:download

# Restore from backup
heroku pg:backups:restore b101
```

#### Manual PostgreSQL

```bash
# Backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore
psql $DATABASE_URL < backup_20260402.sql
```

### Migrations

```bash
# Check for pending migrations
python manage.py showmigrations

# Run migrations
python manage.py migrate

# Create new migration
python manage.py makemigrations <app_name>

# Rollback migration
python manage.py migrate <app_name> <previous_migration>
```

---

## Monitoring & Logging

### Heroku Logs

```bash
# View logs
heroku logs --tail

# View recent logs (last 100 lines)
heroku logs --num 100

# Filter by app
heroku logs --app yields-room --tail
```

### Sentry Integration (Recommended)

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
)
```

### Health Check Endpoint

```bash
# Check if service is healthy
curl https://your-app.herokuapp.com/health/

# Expected response
{"status": "ok"}
```

---

## Troubleshooting

### Common Issues

#### Static Files Not Loading

```bash
# Collect static files
heroku run python manage.py collectstatic --noinput

# Check Whitenoise configuration
# Ensure 'whitenoise.middleware.WhiteNoiseMiddleware' in MIDDLEWARE
```

#### Database Connection Errors

```bash
# Verify DATABASE_URL
heroku config:get DATABASE_URL

# Test connection
heroku pg:psql
```

#### Migration Errors

```bash
# Reset migrations (CAUTION: Data loss)
heroku pg:reset
heroku run python manage.py migrate

# Or rollback specific migration
heroku run python manage.py migrate <app_name> <migration>
```

#### Email Not Sending

```bash
# Check email credentials
heroku config:get EMAIL_HOST_USER
heroku config:get EMAIL_HOST_PASSWORD

# Test email in shell
heroku run python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

---

## SSL/HTTPS

### Heroku SSL

Heroku provides free SSL for `.herokuapp.com` domains. For custom domains:

```bash
# Add SSL certificate (Heroku paid feature)
heroku addons:create ssl:endpoint

# Or use Automated Certificate Management (ACM)
heroku certs:auto:enable
```

### Force HTTPS

```python
# settings.py
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

---

*Last Updated: 2026-04-03*
