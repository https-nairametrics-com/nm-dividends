# NM Dividends Backend - Documentation

Complete documentation for the NM Dividends Backend API.

---

## Project Overview

**Project Name:** NM Dividends Backend API  
**Repository:** `https-nairametrics-com/nm-dividends`  
**Framework:** Django 3.2.16 + Django REST Framework  
**Python Version:** 3.9+  
**Database:** PostgreSQL (via dj-database-url)  
**Authentication:** JWT (SimpleJWT)  

---

## Quick Links

| Section | Description |
|---------|-------------|
| [🏗️ Architecture](./architecture/) | System design and data models |
| [🔌 API Reference](./api/) | API documentation and examples |
| [⚙️ Operations](./operations/) | Testing and deployment |
| [🤝 Contributing](./contributing/) | Development workflow |

**Getting Started**
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Configuration](./operations/DEPLOYMENT.md#environment-configuration)

**Architecture & Design**
- [Architecture Overview](./architecture/OVERVIEW.md) - System architecture
- [Data Models](./architecture/DATA_MODELS.md) - Database schema
- [Authentication](./architecture/AUTHENTICATION.md) - Auth flow and permissions

**API Reference**
- [Authentication](./api/AUTHENTICATION.md) - JWT authentication, login, register
- [Results](./api/RESULTS.md) - CSV uploads and data tracking
- [Error Codes](./api/ERROR_CODES.md) - Error handling reference

**Operations**
- [Testing Guide](./operations/TESTING.md) - Testing strategies and examples
- [Deployment Guide](./operations/DEPLOYMENT.md) - Deployment procedures

**Contributing**
- [Development Workflow](./contributing/WORKFLOW.md) - Git workflow
- [Contributing Guide](./contributing/README.md) - How to contribute

---

## Documentation Structure

```
docs/
├── README.md                    # This file - documentation index
├── architecture/                # System design documentation
│   ├── README.md
│   ├── OVERVIEW.md              # High-level architecture
│   ├── DATA_MODELS.md           # Database schema and models
│   └── AUTHENTICATION.md        # Auth flow and permissions
├── api/                         # API documentation
│   ├── README.md
│   ├── AUTHENTICATION.md        # Authentication API reference
│   ├── RESULTS.md               # Results API reference
│   └── ERROR_CODES.md           # Error handling reference
├── operations/                  # Operations guides
│   ├── README.md
│   ├── TESTING.md               # Testing strategies and examples
│   └── DEPLOYMENT.md            # Deployment procedures
└── contributing/                # Contribution guidelines
    ├── README.md
    └── WORKFLOW.md              # Git workflow and conventions
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL (production) or SQLite (development)
- Virtual environment tool (virtualenv or venv)

### Environment Setup

1. **Clone repository**
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

---

## System Overview

### High-Level Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│  Django API │────▶│  PostgreSQL │
│  (React)    │     │   (DRF)     │     │   (Data)    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Main Components

| Component | Purpose | Status |
|-----------|---------|--------|
| `authentication` | User management, JWT auth | **Active** |
| `article` | Content management (articles, news) | **Active** |
| `results` | NM Data CSV uploads | **Active** |
| `resources` | Content management (next-gen) | **In Development** |
| `income` | Income tracking | Disabled |
| `investor` | Investor profiles | Deprecated |
| `investment` | Investment portfolios | Deprecated |
| `comment` | Comment system | Deprecated |
| `contact` | Contact forms | Deprecated |
| `social_auth` | OAuth providers | Deprecated |

---

## API Quick Reference

### Base URL
```
http://localhost:8000/
```

### Authentication
```bash
# Obtain token
POST /api/token/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

### Key Endpoints

| Endpoint | App | Auth | Description |
|----------|-----|------|-------------|
| `/api/token/` | auth | No | Obtain JWT tokens |
| `/auth/register/` | auth | No | Register new user |
| `/auth/login/` | auth | No | Login and get tokens |
| `/article/posts/` | article | No | List articles |
| `/article/posts/<slug>/` | article | No | Get single article |
| `/results/` | results | No | List NMData uploads |
| `/results/upload/` | results | Yes (Admin) | Upload CSV file |

See [Authentication](./api/AUTHENTICATION.md) and [Results](./api/RESULTS.md) for complete reference.

### Interactive Documentation

- **Swagger UI:** http://localhost:8000/
- **ReDoc:** http://localhost:8000/redoc/

---

## Response Format Standardization

We are migrating all endpoints to use a consistent response format:

```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... },
  "meta": { ... }  // For list endpoints
}
```

### Standardization Progress

| App | Status |
|-----|--------|
| article | ✅ Complete (uses standardized responses) |
| authentication | 🔄 In Progress |
| results | ⏳ Pending |

Legacy apps are deprecated and not being standardized.

See [Issue #9 Implementation Plan](../plans/ISSUE_9_IMPLEMENTATION_PLAN.md).

---

## Known Issues & Technical Debt

### Issue #9: Standardized Response & Error Handling ⚠️
- **Status:** Open - In Progress
- **Priority:** P1 (High)
- **Description:** Inconsistent response formats across apps
- **Impact:** Frontend needs to handle multiple error formats

### Legacy Apps (Deprecated)

The following apps are **legacy/deprecated** and maintained for backward compatibility only:

| App | Status | Note |
|-----|--------|------|
| `investor/` | Deprecated | URLs commented out |
| `investment/` | Deprecated | URLs commented out |
| `comment/` | Deprecated | URLs commented out |
| `contact/` | Deprecated | URLs commented out |
| `social_auth/` | Deprecated | URLs commented out |
| `income/` | Disabled | Not in INSTALLED_APPS |

### In Development

| App | Status | Note |
|-----|--------|------|
| `resources/` | In Development | Models ready, API endpoints pending |

---

## Related Documentation

### Implementation Plans
- [API Requirements](../plans/API_REQUIREMENTS.md)
- [Resources API Issues](../plans/RESOURCES_API_ISSUES.md)
- [Issue #9 Implementation Plan](../plans/ISSUE_9_IMPLEMENTATION_PLAN.md)

### External Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## Contributing to Documentation

When updating documentation:

1. **Follow the structure** - Add content to appropriate section
2. **Keep examples tested** - Ensure code examples work
3. **Update dates** - Change "Last Updated" when modifying
4. **Link appropriately** - Cross-reference related docs
5. **Be concise** - Clear and to the point

### Documentation Standards

- Use clear, concise language
- Include code examples where helpful
- Use tables for structured data
- Keep line length reasonable (< 100 chars)

---

*Last Updated: 2026-04-03*
