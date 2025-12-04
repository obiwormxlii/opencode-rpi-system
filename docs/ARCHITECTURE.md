# RPI System - Architecture Overview

## System Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INITIATES /rpi                         │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   MAIN AGENT (Build)   │
                    │  Orchestrates Workflow │
                    └───────────┬───────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│   RESEARCH    │      │     PLAN      │      │  IMPLEMENT    │
│   Agent       │─────▶│    Agent      │─────▶│   Agent       │
│  (Opus 4.5)   │      │ (Sonnet 4.5)  │      │ (Sonnet 4.5)  │
└───────┬───────┘      └───────┬───────┘      └───────┬───────┘
        │                      │                      │
        │ Spawns               │ Creates              │ Executes
        ▼                      ▼                      ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│   @explore    │      │  Todo Items   │      │ Code Changes  │
│  (Haiku 4.5)  │      │  (tracking)   │      │   + Tests     │
└───────┬───────┘      └───────────────┘      └───────┬───────┘
        │                                              │
        │ Returns findings                             │
        ▼                                              ▼
┌───────────────────────────────────────┐    ┌───────────────┐
│   .tmp/research/current-research.md   │    │    VERIFY     │
│   - Files: paths & line numbers       │    │    Agent      │
│   - Patterns & conventions             │    │  (Opus 4.5)   │
│   - Integration points                 │◀───┤  READ-ONLY    │
│   - Dependencies                       │    └───────┬───────┘
└───────────────────────────────────────┘            │
                                                     │
                ┌────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────────┐
│         .tmp/verification/latest-report.md                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ✅ PASSED                                                │ │
│  │   - Type safety: PASS                                   │ │
│  │   - No hardcoded secrets: PASS                          │ │
│  │                                                          │ │
│  │ ⚠️ RECOMMENDATIONS                                       │ │
│  │   - Extract repeated logic                              │ │
│  │   - Add error handling to async calls                   │ │
│  │                                                          │ │
│  │ 🚨 CRITICAL (BLOCKS if any)                             │ │
│  │   - [None]                                              │ │
│  │                                                          │ │
│  │ Status: APPROVED WITH NOTES                             │ │
│  └─────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   If BLOCKED:         │
                    │   Fix critical issues │
                    │   Re-run /verify      │
                    │                       │
                    │   If APPROVED:        │
                    │   ✅ Ready to merge   │
                    └───────────────────────┘
```

## Agent Communication Flow

```
Main Agent
    │
    ├─ Spawns → Research Agent
    │           │
    │           ├─ May spawn → @explore (for large codebases)
    │           │               │
    │           │               └─ Returns: Compressed findings
    │           │
    │           └─ Writes → .tmp/research/current-research.md
    │
    ├─ Reads research snapshot
    │
    ├─ Spawns → Planner Agent
    │           │
    │           ├─ Reads → .tmp/research/current-research.md
    │           │
    │           ├─ Creates → .tmp/plans/current-plan.md
    │           │
    │           └─ Creates → Todo items (via todowrite)
    │
    ├─ User reviews plan
    │
    ├─ Switches to → Implement Agent (primary)
    │                │
    │                ├─ Reads → .tmp/plans/current-plan.md
    │                │
    │                ├─ Reads → Todo items (via todoread)
    │                │
    │                ├─ For each phase:
    │                │   ├─ Mark todo: in_progress
    │                │   ├─ Make code changes
    │                │   ├─ Run tests
    │                │   └─ Mark todo: completed
    │                │
    │                └─ Completes implementation
    │
    └─ Spawns → Verify Agent
                │
                ├─ Reads → Changed files
                │
                ├─ Checks → SOLID, security, type safety
                │
                ├─ Writes → .tmp/verification/latest-report.md
                │
                └─ Returns → APPROVED / APPROVED WITH NOTES / BLOCKED
```

## Context Management Strategy

```
┌────────────────────────────────────────────────────────────────┐
│                      TOKEN USAGE ZONES                          │
│                                                                 │
│  0%                                  40%                  100% │
│  │─────────────────────────────────────│─────────────────────│ │
│  │         SMART ZONE                  │     DUMB ZONE       │ │
│  │  ✅ Good decisions                  │  ❌ Poor decisions  │ │
│  │  ✅ Accurate tool calls             │  ❌ Hallucinations  │ │
│  │  ✅ Reliable execution              │  ❌ Context loss    │ │
│  └─────────────────────────────────────┴─────────────────────┘ │
└────────────────────────────────────────────────────────────────┘

Strategy: Stay in SMART ZONE through:
1. Sub-agent delegation (spawn @explore, @research, etc.)
2. Context compaction (compress findings into markdown)
3. Ephemeral storage (.tmp/ for session data)
4. Focused tool use (read specific files, not entire directories)
```

## Data Flow

```
User Input
    │
    ▼
┌─────────────────────┐
│  "Add email         │
│   verification"     │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │   Research   │
    │    Phase     │
    └──────┬───────┘
           │
           ▼
    .tmp/research/current-research.md
    ┌─────────────────────────────────┐
    │ # Research: Email Verification  │
    │                                 │
    │ ## Key Findings                 │
    │ - Auth system: src/auth/*.ts    │
    │ - Email service: src/email/*.ts │
    │ - User model: src/models/User.ts│
    │                                 │
    │ ## Integration Points           │
    │ - Registration: line 45         │
    │ - Login: line 120               │
    └────────────┬────────────────────┘
                 │
                 ▼
          ┌──────────────┐
          │     Plan     │
          │    Phase     │
          └──────┬───────┘
                 │
                 ▼
    .tmp/plans/current-plan.md
    ┌──────────────────────────────────┐
    │ # Implementation Plan            │
    │                                  │
    │ ## Phase 1: Update User Model    │
    │ - File: src/models/User.ts:15    │
    │ - Add: verificationToken field   │
    │ - Test: User.test.ts             │
    │                                  │
    │ ## Phase 2: Create Endpoint      │
    │ - File: src/api/verify.ts        │
    │ - Add: POST /verify/:token       │
    │ - Test: verify.test.ts           │
    │                                  │
    │ ## Phase 3: Send Email           │
    │ [...]                            │
    └────────────┬─────────────────────┘
                 │
                 ▼
          ┌──────────────┐
          │  Implement   │
          │    Phase     │
          └──────┬───────┘
                 │
                 ├─ Phase 1 ✅
                 ├─ Phase 2 ✅
                 ├─ Phase 3 ✅
                 │
                 ▼
           Code Changes
    ┌─────────────────────────┐
    │ src/models/User.ts      │
    │ src/api/verify.ts       │
    │ src/email/templates.ts  │
    │ tests/*.test.ts         │
    └────────────┬────────────┘
                 │
                 ▼
          ┌──────────────┐
          │    Verify    │
          │    Phase     │
          └──────┬───────┘
                 │
                 ▼
    .tmp/verification/latest-report.md
    ┌──────────────────────────────────┐
    │ # Verification Report            │
    │                                  │
    │ ✅ PASSED (8 checks)             │
    │ ⚠️ RECOMMENDATIONS (2)           │
    │ 🚨 CRITICAL (0)                  │
    │                                  │
    │ Status: APPROVED WITH NOTES      │
    └────────────┬─────────────────────┘
                 │
                 ▼
            ✅ Ready to Merge
```

## Standards Validation Pipeline

```
Code Changes
     │
     ▼
┌─────────────────────┐
│  Verify Agent       │
│  (Read-Only)        │
└──────────┬──────────┘
           │
           ├─────────────────────┐
           │                     │
           ▼                     ▼
    ┌───────────┐        ┌───────────┐
    │   SOLID   │        │ Security  │
    │ Principles│        │  Checks   │
    └─────┬─────┘        └─────┬─────┘
          │                    │
          ▼                    ▼
    - SRP: ✅             - Secrets: ✅
    - OCP: ✅             - SQL Inj: ✅
    - LSP: ✅             - XSS: ✅
    - ISP: ⚠️             - Auth: ✅
    - DIP: ✅             - Input: ⚠️
           │                    │
           └──────────┬─────────┘
                      │
                      ▼
              ┌───────────┐
              │   Type    │
              │  Safety   │
              └─────┬─────┘
                    │
                    ▼
              - Strict: ✅
              - No any: ✅
              - Types: ✅
                    │
                    └────────────┐
                                 │
                    ┌────────────┴──────────┐
                    │                       │
                    ▼                       ▼
            ┌───────────┐         ┌───────────────┐
            │ If 🚨      │         │ If ✅ or ⚠️   │
            │ CRITICAL   │         │ APPROVED      │
            └─────┬─────┘         └─────┬─────────┘
                  │                     │
                  ▼                     ▼
          ❌ BLOCKED              ✅ CAN MERGE
          Must fix issues        (with notes)
```

## File System Architecture

```
~/.config/opencode/              # GLOBAL: Base configuration
│
├── agent/                        # Agent definitions
│   ├── research.md               # → Research agent config
│   ├── plan.md                   # → Plan agent config
│   ├── implement.md              # → Implement agent config
│   ├── verify.md                 # → Verify agent config
│   └── explore.md                # → Explore agent config
│
├── command/                      # Custom slash commands
│   ├── rpi.md                    # → /rpi command
│   ├── research.md               # → /research command
│   ├── plan.md                   # → /planner command
│   ├── implement.md              # → /implement command
│   ├── verify.md                 # → /verify command
│   └── compact.md                # → /compact command
│
├── prompt/                       # System prompts
│   ├── research.txt              # → Research methodology
│   ├── plan.txt                  # → Planning methodology
│   └── verify-standards.txt      # → Verification standards
│
├── rules/                        # Verification rules
│   └── rpi-blocking-criteria.md  # → What blocks implementation
│
├── scripts/                      # Utility scripts
│   └── sync-config.sh            # → GitHub sync script
│
└── opencode.json                 # → Main OpenCode config

─────────────────────────────────────────────────────────────────

.opencode/                        # PROJECT: Project-specific config
└── standards/
    └── custom-standards.md       # → Project coding standards

─────────────────────────────────────────────────────────────────

.tmp/                            # EPHEMERAL: Session data (gitignored)
│
├── research/
│   ├── current-research.md      # → Active research snapshot
│   ├── research-metadata.json   # → Metadata
│   └── research-history/        # → Historical research
│
├── plans/
│   ├── current-plan.md          # → Active implementation plan
│   ├── plan-metadata.json       # → Metadata
│   └── plan-history/            # → Historical plans
│
└── verification/
    ├── latest-report.md         # → Most recent verification
    └── verify-history.md        # → Session verification log
```

## Model Selection Rationale

| Agent | Model | Why |
|-------|-------|-----|
| **Research** | Opus 4.5 | Deepest understanding, best at pattern recognition |
| **Plan** | Sonnet 4.5 | Balanced speed/accuracy, good at structured thinking |
| **Implement** | Sonnet 4.5 | Reliable execution, good code generation |
| **Verify** | Opus 4.5 | Most thorough, catches subtle issues |
| **Explore** | Haiku 4.5 | Fastest, cost-effective for simple queries |

## Blocking Decision Tree

```
                      Verify finds issue
                            │
                            ▼
                    ┌───────────────┐
                    │ Is it a       │
                    │ security      │
                    │ vulnerability?│
                    └───┬───────┬───┘
                        │       │
                    YES │       │ NO
                        │       │
                        ▼       ▼
                    ┌────┐   ┌──────────────┐
                    │BLOCK│   │ Is it a type │
                    │🚨   │   │ error?       │
                    └────┘   └──┬───────┬───┘
                                │       │
                            YES │       │ NO
                                │       │
                                ▼       ▼
                            ┌────┐   ┌──────────────┐
                            │BLOCK│   │ Is it an     │
                            │🚨   │   │ unhandled    │
                            └────┘   │ error?       │
                                     └──┬───────┬───┘
                                        │       │
                                    YES │       │ NO
                                        │       │
                                        ▼       ▼
                                    ┌────┐   ┌──────┐
                                    │BLOCK│   │ WARN │
                                    │🚨   │   │ ⚠️   │
                                    └────┘   └──────┘
```

## Summary

The RPI system is a comprehensive, production-ready implementation of:
- Context-aware AI development
- Research → Plan → Implement methodology
- Automatic sub-agent delegation
- Standards-based verification with blocking
- Mental alignment through human-readable artifacts

All components work together to keep AI agents in the "smart zone" while maintaining high code quality standards.
