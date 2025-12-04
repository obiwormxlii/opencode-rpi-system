# RPI Verification Blocking Criteria

## What Blocks Implementation

Implementation is BLOCKED if ANY of these conditions are true:

### 🚨 CRITICAL SECURITY

- [ ] Hardcoded secrets (API keys, passwords, JWT secrets)
- [ ] SQL injection vulnerability (string concatenation in queries)
- [ ] XSS vulnerability (unescaped user input in HTML)
- [ ] CSRF vulnerability (state-changing operations lack CSRF tokens)
- [ ] Unencrypted sensitive data transmission
- [ ] Exposed environment variables or configuration
- [ ] Missing authentication on protected routes/endpoints
- [ ] Incorrect permission checks (authorization bypass)
- [ ] Known CVE in dependency (CRITICAL or HIGH severity)

### 🚨 CRITICAL FUNCTIONALITY

- [ ] Type errors in strict mode (TypeScript/Python)
- [ ] Unhandled promise rejections (async without try-catch)
- [ ] Missing required error handling
- [ ] Breaking changes to public API without migration
- [ ] Database schema changes without migration strategy
- [ ] Infinite loops or performance regressions

### ⚠️ SIGNIFICANT ISSUES (Usually blocking unless justified)

- [ ] Missing input validation on user-controlled data
- [ ] Hardcoded environment-specific values
- [ ] Missing logging for critical operations
- [ ] Violates fundamental SOLID principle (blocks refactoring later)

## What Does NOT Block

These are recommendations but don't prevent implementation:

- Code style (formatting, naming, etc.)
- Performance optimizations (unless critical)
- Non-essential refactoring opportunities
- Test coverage gaps (unless below minimum threshold: 80%)
- Documentation gaps

## Override Process

If Verify agent identifies a CRITICAL issue:

1. **Cannot override**: The issue must be fixed
2. **Exception process**: 
   - Document in `.opencode/standards/custom-standards.md` why this is acceptable
   - Get explicit team approval
   - Still recommended: fix rather than override

## Examples

### ❌ BLOCKS Implementation

```typescript
// Hardcoded secret - BLOCKING
const API_KEY = "sk-abc123xyz";
```

```typescript
// SQL injection - BLOCKING
const query = `SELECT * FROM users WHERE email = '${userEmail}'`;
```

```typescript
// Missing auth - BLOCKING
app.get('/admin/settings', (req, res) => {
  // No check if user is authenticated or admin
  res.json(settings);
});
```

```typescript
// Unhandled promise rejection - BLOCKING
async function fetchData() {
  const data = await fetch(url); // No try-catch
  return data.json();
}
```

### ✅ DOES NOT BLOCK (recommendations only)

```typescript
// Poor naming - RECOMMENDATION
const x = getUserData();

// Suggestion: const userData = getUserData();
```

```typescript
// Could be DRY-er - RECOMMENDATION
if (user.role === 'admin') { doAdminThing(); }
// ... later ...
if (user.role === 'admin') { doOtherAdminThing(); }

// Suggestion: Extract to hasAdminRole()
```

```typescript
// Minor optimization opportunity - RECOMMENDATION
const items = data.map(x => x.id).filter(id => id > 0);

// Suggestion: Could combine into single pass with reduce
```
