# Project Coding Standards

## Overview
This document defines coding standards and principles for this project.

## Technology Stack
- **Backend**: [Specify language/framework]
- **Frontend**: [Specify framework]
- **Database**: [Specify database]
- **Testing**: [Specify testing framework]

## Architectural Pattern
[Describe the architectural pattern: MVC, microservices, monolith, etc.]

## Language-Specific Standards

### TypeScript
- Strict mode: REQUIRED
- No `any` types without justification
- All function parameters and returns must be typed
- Use interfaces for object shapes, types for unions/primitives
- Async operations must be properly typed

### Python
- Type hints required for all functions
- Minimum Python version: [specify]
- Use dataclasses or Pydantic for data structures
- Follow PEP 8 style guide
- Use type checkers (mypy) in CI/CD

## Naming Conventions
- **Classes/Components**: PascalCase (e.g., `UserService`, `Button`)
- **Functions/Methods**: camelCase (e.g., `getUserData()`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_RETRY_ATTEMPTS`)
- **Files**: kebab-case for utilities, PascalCase for classes/components
- **Private methods**: Prefix with underscore `_privateMethod()`

## SOLID Principles Expectations

1. **Single Responsibility**: Each class/function has ONE reason to change
2. **Open/Closed**: Extensible without modification (use inheritance, composition)
3. **Liskov Substitution**: Derived types are substitutable for base types
4. **Interface Segregation**: Small, focused interfaces over large, general ones
5. **Dependency Inversion**: Depend on abstractions, not concrete implementations

## Atomic Design (Frontend)
If applicable to your frontend:
- **Atoms**: Basic components (button, input, label)
- **Molecules**: Simple component compositions (form field, card)
- **Organisms**: Complex components (navigation, header, sidebar)
- **Templates**: Page layouts
- **Pages**: Full page implementations

## Testing Requirements
- Minimum code coverage: 80%
- Unit tests for all business logic
- Integration tests for APIs
- E2E tests for critical user flows
- Test files located adjacent to source: `__tests__/` or `.test.ts` suffix

## Security Requirements
- ✅ Input validation on all user-controlled data
- ✅ Parameterized queries for all database access
- ✅ No hardcoded secrets (use environment variables)
- ✅ All endpoints require authentication/authorization where applicable
- ✅ Proper error handling (don't expose internal errors)
- ✅ Dependency vulnerabilities: Scan regularly
- ✅ HTTPS only in production
- ✅ CSRF protection on state-changing operations

## Git Workflow
- Commits should be atomic and focused
- Commit message format: `[type]: description`
  - Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`
  - Example: `feat: add email verification flow`
- Branch naming: `feature/short-description`, `fix/short-description`
- Require code review before merge
- Squash commits on merge (optional, configure per team)

## CI/CD Pipeline
- Run linter: `npm run lint` or `pylint`
- Run type checker: `tsc --noEmit` or `mypy`
- Run tests: `npm test` or `pytest`
- Build check: `npm run build` or equivalent
- Security scan: Check for dependency vulnerabilities

## Common Anti-Patterns to Avoid
1. God classes (too many responsibilities)
2. Deeply nested conditionals (use guard clauses)
3. Magic numbers (extract to named constants)
4. Duplicate code (extract to shared functions)
5. Ignoring errors (always handle or propagate)
6. Mixing concerns (business logic in UI, etc.)
7. Tight coupling (depend on abstractions)

## Code Review Checklist
- [ ] Does this follow SOLID principles?
- [ ] Are there security vulnerabilities?
- [ ] Is error handling adequate?
- [ ] Are tests included?
- [ ] Is naming clear and descriptive?
- [ ] Is the code DRY?
- [ ] Are edge cases handled?

## Documentation Standards
- All public APIs must be documented
- Complex algorithms should have comments explaining "why"
- README should include: setup, usage, testing, deployment
- Keep documentation up to date with code changes

## Performance Guidelines
- Avoid N+1 queries
- Use pagination for large datasets
- Cache expensive computations
- Profile before optimizing
- Monitor production performance

## Questions?
Refer to recent PRs, CONTRIBUTING.md, or ask the team.
