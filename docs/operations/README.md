# Operations Documentation

Deployment, maintenance, and operational procedures.

---

## Documents

| Document | Description |
|----------|-------------|
| [DEPLOYMENT.md](./DEPLOYMENT.md) | Deployment procedures and environment setup |
| [TESTING.md](./TESTING.md) | Testing strategies and examples |

## Deployment

### Heroku (Primary)

```bash
# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-database-url
heroku config:set DEBUG=False

# Deploy
git push heroku staging

# Run migrations
heroku run python manage.py migrate

# Collect static
heroku run python manage.py collectstatic --noinput
```

### Deployment Checklist

- [ ] All environment variables set
- [ ] Migrations run successfully
- [ ] Static files collected
- [ ] Superuser created
- [ ] Allowed hosts configured
- [ ] CORS origins set
- [ ] Health check endpoint responding

## Environment Variables

Required for production:

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Django secret key |
| `DATABASE_URL` | Yes | PostgreSQL connection |
| `DEBUG` | Yes | Set to `False` |
| `EMAIL_HOST_USER` | Yes | SMTP username |
| `EMAIL_HOST_PASSWORD` | Yes | SMTP password |
| `FRONTEND_URL` | Yes | Frontend URL |

## Maintenance

### Database Backups

```bash
# Heroku
heroku pg:backups:capture
heroku pg:backups:download

# Manual PostgreSQL
pg_dump $DATABASE_URL > backup.sql
```

### Log Monitoring

```bash
# Heroku logs
heroku logs --tail

# View recent logs
heroku logs --num 100
```

---

*See [Docs README](../README.md) for full documentation index*
