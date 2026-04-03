# Testing Guide

Testing strategies, examples, and best practices.

---

## Test Configuration

- **Framework:** Django Test + Pytest
- **Coverage:** Coverage.py
- **Location:** `conftest.py`, app-level `tests.py` or `tests/` directories

---

## Running Tests

### Basic Commands

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test authentication
python manage.py test results

# Run with pytest
pytest

# Run specific test file
pytest authentication/tests/test_views.py

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Run with verbose output
pytest -v --tb=short
```

### Test Discovery

```bash
# Run tests matching pattern
pytest -k "test_nmdata"

# Run specific test class
pytest results/tests/test_views.py::NMDataViewTest

# Run specific test method
pytest results/tests/test_views.py::NMDataViewTest::test_upload_csv
```

---

## Test Examples

### Model Tests

```python
# results/tests/test_models.py
import pytest
from results.models import NMData

@pytest.mark.django_db
def test_nmdata_slug_auto_generation():
    """Test that slug is auto-generated from name."""
    nmdata = NMData.objects.create(
        name="Test Data",
        data_type="dividends"
    )
    assert nmdata.slug == "test-data"

@pytest.mark.django_db
def test_nmdata_str_representation():
    """Test string representation of NMData."""
    nmdata = NMData.objects.create(
        name="Test Data",
        data_type="dividends"
    )
    assert str(nmdata) == "Test Data"

@pytest.mark.django_db
def test_nmdata_status_choices():
    """Test valid status choices."""
    valid_statuses = ['pending', 'approved', 'disapproved']
    for status in valid_statuses:
        nmdata = NMData.objects.create(
            name=f"Test {status}",
            data_type="dividends",
            status=status
        )
        assert nmdata.status == status
```

### API Tests

```python
# results/tests/test_views.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_list_uploads_public(client):
    """Test that anyone can list NMData uploads."""
    response = client.get('/results/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_upload_requires_auth(client):
    """Test that uploading CSV requires authentication."""
    response = client.post('/results/upload/')
    assert response.status_code == 401

@pytest.mark.django_db
def test_upload_requires_admin(admin_user, client):
    """Test that only admin can upload CSV."""
    refresh = RefreshToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    # Test upload with admin user
    # Note: Actual test would include file upload
    response = client.post('/results/upload/')
    
    # Assert based on actual implementation
    assert response.status_code in [201, 400]  # 400 if missing file

@pytest.mark.django_db
def test_filter_uploads_by_data_type(client):
    """Test filtering NMData by data_type."""
    from results.models import NMData
    # Create uploads with different data types
    NMData.objects.create(name="Data 1", data_type="dividends", status="approved")
    NMData.objects.create(name="Data 2", data_type="results", status="approved")
    
    response = client.get('/results/?data_type=dividends')
    assert response.status_code == 200

### Authentication Tests

```python
# authentication/tests/test_views.py
import pytest
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_user_registration(client):
    """Test successful user registration."""
    response = client.post('/auth/register/', {
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'TestPass123!',
        'firstname': 'Test',
        'lastname': 'User'
    })
    
    assert response.status_code == 201
    assert response.data['status'] == 'success'
    assert response.data['data']['email'] == 'test@example.com'

@pytest.mark.django_db
def test_user_login(client, user):
    """Test successful user login."""
    user.set_password('testpass123')
    user.save()
    
    response = client.post('/auth/login/', {
        'email': user.email,
        'password': 'testpass123'
    })
    
    assert response.status_code == 200
    assert 'tokens' in response.data
    assert 'access' in response.data['tokens']
    assert 'refresh' in response.data['tokens']

@pytest.mark.django_db
def test_duplicate_email_registration(client, user):
    """Test registration with duplicate email."""
    response = client.post('/auth/register/', {
        'email': user.email,  # Already exists
        'username': 'newuser',
        'password': 'TestPass123!'
    })
    
    assert response.status_code == 400
    assert 'email' in response.data.get('errors', {})
```

### Fixture Examples

```python
# conftest.py
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from results.models import NMData

User = get_user_model()

@pytest.fixture
def client():
    """Return API client."""
    return APIClient()

@pytest.fixture
def user(db):
    """Create a regular user."""
    return User.objects.create_user(
        email='user@example.com',
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(
        email='admin@example.com',
        username='adminuser',
        password='adminpass123'
    )

@pytest.fixture
def editor_user(db):
    """Create an editor user (staff)."""
    user = User.objects.create_user(
        email='editor@example.com',
        username='editoruser',
        password='editorpass123'
    )
    user.is_staff = True
    user.save()
    return user

@pytest.fixture
def auth_client(client, user):
    """Return authenticated client."""
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client
```

---

## Manual Testing Checklist

Use this checklist when testing manually via API client (Postman, curl, etc.):

### Authentication

- [ ] POST /auth/register/ - Creates user with valid data
- [ ] POST /auth/register/ - Returns 400 for duplicate email
- [ ] POST /auth/register/ - Returns 400 for invalid email format
- [ ] POST /auth/register/ - Returns 400 for weak password
- [ ] POST /auth/login/ - Returns tokens for valid credentials
- [ ] POST /auth/login/ - Returns 401 for invalid credentials
- [ ] POST /auth/login/ - Returns 403 for unverified email
- [ ] GET /auth/user/ - Returns user data with valid token
- [ ] GET /auth/user/ - Returns 401 without token
- [ ] GET /auth/user/ - Returns 401 with expired token
- [ ] POST /auth/logout/ - Successfully logs out user
- [ ] POST /auth/request-reset-email/ - Sends reset email
- [ ] PATCH /auth/password-reset-complete/ - Resets password with valid token

### Results (Public)

- [ ] GET /results/ - Returns list without auth
- [ ] GET /results/ - Supports pagination
- [ ] GET /results/ - Supports filtering by name
- [ ] GET /results/ - Supports filtering by data_type
- [ ] GET /results/ - Supports filtering by company (searches in json_data)
- [ ] GET /results/ - Supports sorting by upload_date
- [ ] GET /results/ - Returns 404 for non-existent upload

### Results (Admin)

- [ ] POST /results/upload/ - Creates NMData (admin only)
- [ ] POST /results/upload/ - Returns 401 without auth
- [ ] POST /results/upload/ - Returns 403 for non-admin
- [ ] POST /results/upload/ - Parses CSV and stores as json_data
- [ ] POST /results/upload/ - Returns 400 for invalid CSV format
- [ ] PUT /results/nmdata/{id}/update/ - Updates NMData (admin only)
- [ ] PUT /results/nmdata/{id}/update/ - Returns 403 for non-admin

### Media Upload



---

## Coverage Requirements

| Component | Target Coverage |
|-----------|-----------------|
| Models | 90%+ |
| Views/API | 80%+ |
| Serializers | 80%+ |
| Permissions | 90%+ |
| Utils | 70%+ |

### Running Coverage

```bash
# Run tests with coverage
coverage run --source='.' manage.py test

# View coverage report
coverage report

# Generate HTML report
coverage html

# Open HTML report
open htmlcov/index.html
```

---

## Continuous Integration

Recommended GitHub Actions workflow:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test_db
          SECRET_KEY: test-secret-key
        run: |
          python manage.py test
      
      - name: Run coverage
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test_db
          SECRET_KEY: test-secret-key
        run: |
          coverage run --source='.' manage.py test
          coverage report
```

---

*Last Updated: 2026-04-03*
