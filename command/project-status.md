---
description: Display current project progress and status summary
agent: build
---

# Project Status

I'll provide a comprehensive summary of your current project status, progress metrics, and recommended next steps.

This command triggers the **project-manager** agent to:
1. **Read STATUS.md** - Load current project state
2. **Calculate metrics** - Progress percentages, velocity, projections
3. **Identify active work** - Current tasks in progress
4. **Show recent completions** - Recently finished tasks
5. **Suggest next steps** - Recommended tasks based on dependencies

## Usage

```bash
/project-status
```

Shows full status report including all epics, active work, recent completions, and next steps.

### Focused Views

```bash
/project-status --epic epic-003
```
Show status for specific epic only.

```bash
/project-status --recent 7
```
Show completions from last 7 days.

```bash
/project-status --next
```
Show only recommended next tasks (useful for quick planning).

## Example Output

```markdown
## Project Status (as of 2025-01-15)

### Overview
- Total Epics: 8
- Completed Epics: 1 (12.5%)
- Total Tasks: 87
- Completed Tasks: 23 (26.4%)
- Estimated Completion: 2025-03-20 (based on current velocity)

### Current Epic: 003 - User Management
Progress: 58% complete (7/12 tasks)

**Active Work**
- 🔄 task-003-003 - User registration form components
  - Status: IN PROGRESS (started 2025-01-14)
  - Acceptance: 3/5 criteria completed
  - Estimated: 1 RPI session remaining

**Recently Completed** (Last 7 Days)
- ✅ task-003-002 - Password hashing and validation (2025-01-15)
  - Implemented bcrypt with salt rounds
  - Added password strength validation
  - Created comprehensive unit tests
  
- ✅ task-003-001 - User registration API endpoints (2025-01-12)
  - POST /api/users/register endpoint
  - Email uniqueness validation
  - Rate limiting implementation

**Pending Tasks**
- ⏳ task-003-004 - Login form and session management
  - Depends on: task-003-003
  - Estimated: 1 RPI session
  
- ⏳ task-003-005 - User profile page components
  - Depends on: task-003-004
  - Estimated: 1 RPI session

### Next Recommended Tasks

1. **task-003-003** - Complete user registration form (PRIORITY)
   - Currently in progress
   - Remaining: Error display, loading states, component tests
   - Blocks: task-003-004, task-003-005
   
2. **task-003-004** - Login form and session management
   - Ready to start once 003-003 completes
   - Critical path item
   
3. **task-004-001** - Task model and database schema
   - Can be started in parallel (different epic)
   - No blockers

### Velocity Metrics

**Last 7 Days**
- Tasks completed: 2
- Average: 0.29 tasks/day
- Trend: Stable

**Projections** (based on 0.29 tasks/day)
- Epic 003 completion: ~8 days (5 tasks remaining)
- Project completion: ~220 days (64 tasks remaining)
- Next milestone: Epic 004 start (~2025-01-23)

### Blockers

None currently

### Epic Summary

✅ **Epic 001 - Project Setup** (100%)
- 5/5 tasks completed
- Completed: 2025-01-10

✅ **Epic 002 - Database Design** (100%)
- 8/8 tasks completed
- Completed: 2025-01-11

🔄 **Epic 003 - User Management** (58%)
- 7/12 tasks completed
- In Progress: Phase 2 (Frontend)
- Estimated completion: 2025-01-23

⏳ **Epic 004 - Task Management Core** (0%)
- 0/15 tasks started
- Estimated start: 2025-01-23

⏳ **Epic 005 - Team Collaboration** (0%)
⏳ **Epic 006 - Notifications** (0%)
⏳ **Epic 007 - Reporting & Analytics** (0%)
⏳ **Epic 008 - Polish & Performance** (0%)
```

## Quick Commands

**What should I work on next?**
```bash
/project-status --next
```

**How much progress this week?**
```bash
/project-status --recent 7
```

**When will we finish Epic 003?**
```bash
/project-status --epic epic-003 --verbose
```

## Status Indicators

- ✅ **Completed** - All acceptance criteria met
- 🔄 **In Progress** - Work actively happening
- ⏳ **Pending** - Not yet started
- ⚠️ **Blocked** - Waiting on dependencies
- 🔴 **At Risk** - Behind schedule or has issues

## Metrics Explained

**Progress Percentage**: (Completed tasks / Total tasks) × 100

**Velocity**: Average tasks completed per day (last 7 days)

**Projected Completion**: (Remaining tasks / Velocity) + Current date

**Critical Path**: Longest sequence of dependent tasks to project completion

## Prerequisites

Requires `.opencode/project/` structure created by `/project-init`.

If not found, you'll be prompted to initialize the project first.

## Notes

- Status is read from STATUS.md (use `/project-update` to refresh)
- Velocity calculations based on git commit timestamps
- Projections assume consistent velocity (actual may vary)
- Dependency tracking based on task files' "Depends On" sections
