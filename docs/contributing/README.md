# Contributing Guide

How to contribute to the NM Dividends Backend project.

## Development Workflow

See [WORKFLOW.md](./WORKFLOW.md) for detailed Git workflow and conventions.

## Quick Reference

### Branch Naming
```
issue-<number>-<brief-description>
```

Examples:
- `issue-1-add-csv-validation`
- `issue-9-standardize-responses`

### Commit Format
```
<type>(<scope>): <description>
```

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code style
- `refactor` - Code refactoring
- `test` - Tests
- `chore` - Build/tool changes

### PR Template

```markdown
## Summary
Implements Issue #<number>: <Brief Title>

## Changes
- Change 1
- Change 2

## Testing
How to test these changes

## Screenshots (if UI)

Closes #<number>
```

## Code Standards

- Follow PEP 8 for Python
- Use type hints where possible
- Write docstrings for functions
- Keep functions under 50 lines
- Maintain test coverage > 80%

## Review Process

1. Create PR to `staging` branch
2. Ensure tests pass
3. Request review from team
4. Address feedback
5. Merge when approved

---

*See [WORKFLOW.md](./WORKFLOW.md) for complete workflow*
