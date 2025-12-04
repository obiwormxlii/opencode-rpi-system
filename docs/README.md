# RPI System (Research → Plan → Implement)

A markdown-based, OpenCode-native agentic system implementing the Research → Plan → Implement methodology for context-aware AI-driven development.

## Overview

The RPI system operationalizes the concepts from Dex's "12 Factor Agents" talk, focusing on:
- **Context Compaction**: Staying in the "smart zone" (< 40% token usage)
- **Sub-agent Delegation**: Automatic spawning for exploration and analysis
- **Verification Blocking**: Standards validation that prevents bad code from shipping
- **Mental Alignment**: Human-readable research, plans, and verification reports

## Quick Start

### Installation

1. Ensure you have [OpenCode](https://opencode.ai) installed
2. The base configuration is already set up in `~/.config/opencode/`
3. Project-specific configuration is in `.opencode/`

### Basic Usage

```bash
# Start OpenCode
opencode

# Run the RPI workflow
/rpi

# Or run individual phases:
/research "understand authentication system"
/planner "implement email verification"
/implement
/verify
```

## System Architecture

```
User Request
    ↓
[Research Agent] ← Explores codebase, compresses findings
    ↓
Research Snapshot (.tmp/research.md)
    ↓
[Planner Agent] ← Reviews research, creates implementation plan
    ↓
Plan Document (.tmp/plans/) + Todo items
    ↓
[Implement Agent] ← Executes plan step-by-step
    ↓
[Verify Agent] ← Validates standards (BLOCKS if critical issues)
    ↓
Output: Code Changes + Verification Report
```

## Agents

### Research Agent
- **Model**: Claude Opus 4.5 (deep understanding)
- **Mode**: Subagent
- **Tools**: Read-only + webfetch
- **Purpose**: Understand codebase, find relevant files, document patterns

### Planner Agent
- **Model**: Claude Sonnet 4.5 (balanced)
- **Mode**: Subagent
- **Tools**: Read-only + todowrite
- **Purpose**: Create atomic implementation plans with exact steps

### Implement Agent
- **Model**: Claude Sonnet 4.5 (balanced)
- **Mode**: Primary
- **Tools**: Full write access
- **Purpose**: Execute plans step-by-step with testing

### Verify Agent
- **Model**: Claude Opus 4.5 (careful analysis)
- **Mode**: Subagent
- **Tools**: Read-only + limited bash (tests/linting)
- **Purpose**: Validate SOLID, security, type safety (BLOCKS on critical issues)

### Explore Agent
- **Model**: Claude Haiku 4.5 (fast)
- **Mode**: Subagent
- **Tools**: Read-only
- **Purpose**: Fast, targeted exploration for Research agent

## Commands

| Command | Description |
|---------|-------------|
| `/rpi` | Full Research → Plan → Implement workflow |
| `/research` | Run research phase only |
| `/planner` | Create implementation plan |
| `/implement` | Execute existing plan |
| `/verify` | Run standards verification |
| `/compact` | Compress context into research snapshot |

## Directory Structure

```
~/.config/opencode/          # Base configuration (synced with GitHub)
├── agent/                    # Agent definitions
│   ├── research.md
│   ├── plan.md
│   ├── implement.md
│   ├── verify.md
│   └── explore.md
├── command/                  # Custom commands
│   ├── rpi.md
│   ├── research.md
│   ├── plan.md
│   ├── implement.md
│   ├── verify.md
│   └── compact.md
├── prompt/                   # System prompts
│   ├── research.txt
│   ├── plan.txt
│   └── verify-standards.txt
└── rules/                    # Verification rules
    └── rpi-blocking-criteria.md

.opencode/                    # Project-specific config
└── standards/
    └── custom-standards.md   # Project coding standards

.tmp/                         # Ephemeral session data (gitignored)
├── research/
│   ├── current-research.md
│   └── research-history/
├── plans/
│   ├── current-plan.md
│   └── plan-history/
└── verification/
    ├── latest-report.md
    └── verify-history.md
```

## Workflow Examples

### Simple Feature

```
User: /rpi
User: "Add email verification to user registration"

→ Research agent explores auth system, user model, email service
→ Creates `.tmp/research/current-research.md`

→ Plan agent creates atomic phases:
  - Phase 1: Add verification fields to User model
  - Phase 2: Create verification endpoint
  - Phase 3: Update registration flow
  - Phase 4: Add verification check on login

→ Implement agent executes each phase with tests

→ Verify agent checks:
  ✅ Type safety
  ✅ No hardcoded secrets
  ⚠️ Add error handling to email service
  
→ Status: APPROVED WITH NOTES
```

### Complex Refactor

```
User: /rpi
User: "Refactor auth system to use refresh tokens"

→ Research spawns @explore sub-agents for large codebase
→ Compresses findings into research snapshot

→ Plan creates many atomic phases (10+)
→ Each phase tracked via todo items

→ Implement executes phases incrementally
→ Context stays low through delegation

→ Verify finds:
  🚨 CRITICAL: Backwards compatibility issue
  
→ Status: BLOCKED
→ User fixes issue, re-runs verify
→ Status: APPROVED
```

## Key Principles

### 1. Always Research First
Research is auto-run by default. It provides essential context for planning.

### 2. Atomic Phases
Plans break work into independent, testable phases. Each phase:
- Has ONE logical goal
- Can be tested independently
- Includes rollback procedure

### 3. Context Compaction
Agents delegate to sub-agents to stay below 40% token usage ("smart zone").
- Research spawns @explore for large codebases
- Findings are compressed into markdown snapshots

### 4. Verification Blocks
The Verify agent identifies:
- 🚨 **CRITICAL** (blocks): Security vulnerabilities, type errors, hardcoded secrets
- ⚠️ **RECOMMENDATIONS** (warns): Style issues, optimizations

Implementation is BLOCKED until critical issues are fixed.

### 5. Mental Alignment
All phases produce human-readable documents:
- Research snapshots for understanding
- Plans for code review
- Verification reports for quality assurance

## Standards Validation

The Verify agent checks:

### SOLID Principles
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

### Security
- No hardcoded secrets
- SQL injection prevention
- XSS prevention
- CSRF protection
- Authentication/authorization checks

### Code Quality
- Type safety (strict mode)
- Error handling
- Naming conventions
- DRY (Don't Repeat Yourself)
- Test coverage (80% minimum)

### Atomic Design (Frontend)
- Atoms, Molecules, Organisms, Templates, Pages

## Customization

### Project-Specific Standards
Edit `.opencode/standards/custom-standards.md` to define:
- Technology stack
- Architectural patterns
- Naming conventions
- Testing requirements
- Security requirements

### Blocking Criteria
Blocking criteria are defined in `~/.config/opencode/rules/rpi-blocking-criteria.md`.
Critical issues always block implementation.

## Advanced Features

### Session History
Research and plans are stored in `.tmp/` with history:
- `research-history/` - Previous research from this session
- `plan-history/` - Previous plans from this session
- Automatically cleaned up when topics become irrelevant

### Todo Integration
Plan phases automatically create todo items:
- Research agent doesn't use todos (keeps context low)
- Plan agent creates todos for tracking
- Implement agent marks progress: pending → in_progress → completed

### Context Cleanup
Use `/compact` to:
- Compress long conversations
- Reset context when switching topics
- Archive findings before starting new work

## Troubleshooting

### Research not finding files?
- Check `.gitignore` - research respects git ignore patterns
- Use `.ignore` file to explicitly allow certain paths

### Verification blocking incorrectly?
- Review `.opencode/standards/custom-standards.md`
- Check `~/.config/opencode/rules/rpi-blocking-criteria.md`
- Critical issues are security/stability related and should be fixed

### Context getting too large?
- Use `/compact` to compress findings
- Ensure agents are delegating to @explore sub-agents
- Review research snapshots for unnecessary detail

## Future Enhancements

- [ ] GitHub Action integration (auto-attach research/plans to PRs)
- [ ] Project-level epic planning system
- [ ] Multi-repo support for monorepos
- [ ] Collaborative planning (team review workflows)
- [ ] Research comparison between sessions

## Contributing

To contribute to the RPI system:
1. Base configs are in `~/.config/opencode/`
2. Test changes on a sample project
3. Document any new agents, commands, or prompts
4. Ensure verification standards are comprehensive

## License

[Specify license]

## Credits

Based on concepts from Dex's "12 Factor Agents" talk:
- Context engineering and compaction
- Research → Plan → Implement methodology
- Sub-agent delegation
- Verification blocking
