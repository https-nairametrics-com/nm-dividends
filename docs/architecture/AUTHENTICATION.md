# Authentication & Authorization

Authentication flow and permission system.

---

## JWT Token Flow

```
┌─────────┐              ┌─────┐              ┌────────┐              ┌──────────┐
│ Client  │              │ API │              │  Auth  │              │ Database │
└────┬────┘              └──┬──┘              └───┬────┘              └────┬─────┘
     │                      │                     │                       │
     │ POST /api/token/     │                     │                       │
     │ {email, password}    │                     │                       │
     │─────────────────────>│                     │                       │
     │                      │ Validate credentials│                       │
     │                      │────────────────────>│                       │
     │                      │                     │ Check user exists     │
     │                      │                     │──────────────────────>│
     │                      │                     │                       │
     │                      │                     │<──────────────────────│
     │                      │                     │ User data             │
     │                      │                     │ Generate tokens       │
     │                      │                     │───────────────────┐   │
     │                      │                     │                   │   │
     │                      │<────────────────────│ {access, refresh} │   │
     │                      │                     │<──────────────────┘   │
     │<─────────────────────│ 200 OK + tokens     │                       │
     │                      │                     │                       │
     │                      │                     │                       │
     ═══════════════════════════════════════════════════════════════════════════
                                    [Token expires after 30 minutes]
     ═══════════════════════════════════════════════════════════════════════════
     │                      │                     │                       │
     │ Request + Bearer     │                     │                       │
     │ {access_token}       │                     │                       │
     │─────────────────────>│                     │                       │
     │                      │ Validate token      │                       │
     │                      │────────────────────>│                       │
     │                      │<────────────────────│ Token valid           │
     │                      │                     │                       │
     │                      │ Fetch data          │                       │
     │                      │────────────────────────────────────────────>│
     │                      │<────────────────────────────────────────────│
     │                      │ Data                │                       │
     │<─────────────────────│ 200 OK + data       │                       │
     │                      │                     │                       │
     │                      │                     │                       │
     │ POST /api/token/     │                     │                       │
     │ /refresh/            │                     │                       │
     │ {refresh}            │                     │                       │
     │─────────────────────>│                     │                       │
     │                      │ Validate refresh    │                       │
     │                      │────────────────────>│                       │
     │                      │<────────────────────│ New access token      │
     │<─────────────────────│ 200 OK + access     │                       │
     │                      │                     │                       │
```

### Token Details

| Token Type | Expiration | Usage |
|------------|------------|-------|
| Access Token | 30 minutes | API requests |
| Refresh Token | 7 days | Obtain new access token |

---

## Permission Matrix

| Role | Public Read | Authenticated Read | Create | Update | Delete | Admin Panel |
|------|-------------|-------------------|--------|--------|--------|-------------|
| Anonymous | Published only | - | - | - | - | - |
| Authenticated | Published only | Own data | - | Own profile | - | - |
| Editor (is_staff) | All | All | Yes | Yes | Yes | Limited |
| Admin (is_superuser) | All | All | Yes | Yes | Yes | Full |

### Role Definitions

#### Anonymous
- Can view public NMData uploads
- Can register, login, verify email
- Can request password reset

#### Authenticated
- All Anonymous permissions
- Can view own profile
- Can update own profile

#### Editor (is_staff=True)
- All Authenticated permissions
- Limited admin panel access

#### Admin (is_superuser=True)
- All Editor permissions
- Can upload CSV files to results
- Can manage users
- Full admin panel access
- Can manage site settings

---

## Response Format Standardization

### Current State

We have inconsistent response formats across different apps.

#### Target Standard Format

```json
{
  "success": true,
  "message": "Data retrieved successfully",
  "data": [...],
  "meta": {
    "current_page": 1,
    "per_page": 10,
    "total": 50,
    "total_pages": 5
  }
}
```

#### Legacy Format (`authentication` app)

```json
// Success - Various formats
{"status": "success", "data": {...}}
{"email": "Successfully activated"}
{"success": "We have sent you a link..."}
{...user_data}

// Error - Various formats
{"status": "error", "error": "..."}
{"error": "Activation Expired"}
{"errors": {...}}
```



### Standardization Progress (Active Apps)

| App | Current Format | Target Format | Status |
|-----|---------------|---------------|--------|
| authentication | Legacy | Standard | 🔄 In Progress |
| results | Custom | Standard | ⏳ Pending |

See [Issue #9 Implementation Plan](../plans/ISSUE_9_IMPLEMENTATION_PLAN.md) for migration details.

---

*Last Updated: 2026-04-03*
