# NM Dividends Backend API

A Django REST Framework API for managing dividend-related content including articles, disclosures, news, and actions.

## Installation Steps

1. Ensure you have Python 3.9+ installed

2. Clone the repository
3. Create a virtual environment:
   ```bash
   virtualenv venv
   ```
4. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   # On Windows: source venv\Scripts\activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Set up environment variables:
   ```bash
   cp .env-example .env
   # Edit .env and set SECRET_KEY and other required variables
   ```
7. Run database migrations:
   ```bash
   python manage.py migrate
   ```
8. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/
- **ReDoc**: http://localhost:8000/redoc/

## Resources API

The Resources API provides content management capabilities with support for articles, disclosures, news, and actions.

### Base URL
```
/api/v1/
```

### Endpoints

#### Resources

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/resources/` | List all resources (public: published only) | No |
| POST | `/resources/` | Create new resource | Yes (Admin/Editor) |
| GET | `/resources/{slug}/` | Get single resource | No |
| PUT | `/resources/{slug}/` | Update resource (full) | Yes (Admin/Editor) |
| PATCH | `/resources/{slug}/` | Update resource (partial) | Yes (Admin/Editor) |
| DELETE | `/resources/{slug}/` | Delete resource | Yes (Admin/Editor) |
| GET | `/resources/categories/` | Get categories with counts | No |

**Query Parameters:**
- `category` - Filter by category (article, disclosure, news, actions)
- `status` - Filter by status (staff only: draft, pending, approved, published, archived)
- `featured` - Filter by featured status (true/false)
- `search` - Full-text search in title and content
- `author` - Filter by author name
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 10, max: 100)

#### Media Files

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/media/` | List media files | Yes (Admin/Editor) |
| POST | `/media/` | Upload new file | Yes (Admin/Editor) |
| GET | `/media/{id}/` | Get file details | Yes (Admin/Editor) |
| DELETE | `/media/{id}/` | Delete file | Yes (Admin/Editor) |

**File Upload Constraints:**
- Allowed types: JPEG, PNG, GIF, WebP
- Max size: 5MB

### Response Format

All API responses follow a consistent wrapper format:

```json
{
  "success": true,
  "message": "Resources retrieved successfully",
  "data": [...],
  "meta": {
    "current_page": 1,
    "per_page": 10,
    "total": 0,
    "total_pages": 0
  }
}
```

## Authentication

The API uses JWT token authentication:
- **Login**: `POST /auth/login/`
- **Refresh**: `POST /api/token/refresh/`
- **Verify**: `POST /api/token/verify/`

Include the token in requests:
```
Authorization: Bearer <token>
```

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
```bash
# Check linting
flake8 .

# Format code
black .
```
