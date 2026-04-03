# NM Dividends Backend

A Django REST API for user authentication and NM Data CSV uploads.

## Features

- **JWT Authentication** - Secure token-based authentication with SimpleJWT
- **Results API** - CSV data upload and management for NM Data
- **Role-Based Access** - Admin and regular user roles
- **User Management** - Registration, login, email verification, password reset

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL (recommended) or SQLite (development)
- Virtual environment tool (virtualenv or venv)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nm-dividends-backend
   ```

2. **Create and activate virtual environment**
   ```bash
   virtualenv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env-example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at http://localhost:8000/

## API Documentation

Interactive API documentation is available at:

- **Swagger UI:** http://localhost:8000/
- **ReDoc:** http://localhost:8000/redoc/

### Key Endpoints

| Endpoint | Auth | Description |
|----------|------|-------------|
| `POST /api/token/` | No | Obtain JWT tokens |
| `POST /auth/register/` | No | User registration |
| `POST /auth/login/` | No | User login |
| `GET /results/` | No | List NMData uploads |
| `POST /results/upload/` | Yes (Admin) | Upload CSV file |

### Authentication Example

```bash
# Obtain token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Use token
curl http://localhost:8000/auth/loaduser/ \
  -H "Authorization: Bearer <access_token>"
```

## Project Structure

```
nm-dividends-backend/
├── authentication/     # User management, JWT auth (ACTIVE)
├── results/            # NM Data CSV uploads (ACTIVE)
├── article/            # Legacy - deprecated
├── investment/         # Legacy - deprecated
├── investor/           # Legacy - deprecated
├── expenses/           # Legacy - deprecated
├── comment/            # Legacy - deprecated
├── contact/            # Legacy - deprecated
├── social_auth/        # Legacy - deprecated
├── dividends/          # Project settings
├── docs/               # Documentation
├── plans/              # Implementation plans
└── media/              # Uploaded files
```

**Note:** Only `authentication` and `results` apps are active. All other apps are legacy/deprecated.

## Documentation

- **[Documentation Index](./docs/README.md)** - Complete documentation
- **[API Reference](./docs/api/)** - Authentication and Results APIs
- **[Architecture](./docs/architecture/)** - System design and data models
- **[Development Workflow](./docs/contributing/WORKFLOW.md)** - Git workflow

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test authentication
python manage.py test results

# Run with pytest
pytest

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Environment Variables

Key environment variables (see `.env-example` for full list):

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Django secret key |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `EMAIL_HOST_USER` | Yes | SMTP email username |
| `EMAIL_HOST_PASSWORD` | Yes | SMTP email password |
| `FRONTEND_URL` | Yes | Frontend application URL |
| `DEBUG` | No | Enable debug mode (default: False) |

## Deployment

### Heroku (Primary)

```bash
# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-database-url

# Deploy
git push heroku staging

# Run migrations
heroku run python manage.py migrate
```

See [docs/operations/DEPLOYMENT.md](./docs/operations/DEPLOYMENT.md) for full deployment details.

## Contributing

1. Check the [Issues](https://github.com/https-nairametrics-com/nm-dividends/issues) tab
2. Create a branch: `issue-<number>-<description>`
3. Follow [Conventional Commits](https://www.conventionalcommits.org/) format
4. Create PR to `staging` branch

See [docs/contributing/WORKFLOW.md](./docs/contributing/WORKFLOW.md) for detailed workflow.

## License

[Add your license information here]

---

*Last Updated: 2026-04-03*
