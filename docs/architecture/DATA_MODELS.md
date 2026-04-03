# Data Models

Database models and entity relationships.

---

## User Model (`authentication`)

```python
User:
- id: AutoField (PK)
- username: CharField (unique, indexed)
- email: EmailField (unique, indexed)
- firstname: CharField
- lastname: CharField
- address: TextField (nullable)
- linkedin: TextField (nullable)
- phone: CharField (nullable)
- referral_code: CharField (unique, indexed)
- is_verified: BooleanField (default=False)
- is_approved: BooleanField (default=False)
- is_active: BooleanField (default=True)
- is_staff: BooleanField (default=False)
- created_at: DateTimeField (auto_now_add)
- updated_at: DateTimeField (auto_now)
- auth_provider: CharField (default='email')
```

### User Relationships

```
User
├── Referrals (FK - owner)
└── NMData (FK - uploaded_by)
```

---

## Referrals Model (`authentication`)

```python
Referrals:
- id: AutoField (PK)
- owner: ForeignKey -> User
- referred: ForeignKey -> User
- status: BooleanField (default=False)
- created_at: DateTimeField (auto_now_add)
- updated_at: DateTimeField (auto_now)
```

---

## Profile Model (`authentication`)

```python
Profile:
- id: AutoField (PK)
- user: ForeignKey -> User
- dob: DateField (nullable)
- identity: ImageField (upload_to='identity/')
```

---

## NMData Model (`results`)

```python
NMData:
- id: AutoField (PK)
- name: CharField (CSV name/title)
- slug: SlugField (unique, auto-generated from name)
- data_type: CharField (type of data: dividends, results, etc.)
- description: TextField (optional description)
- upload_date: DateField (date of upload)
- csv_file: FileField (uploaded CSV file)
- status: CharField (choices: pending, approved, disapproved)
- json_data: JSONField (parsed CSV data as array)
- uploaded_by: ForeignKey -> User
- created_at: DateTimeField (auto_now_add)
- updated_at: DateTimeField (auto_now)
```

### Status Choices

| Value | Description |
|-------|-------------|
| `pending` | Awaiting review/approval |
| `approved` | Approved and active |
| `disapproved` | Rejected |

---

## Database Indexes

### User Table

```sql
CREATE INDEX idx_auth_user_username ON authentication_user(username);
CREATE INDEX idx_auth_user_email ON authentication_user(email);
CREATE INDEX idx_auth_user_referral ON authentication_user(referral_code);
```

### NMData Table

```sql
CREATE INDEX idx_results_nmdata_name ON results_nmdata(name);
CREATE INDEX idx_results_nmdata_data_type ON results_nmdata(data_type);
CREATE INDEX idx_results_nmdata_status ON results_nmdata(status);
CREATE INDEX idx_results_nmdata_upload_date ON results_nmdata(upload_date);
```

---

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │
├─────────────┤
│ id          │
│ username    │
│ email       │
│ firstname   │
│ lastname    │
│ is_verified │
│ is_staff    │
│ is_active   │
└──────┬──────┘
       │
       ├───────────────────┐
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│  Referrals  │     │   NMData    │
├─────────────┤     ├─────────────┤
│ id          │     │ id          │
│ owner       │────▶│ name        │
│ referred    │     │ data_type   │
│ status      │     │ csv_file    │
│ created_at  │     │ json_data   │
└─────────────┘     │ status      │
                    │ uploaded_by │────┐
                    │ created_at  │    │
                    └─────────────┘    │
                                       │
                              ┌────────┴────┐
                              │    User     │
                              └─────────────┘
```

---

## Legacy Models (Deprecated)

The following models exist in deprecated apps and should not be used for new features:

### Article Model (`article` app - Deprecated)

```python
Article:
- id: AutoField (PK)
- title: CharField
- slug: SlugField (unique)
- content: TextField (HTML)
- author: ForeignKey -> User
- featured_image: ImageField
- created_at: DateTimeField
- updated_at: DateTimeField
```

---

*Last Updated: 2026-04-03*
