# Agent Naming - Important Note

## Change Made

To avoid conflicts with OpenCode's built-in `plan` agent, we've renamed our planning agent:

- **Old**: `plan` agent / `/plan` command
- **New**: `planner` agent / `/planner` command

## Why?

OpenCode has built-in agents:
- `build` - Default primary agent (full write access)
- `plan` - Built-in planning agent (read-only analysis)

Our custom agent conflicted with the built-in `plan` agent, so we renamed it to `planner`.

## Updated Commands

| Old Command | New Command | Description |
|-------------|-------------|-------------|
| `/plan` | `/planner` | Create implementation plan from research |

The main `/rpi` workflow remains unchanged and will automatically use the `planner` agent.

## What Changed

### Files Renamed
- `~/.config/opencode/agent/plan.md` → `planner.md`
- `~/.config/opencode/command/plan.md` → `planner.md`

### Config Updated
- `opencode.json` now references `planner` instead of `plan`
- All documentation updated to use `/planner`

## Usage

```bash
# Full RPI workflow (no change)
/rpi

# Standalone planning (command renamed)
/planner "add email verification feature"

# Other commands (unchanged)
/research "understand auth system"
/implement
/verify
/compact
```

## No Action Required

If you haven't used the system yet, no action is needed. Everything is already updated.

If you have scripts or workflows that reference `/plan`, simply update them to use `/planner`.
