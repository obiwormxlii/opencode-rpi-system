# RPI System - Setup Guide

## Prerequisites

1. **OpenCode** installed and configured
   - Install: `curl -fsSL https://opencode.ai/install | bash`
   - Configure: Run `opencode` and follow `/connect` prompts

2. **Claude Pro subscription** (recommended)
   - The system uses Claude Opus 4.5, Sonnet 4.5, and Haiku 4.5

## Installation Steps

### 1. Base Configuration (Global)

The base configuration is already set up in `~/.config/opencode/`:

```bash
~/.config/opencode/
├── agent/          # 5 agent definitions
├── command/        # 6 custom commands
├── prompt/         # 3 system prompts
├── rules/          # Blocking criteria
└── opencode.json   # Main config file
```

To verify installation:
```bash
ls -la ~/.config/opencode/agent/
```

You should see: `research.md`, `plan.md`, `implement.md`, `verify.md`, `explore.md`

### 2. Project Configuration

For each project, set up project-specific configuration:

```bash
cd /your/project
mkdir -p .opencode/standards
```

Copy the template:
```bash
cp ~/.config/opencode/templates/custom-standards.md .opencode/standards/
```

Or manually create `.opencode/standards/custom-standards.md` with your project's:
- Technology stack
- Architectural patterns
- Coding standards
- Testing requirements

### 3. Ephemeral Data Directory

Create the `.tmp/` directory structure:

```bash
mkdir -p .tmp/{research/research-history,plans/plan-history,verification}
```

Add to `.gitignore`:
```bash
echo ".tmp/" >> .gitignore
```

### 4. Verify Installation

Start OpenCode:
```bash
opencode
```

Test the RPI commands:
```
/help
```

You should see:
- `/rpi` - Research → Plan → Implement workflow
- `/research` - Analyze codebase
- `/planner` - Create implementation plan
- `/implement` - Execute plan
- `/verify` - Validate standards
- `/compact` - Compress context

## GitHub Sync (Optional)

To sync your base configuration with a GitHub repository:

### Initial Setup

1. Create a new GitHub repository (e.g., `opencode-rpi-config`)

2. Set the repository URL:
```bash
export RPI_REPO_URL="https://github.com/yourusername/opencode-rpi-config.git"
```

3. Initialize and push:
```bash
~/.config/opencode/scripts/sync-config.sh setup
~/.config/opencode/scripts/sync-config.sh push
```

### Ongoing Sync

Push changes to GitHub:
```bash
~/.config/opencode/scripts/sync-config.sh push
```

Pull updates from GitHub:
```bash
~/.config/opencode/scripts/sync-config.sh pull
```

Check status:
```bash
~/.config/opencode/scripts/sync-config.sh status
```

## Testing the System

### Test 1: Simple Research

```
User: /research "find all authentication-related files"
```

Check output in `.tmp/research/current-research.md`

### Test 2: Create a Plan

```
User: /planner "add a new API endpoint for user profile"
```

Check output in `.tmp/plans/current-plan.md`

### Test 3: Full RPI Workflow

```
User: /rpi
User: "Add email validation to the user registration form"
```

The system should:
1. Research the codebase
2. Create a detailed plan
3. Ask for approval
4. Implement the changes
5. Run verification

## Configuration Options

### Model Selection

Edit `~/.config/opencode/opencode.json` to change models:

```json
{
  "agent": {
    "research": {
      "model": "anthropic/claude-opus-4-5"
    }
  }
}
```

Available models:
- `claude-opus-4-5` - Best for research and verification
- `claude-sonnet-4-5` - Balanced for planning and implementation
- `claude-haiku-4-5` - Fast for exploration

### Temperature Settings

Adjust agent creativity:

```json
{
  "agent": {
    "research": {
      "temperature": 0.1  // Very focused (0.0-0.2)
    }
  }
}
```

### Tool Permissions

Control which tools agents can use:

```json
{
  "agent": {
    "verify": {
      "tools": {
        "write": false,
        "edit": false,
        "bash": true
      }
    }
  }
}
```

## Troubleshooting

### Issue: Commands not showing up

**Solution**: Reload OpenCode configuration
```bash
# Restart OpenCode
```

### Issue: Agents not writing to .tmp/

**Solution**: Ensure directories exist
```bash
mkdir -p .tmp/{research,plans,verification}
```

### Issue: Verification always blocking

**Solution**: Review blocking criteria
```bash
cat ~/.config/opencode/rules/rpi-blocking-criteria.md
```

Adjust project standards:
```bash
vim .opencode/standards/custom-standards.md
```

### Issue: Context getting too large

**Solution**: Use manual compaction
```
/compact
```

Or check that agents are delegating to sub-agents properly.

### Issue: Research not finding files

**Solution**: Check `.gitignore` and `.ignore` files

Create `.ignore` to include specific paths:
```bash
echo "!node_modules/" >> .ignore
```

## Next Steps

1. **Customize Project Standards**: Edit `.opencode/standards/custom-standards.md`
2. **Test on Real Features**: Try `/rpi` on an actual feature
3. **Review Outputs**: Check `.tmp/` directories after each phase
4. **Iterate on Prompts**: Customize `~/.config/opencode/prompt/` if needed
5. **Share with Team**: Commit `.opencode/` to your project repo

## Resources

- [OpenCode Documentation](https://opencode.ai/docs)
- [12 Factor Agents Talk](https://www.youtube.com/watch?v=...) (Dex's talk)
- [RPI System README](./README.md)
- [Custom Standards Template](./.opencode/standards/custom-standards.md)

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting)
2. Review [OpenCode docs](https://opencode.ai/docs)
3. Check `.tmp/` logs for agent output
4. Review verification reports for blocking issues

## Updates

To update the RPI system:
```bash
cd ~/.config/opencode
git pull origin main  # If using GitHub sync
```

Or manually update agent/command/prompt files as needed.
