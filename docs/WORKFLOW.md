# NM Dividends Backend - Development Workflow

This document describes the development workflow for the NM Dividends backend project.

## Repository Structure

- **Main Repo:** `https-nairametrics-com/nm-dividends` (fork of `Francis-Njoku/nm-dividends`)
- **Upstream:** `Francis-Njoku/nm-dividends`
- **Default Branch:** `main`

## Workflow Overview

We use an issue-based workflow with short-lived feature branches.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    Issue    │────▶│    Branch   │────▶│     PR      │
│   (GitHub)  │     │  (Local)    │     │  (to main)  │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Step-by-Step Process

### 1. Pick an Issue

- Check the [Issues tab](https://github.com/https-nairametrics-com/nm-dividends/issues)
- Start with P0 (Critical) issues first
- Ensure dependencies are completed before starting

### 2. Create a Branch

Branch naming convention:
```
issue-<number>-<brief-description>
```

Examples:
- `issue-1-create-resources-app`
- `issue-2-resources-api-crud`
- `issue-6-environment-settings`

Commands:
```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create and switch to feature branch
git checkout -b issue-<number>-<description>
```

### 3. Make Changes

- Write code following the project conventions
- Keep commits small and focused
- **Commit messages should be ONE LINE only**

Good commit messages:
```bash
git commit -m "feat(resources): add Resource model"
git commit -m "fix(auth): standardize login response format"
git commit -m "test(resources): add CRUD endpoint tests"
```

Bad commit messages:
```bash
# Too long, has body
git commit -m "feat(resources): create Resources app

This commit adds the Resources app with models..."  # ❌

# No clear type prefix
git commit -m "added some stuff"  # ❌
```

### 4. Push and Create PR

```bash
# Push branch
git push origin issue-<number>-<description>

# Create PR (via GitHub CLI or web)
gh pr create --title "Issue #<number>: <Brief Title>" \
             --body "<Detailed description>" \
             --repo https-nairametrics-com/nm-dividends
```

### 5. PR Description Template

Include in your PR description:
- What was implemented/changed
- How to test
- Link to the issue: `Closes #<number>`

Example:
```markdown
## Summary
Implements Issue #2: Resources API CRUD & Categories

## Changes
- Add ResourceSerializer with validation
- Add ResourceViewSet with CRUD operations
- Add permission checks (public read, admin write)
- Add filters for category, status, featured, search
- Add pagination (max 100 per page)
- Add categories endpoint with resource counts

## Testing
Tested via Django shell and browsable API.

Closes #2
```

### 6. Review and Merge

- PRs should be reviewed before merging
- Once approved, merge to `main`
- Delete the feature branch after merge

## Commit Message Conventions

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <short description>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, missing semi colons, etc)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

Scopes (examples):
- `resources`: Resources app
- `auth`: Authentication
- `settings`: Django settings
- `tests`: Test suite

Examples:
```
feat(resources): add Resource model
feat(resources): implement CRUD endpoints
fix(auth): correct token refresh response
docs(api): add resources endpoint documentation
test(resources): add permission tests
chore(deps): add django-csp to requirements
```

## Issue Priority Levels

| Label | Priority | Description |
|-------|----------|-------------|
| `P0` | Critical | Blocks development, security issues |
| `P1` | High | Important features, blocking integration |
| `P2` | Medium | Should have, non-blocking |
| `P3` | Low | Nice to have |
| `P4` | Very Low | Future improvements |

## Common Commands

```bash
# Sync with upstream (parent repo)
git fetch upstream
git checkout main
git merge upstream/main

# Check status
git status
gh issue list --repo https-nairametrics-com/nm-dividends

# Create PR
gh pr create --repo https-nairametrics-com/nm-dividends

# View PRs
gh pr list --repo https-nairametrics-com/nm-dividends
```

## Important Notes

1. **Always branch from latest main**
2. **One issue = one branch = one PR**
3. **Commit messages: ONE LINE ONLY**
4. **Implementation details go in PR description**
5. **Test before creating PR**
6. **PRs target `main` branch of your fork**

## Git Remotes

```bash
# Check remotes
git remote -v

# Expected output:
# origin   git@github.com:https-nairametrics-com/nm-dividends.git (fetch)
# origin   git@github.com:https-nairametrics-com/nm-dividends.git (push)
# upstream git@github.com:Francis-Njoku/nm-dividends.git (fetch)
# upstream git@github.com:Francis-Njoku/nm-dividends.git (push)
```

---

*Last Updated: 2026-03-31*
