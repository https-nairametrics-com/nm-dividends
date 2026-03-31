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

Use this template for PR descriptions:

```markdown
## Summary
Brief description of changes

## Changes
- List specific changes
- Use bullet points

## Testing
- [ ] Unit tests pass (`python manage.py test`)
- [ ] Integration tests pass (if applicable)
- [ ] Manual testing completed
- [ ] Test coverage >= 80% for new code
- [ ] Linting passes (`flake8 .`, `black --check .`)

## Checklist
- [ ] Code follows Django/Python style guide
- [ ] Documentation updated (if needed)
- [ ] No breaking changes (or documented)
- [ ] Migrations tested (if applicable)

## Related Issue
Closes #<number>
```

### 6. Review and Merge

#### Developer Responsibilities

As a feature developer, your responsibility ends at creating the pull request. You do not merge your own PRs.

```bash
# Push your feature branch
git push origin issue-<number>-<description>

# Create PR for review
gh pr create --base main --title "Issue #<n>: Description" --body "Closes #<n>"

# Respond to reviewer feedback
# Do not click the merge button - that is the reviewer's role
```

#### Reviewer/Maintainer Responsibilities

The reviewer is responsible for:
1. Code review (quality, style, acceptance criteria)
2. Running tests and verifying they pass
3. Checking test coverage meets requirements
4. Merging via GitHub UI once approved

**Review Checklist:**
- [ ] Code follows project conventions
- [ ] Acceptance criteria are met
- [ ] All tests pass (`python manage.py test`)
- [ ] Test coverage >= 80% for new code
- [ ] Linting passes (`flake8 .`, `black --check .`)
- [ ] Migrations are valid (if applicable)
- [ ] No security issues

**Running Tests Before Merge:**
```bash
# Checkout the PR branch
gh pr checkout <pr-number>

# Run full test suite
python manage.py test

# Check coverage
coverage run manage.py test
coverage report

# Run linting
flake8 .
black --check .
```

After approval, the reviewer merges via GitHub UI using "Squash and merge" and deletes the feature branch.

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

## Testing Requirements

### Before Creating PR

Run these commands locally:

```bash
# Run tests
python manage.py test

# Check coverage
coverage run manage.py test
coverage report

# Run linting
flake8 .
black --check .

# Check migrations (if models changed)
python manage.py makemigrations --check --dry-run
```

**Requirements:**
- All tests must pass
- New code: minimum 80% coverage
- No linting errors
- Valid migrations

### Reviewer Testing

Before approving, reviewers must:
1. Checkout PR: `gh pr checkout <number>`
2. Run tests: `python manage.py test`
3. Verify coverage: `coverage report`
4. Run linting: `flake8 . && black --check .`
5. Test migrations: `python manage.py migrate` (test DB)

## Dependency Analysis Framework

### When to Branch from Other Branches

If your issue depends on code from an open PR that hasn't merged yet:

#### Step 1: Check for Dependencies

Read the issue description for explicit dependencies:
- "Depends on..."
- "Requires..."
- "Blocked by..."

#### Step 2: Analyze Infrastructure

Before branching, verify required infrastructure exists:

```bash
# Check if auth system exists in main
grep -r "authentication" app_name/

# Check if models exist
ls app_name/models.py

# Check open PRs for related work
gh pr list --state open
```

#### Step 3: Branching Strategy

| Scenario | Branch From | Example |
|----------|-------------|---------|
| Standalone feature | `main` | `issue-5-add-endpoint` |
| Needs unmerged auth | `issue-3-auth-system` | `issue-6-user-profile` |
| Uses new models | `issue-4-model-changes` | `issue-7-api-views` |

#### Example: Branching from a Feature Branch

Issue #10 depends on Issue #9 (auth system) which is in PR but not merged:

```bash
# 1. Checkout the dependency branch
git checkout issue-9-auth-system
git pull origin issue-9-auth-system

# 2. Create your branch from it
git checkout -b issue-10-user-profile

# 3. Implement changes
git add .
git commit -m "feat(user): add user profile endpoint"

# 4. Push both branches
git push origin issue-9-auth-system   # PR #20
git push origin issue-10-user-profile # PR #21

# 5. Create PRs (dependency first)
gh pr create --base main --title "feat: auth system" --body "Closes #9"
gh pr create --base main --draft --title "feat: user profile (depends on #20)" \
  --body "Depends on PR #20. Closes #10"
```

**After the dependency merges:**
```bash
# Rebase onto main to clean up history
git checkout issue-10-user-profile
git fetch origin
git rebase origin/main
git push --force-with-lease origin issue-10-user-profile
gh pr ready  # Mark as ready for review
```

## Project Board Integration (Optional)

If using GitHub Projects to track issues:

### Board Columns
- **Backlog** - Not started
- **In Progress** - Actively working
- **Review** - PR created
- **Done** - Merged

### Updating Status

```bash
# Move to In Progress
gh project item-edit --id <item-id> --field "Status" --value "In Progress"

# Or use GitHub UI
```

### When to Update

| Action | Update To |
|--------|-----------|
| Start working | In Progress |
| Create PR | Review |
| PR merged | Done |

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

*Workflow updated with testing requirements and review procedures*
