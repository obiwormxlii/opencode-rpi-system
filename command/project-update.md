---
description: Update project progress and task completion status
agent: build
---

# Project Update

I'll analyze recent git commits and update your project STATUS.md to reflect completed tasks.

This command triggers the **project-manager** agent to:
1. **Analyze git history** - Review commits since last status update
2. **Detect completed tasks** - Match commits to task acceptance criteria
3. **Validate completion** - Check if criteria are met (with confidence scoring)
4. **Update STATUS.md** - Mark tasks complete and update progress percentages
5. **Report progress** - Show what was completed and suggest next steps

## Usage Modes

### Automatic (Default)
```bash
/project-update
```
Analyzes commits since last update, auto-detects completions, asks for confirmation when uncertain.

### Manual Task Marking
```bash
/project-update task-003-002
```
Manually mark specific task as complete (will validate and ask for confirmation).

### Multiple Tasks
```bash
/project-update task-003-001 task-003-002 task-003-003
```
Mark multiple tasks as complete in one operation.

### Custom Time Range
```bash
/project-update --since "7 days ago"
```
Analyze commits from specific time period.

## What Gets Updated

- **STATUS.md** - Task statuses, progress percentages, completion dates
- **Progress tracking** - Epic/phase completion percentages
- **Next steps** - Recommended tasks based on dependencies
- **History snapshots** - Archives completed epics/phases to `.opencode/project/planning/history/`

## Detection Confidence

The project-manager uses moderate sensitivity:

**High confidence (≥70%)** → Auto-mark complete:
- Commit explicitly references task number (e.g., "feat: complete task-003-002")
- All acceptance criteria files were modified
- Commit contains completion keywords ("complete", "finish", "closes")

**Medium confidence (40-69%)** → Ask for confirmation:
- Most but not all criteria met
- Related files modified but no explicit task reference
- Ambiguous commit messages

**Low confidence (<40%)** → Ignore:
- Unrelated file changes
- Minor fixes/refactors without task context
- WIP commits

## Example Session

```
User: /project-update

Agent: Analyzing commits since 2025-01-10...

Found 3 commits:
1. abc123 - "feat: complete task-003-002 - password hashing" (2025-01-15)
2. def456 - "add user registration form validation" (2025-01-14)
3. ghi789 - "fix typo in button" (2025-01-14)

✅ Auto-detected completion: task-003-002 (95% confidence)
  - All 4 acceptance criteria files modified
  - Commit explicitly references task
  - Evidence: src/auth/password.py, tests/test_auth.py

🤔 Possible completion: task-003-003 (65% confidence)
  - Form component created ✓
  - Validation added ✓
  - Error handling unclear
  - Loading states unclear
  - Tests not found ✗
  
  Mark task-003-003 as complete? (y/n/partial)

User: partial

Agent: Updated STATUS.md:
  - task-003-002: ✅ Completed (2025-01-15)
  - task-003-003: 🔄 Partially complete (3/5 criteria)
  - Epic 003 Phase 1: 100% (4/4 tasks)
  - Epic 003 Phase 2: 40% (2/5 tasks)

Next recommended: Complete task-003-003 (registration form)
```

## Prerequisites

Requires `.opencode/project/` structure created by `/project-init`.

If not found, you'll be prompted to initialize the project first.

## Notes

- Updates are based on git commits - ensure work is committed before running
- Completion dates use git commit timestamps
- Task dependencies are respected when suggesting next steps
- History snapshots automatically created when epics/phases complete
