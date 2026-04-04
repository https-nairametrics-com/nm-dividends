# Results API

API for managing NM Data CSV uploads and results tracking.

---

## Overview

The Results API allows admin users to upload CSV files containing financial data, which are parsed and stored as JSON. The data can then be queried and filtered by various parameters.

### Use Cases

- Upload dividend data CSVs
- Store corporate action results
- Track financial metrics over time
- Search/filter data by company name

---

## Data Model

### NMData

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String | CSV name/title |
| `slug` | String | URL-friendly identifier |
| `data_type` | String | Type of data (e.g., "dividends", "results") |
| `description` | String | Additional description |
| `upload_date` | Date | Date of upload |
| `csv_file` | File | Uploaded CSV file |
| `status` | String | pending, approved, disapproved |
| `json_data` | JSON | Parsed CSV data as array of objects |
| `uploaded_by` | FK | User who uploaded |
| `created_at` | DateTime | Creation timestamp |
| `updated_at` | DateTime | Last update timestamp |

### Status Options

| Status | Description |
|--------|-------------|
| `pending` | Awaiting review/approval |
| `approved` | Approved and active |
| `disapproved` | Rejected |

---

## Endpoints

### Upload CSV

Upload a new CSV file. Only admins can upload.

```bash
POST /results/upload/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

name: Q1 2024 Dividends
data_type: dividends
description: First quarter dividend data
upload_date: 2024-03-31
status: pending
csv_file: <csv-file-data>
```

**Response (201 Created):**
```json
{
  "id": 1,
  "uploaded_by": 5,
  "name": "Q1 2024 Dividends",
  "slug": "q1-2024-dividends",
  "data_type": "dividends",
  "description": "First quarter dividend data",
  "upload_date": "2024-03-31",
  "csv_file": "/media/csv/q1-2024-dividends.csv",
  "json_data": [
    {"Company": "Company A", "Dividend": "5.00", "Date": "2024-03-15"},
    {"Company": "Company B", "Dividend": "3.50", "Date": "2024-03-20"}
  ],
  "status": "pending",
  "updated_at": "2024-04-02T10:00:00Z"
}
```

### Update CSV Upload

Update an existing CSV upload. Only admins can update.

```bash
PUT /results/upload/1/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

name: Q1 2024 Dividends Updated
status: approved
csv_file: <updated-csv-file>
```

Or partial update:

```bash
PATCH /results/upload/1/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "approved",
  "description": "Updated description"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "uploaded_by": 5,
  "name": "Q1 2024 Dividends Updated",
  "slug": "q1-2024-dividends",
  "data_type": "dividends",
  "description": "Updated description",
  "upload_date": "2024-03-31",
  "csv_file": "/media/csv/q1-2024-dividends.csv",
  "json_data": [...],
  "status": "approved",
  "updated_at": "2024-04-02T11:00:00Z"
}
```

### View All Uploads

List all NMData uploads with filtering and pagination.

```bash
GET /results/uploads/?name=dividends&data_type=dividends&company=Company&sort_by=-upload_date&page=1&page_size=10
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Filter by name (icontains) |
| `data_type` | string | Filter by data type (icontains) |
| `company` | string | Search within json_data for company name |
| `sort_by` | string | Sort field (default: -upload_date) |
| `page` | integer | Page number (default: 1) |
| `page_size` | integer | Items per page (default: 10, max: 100) |

**Response (200 OK):**
```json
{
  "count": 50,
  "next": "http://localhost:8000/results/uploads/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Q1 2024 Dividends",
      "data_type": "dividends",
      "description": "First quarter dividend data",
      "upload_date": "2024-03-31",
      "status": "approved",
      "uploaded_by": 5,
      "json_data": [
        {"Company": "Company A", "Dividend": "5.00", "Date": "2024-03-15"},
        {"Company": "Company B", "Dividend": "3.50", "Date": "2024-03-20"}
      ]
    }
  ]
}
```

**With Company Filter:**
When `company` parameter is provided, only matching rows from `json_data` are returned:

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Q1 2024 Dividends",
      "data_type": "dividends",
      "description": "First quarter dividend data",
      "upload_date": "2024-03-31",
      "status": "approved",
      "uploaded_by": 5,
      "filtered_json_data": [
        {"Company": "Company A", "Dividend": "5.00", "Date": "2024-03-15"}
      ]
    }
  ]
}
```

### View My Uploads

Get all uploads by the authenticated user.

```bash
GET /results/my-uploads/
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "uploaded_by": 5,
    "name": "Q1 2024 Dividends",
    "slug": "q1-2024-dividends",
    "data_type": "dividends",
    "description": "First quarter dividend data",
    "upload_date": "2024-03-31",
    "csv_file": "/media/csv/q1-2024-dividends.csv",
    "json_data": [...],
    "status": "approved",
    "updated_at": "2024-04-02T10:00:00Z"
  }
]
```

### Update Upload (Alternative)

Alternative endpoint for updating uploads.

```bash
PUT /results/nmdata/1/update/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

{
  "name": "Updated Name",
  "status": "approved",
  "csv_file": <new-file>
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "uploaded_by": 5,
  "name": "Updated Name",
  "slug": "q1-2024-dividends",
  "data_type": "dividends",
  "description": "First quarter dividend data",
  "upload_date": "2024-03-31",
  "csv_file": "/media/csv/updated-file.csv",
  "json_data": [...],
  "status": "approved",
  "updated_at": "2024-04-02T12:00:00Z"
}
```

---

## Endpoint Summary

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/results/upload/` | Admin | Upload new CSV |
| PUT/PATCH | `/results/upload/<id>/` | Admin | Update CSV upload |
| GET | `/results/uploads/` | Public | List all uploads (filtered) |
| GET | `/results/my-uploads/` | Yes | List user's uploads |
| PUT/PATCH | `/results/nmdata/<id>/update/` | Admin | Update upload (alt) |

---

## CSV File Requirements

### Supported Encodings
- UTF-8 (preferred)
- Latin-1 (fallback)
- Auto-detected using chardet

### CSV Format
- Must have header row
- Comma-separated values
- Standard CSV format

### Example CSV
```csv
Company,Dividend,Date,Currency
Company A,5.00,2024-03-15,USD
Company B,3.50,2024-03-20,USD
Company C,2.75,2024-03-25,USD
```

This will be parsed to:
```json
[
  {"Company": "Company A", "Dividend": "5.00", "Date": "2024-03-15", "Currency": "USD"},
  {"Company": "Company B", "Dividend": "3.50", "Date": "2024-03-20", "Currency": "USD"},
  {"Company": "Company C", "Dividend": "2.75", "Date": "2024-03-25", "Currency": "USD"}
]
```

---

## Error Responses

### File Encoding Error
```json
{
  "error": "File encoding issue: <details>"
}
```
**Status:** 400 Bad Request

### Missing File
```json
{
  "error": "CSV file is required"
}
```
**Status:** 400 Bad Request

### Upload Not Found
```json
{
  "error": "Upload not found"
}
```
**Status:** 404 Not Found

### Validation Errors
```json
{
  "name": ["This field is required."],
  "data_type": ["This field is required."]
}
```
**Status:** 400 Bad Request

### Permission Denied
```json
{
  "detail": "You do not have permission to perform this action."
}
```
**Status:** 403 Forbidden

---

## Use Case Examples

### Upload Dividend Data

```bash
curl -X POST http://localhost:8000/results/upload/ \
  -H "Authorization: Bearer <token>" \
  -F "name=Q1 2024 Dividends" \
  -F "data_type=dividends" \
  -F "description=First quarter dividend announcements" \
  -F "upload_date=2024-03-31" \
  -F "status=pending" \
  -F "csv_file=@dividends_q1_2024.csv"
```

### Search for Company Data

```bash
curl "http://localhost:8000/results/uploads/?company=Zenith+Bank&data_type=dividends"
```

### Approve Pending Upload

```bash
curl -X PATCH http://localhost:8000/results/upload/1/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'
```

---

*Last Updated: 2026-04-03*
