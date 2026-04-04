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
├── Articles (FK - author)
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

## Article Model (`article`)

```python
Article:
- id: AutoField (PK)
- slug: SlugField (unique)
- title: CharField
- content: TextField (HTML)
- excerpt: TextField
- category: CharField (choices: article, disclosure, news, actions)
- tags: JSONField (list)
- featured_image: ImageField
- status: CharField (draft, pending, approved, published, archived)
- featured: BooleanField
- meta_title: CharField (SEO)
- meta_description: TextField (SEO)
- og_image: CharField (SEO)
- author_name: CharField
- author: ForeignKey -> User
- date: DateTimeField
- created_at: DateTimeField
- updated_at: DateTimeField
```

### ArticleCategory Model (`article`)

```python
ArticleCategory:
- id: AutoField (PK)
- name: CharField (unique)
- slug: SlugField (unique)
- description: TextField
- created_at: DateTimeField
```

### MediaFile Model (`article`)

```python
MediaFile:
- id: AutoField (PK)
- file: FileField
- original_filename: CharField
- file_type: CharField
- file_size: PositiveIntegerField
- uploaded_by: ForeignKey -> User
- uploaded_at: DateTimeField
- article: ForeignKey -> Article (optional)
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
- status: CharField (choices: pending, approved, disapproved, default: pending)
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

## Resource Model (`resources` - In Development)

> **Note:** This model is implemented but has no API endpoints yet.

```python
Resource:
- id: AutoField (PK)
- slug: SlugField (unique)
- title: CharField
- content: TextField (HTML)
- excerpt: TextField
- category: CharField (article, disclosure, news, actions)
- tags: JSONField (list, max 10)
- featured_media: CharField (URL)
- featured_media_type: CharField (local/external)
- status: CharField (draft, pending, approved, published, archived)
- featured: BooleanField
- meta_title: CharField (SEO)
- meta_description: TextField (SEO)
- og_image: CharField (SEO)
- author_name: CharField
- author_user: ForeignKey -> User
- date: DateTimeField
- link: URLField
- created_at: DateTimeField
- updated_at: DateTimeField
```

---

## Database Indexes

### User Table

```sql
CREATE INDEX idx_auth_user_username ON authentication_user(username);
CREATE INDEX idx_auth_user_email ON authentication_user(email);
CREATE INDEX idx_auth_user_referral ON authentication_user(referral_code);
```

### Article Table

```sql
CREATE INDEX idx_article_category ON article_article(category);
CREATE INDEX idx_article_status ON article_article(status);
CREATE INDEX idx_article_date ON article_article(date);
CREATE INDEX idx_article_featured ON article_article(featured);
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
       ├───────────────────┬───────────────────┐
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Referrals  │     │   Article   │     │   NMData    │
├─────────────┤     ├─────────────┤     ├─────────────┤
│ id          │     │ id          │     │ id          │
│ owner       │────▶│ slug        │     │ name        │
│ referred    │     │ title       │     │ data_type   │
│ status      │     │ content     │     │ csv_file    │
│ created_at  │     │ category    │     │ json_data   │
└─────────────┘     │ status      │     │ status      │
                    │ author      │────▶│ uploaded_by │────┐
                    │ created_at  │     │ created_at  │    │
                    └─────────────┘     └─────────────┘    │
                                                           │
                                                  ┌────────┴────┐
                                                  │    User     │
                                                  └─────────────┘
```

---

*Last Updated: 2026-04-03*
