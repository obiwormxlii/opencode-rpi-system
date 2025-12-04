# RPI System - Quick Reference

## Commands

| Command | Description | When to Use |
|---------|-------------|-------------|
| `/rpi` | Full workflow | Starting a new feature or fix |
| `/research <topic>` | Research only | Understanding codebase before planning |
| `/planner <feature>` | Planning only | Creating implementation strategy |
| `/implement` | Execute plan | After plan is reviewed and approved |
| `/verify` | Validate code | Checking standards compliance |
| `/compact` | Compress context | When conversation gets long |

## Workflow

```
/rpi → Describe feature/fix
  ↓
Research phase (automatic)
  ↓
Review: .tmp/research/current-research.md
  ↓
Plan phase (automatic)
  ↓
Review: .tmp/plans/current-plan.md
  ↓
Approve plan
  ↓
Implementation (automatic)
  ↓
Verification (automatic)
  ↓
Review: .tmp/verification/latest-report.md
  ↓
✅ APPROVED or 🚨 BLOCKED
```

## Agents

| Agent | Model | Mode | Purpose |
|-------|-------|------|---------|
| **Research** | Opus 4.5 | Subagent | Understand codebase, compress findings |
| **Plan** | Sonnet 4.5 | Subagent | Create atomic implementation plans |
| **Implement** | Sonnet 4.5 | Primary | Execute plan step-by-step |
| **Verify** | Opus 4.5 | Subagent | Validate standards (BLOCKS on critical) |
| **Explore** | Haiku 4.5 | Subagent | Fast exploration for Research |

## Key Principles

### 1. Always Research First ✅
Research is auto-run. It provides context for planning.

### 2. Atomic Phases 🧩
Plans break work into small, independent, testable changes.

### 3. Context Compaction 📦
- Stay below 40% token usage ("smart zone")
- Delegate to sub-agents
- Compress findings into markdown

### 4. Verification Blocks 🚨
- **CRITICAL** issues block implementation
- **RECOMMENDATIONS** are warnings only

### 5. Mental Alignment 🧠
All phases produce human-readable documents for team review.

## Verification Status

### ✅ APPROVED
No critical issues. Safe to merge.

### ⚠️ APPROVED WITH NOTES
Recommendations provided. Consider addressing.

### 🚨 BLOCKED
Critical issues must be fixed:
- Hardcoded secrets
- SQL injection vulnerabilities
- Type errors
- Missing authentication
- Unhandled errors

## File Structure

```
~/.config/opencode/        # Base config (global)
├── agent/                 # Agent definitions
├── command/               # Custom commands
├── prompt/                # System prompts
└── rules/                 # Blocking criteria

.opencode/                 # Project config
└── standards/             # Project standards

.tmp/                      # Session data (gitignored)
├── research/              # Research snapshots
├── plans/                 # Implementation plans
└── verification/          # Verification reports
```

## Common Tasks

### Start New Feature
```
/rpi
"Add user profile page with edit functionality"
```

### Understand Existing Code
```
/research "how does authentication work"
```

### Review Plan Before Implementing
```
/planner "refactor database connection pooling"
# Review .tmp/plans/current-plan.md
# Then approve and:
/implement
```

### Compress Long Conversation
```
/compact
```

### Check Code Quality
```
/verify
```

## Standards Checked

### SOLID ✓
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

### Security 🔒
- No hardcoded secrets
- SQL injection prevention
- XSS prevention
- Authentication/authorization
- Input validation

### Code Quality 📝
- Type safety (strict mode)
- Error handling
- Naming conventions
- DRY (Don't Repeat Yourself)
- Test coverage (80%+)

### Atomic Design 🎨 (Frontend)
- Atoms → Molecules → Organisms → Templates → Pages

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Context too large | Use `/compact` |
| Research not finding files | Check `.gitignore`, create `.ignore` |
| Verification always blocking | Review `.opencode/standards/` |
| Plan too vague | Provide more context in `/rpi` description |
| Implementation failing | Check `.tmp/verification/latest-report.md` |

## Customization

### Project Standards
Edit: `.opencode/standards/custom-standards.md`

### Blocking Criteria
Edit: `~/.config/opencode/rules/rpi-blocking-criteria.md`

### Agent Prompts
Edit: `~/.config/opencode/prompt/*.txt`

### Model Selection
Edit: `~/.config/opencode/opencode.json`

## Tips

1. **Be Specific**: Detailed descriptions → better research → better plans
2. **Review Plans**: Always review before implementing
3. **Fix Critical Issues**: Don't skip verification blockers
4. **Use Sub-agents**: Let agents delegate for better context management
5. **Keep Standards Updated**: Maintain `.opencode/standards/custom-standards.md`

## Example Session

```bash
# Start OpenCode
opencode

# Navigate to project
cd /path/to/project

# Run RPI workflow
/rpi

# Describe feature
"Add email verification to user registration.
Users should receive an email with a verification link.
After clicking, their account is activated.
Add verification check on login to prevent unverified users from accessing the app."

# System runs Research → Plan → Implement → Verify
# Review each phase in .tmp/

# If BLOCKED, fix issues and re-verify
/verify

# If APPROVED, commit changes
git add .
git commit -m "feat: add email verification to registration"
```

## Resources

- Full Documentation: [README.md](./README.md)
- Setup Guide: [SETUP.md](./SETUP.md)
- OpenCode Docs: https://opencode.ai/docs
- 12 Factor Agents Talk: [Link to talk]
