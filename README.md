# OpenCode RPI System

**Research → Plan → Implement** - A markdown-based agentic system for OpenCode implementing context-aware AI development.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

The RPI system operationalizes the concepts from Dex's "12 Factor Agents" talk, focusing on:
- **Context Compaction**: Staying in the "smart zone" (< 40% token usage)
- **Sub-agent Delegation**: Automatic spawning for exploration and analysis
- **Verification Blocking**: Standards validation that prevents bad code from shipping
- **Mental Alignment**: Human-readable research, plans, and verification reports

## Quick Start

```bash
# Clone the repository
git clone https://github.com/obiwormxlii/opencode-rpi-system.git

# Copy to OpenCode config directory
cp -r opencode-rpi-system/* ~/.config/opencode/

# Start OpenCode and use the system
opencode
/rpi
```

## Features

✅ **Project Initialization System** 🆕
- `/project-init` - Initialize comprehensive project structure
- **Greenfield**: Guided interview creates architecture docs, roadmap, and epics
- **Brownfield**: Analyzes existing codebase and generates documentation
- **Auto-tracking**: Progress updates based on git commits
- See [Project Init Guide](docs/PROJECT_INIT_GUIDE.md)

✅ **6 Specialized Agents**
- Project-Architect (Opus 4.5) - Greenfield project initialization 🆕
- Research (Opus 4.5) - Deep codebase understanding
- Planner (Sonnet 4.5) - Atomic implementation plans
- Implement (Sonnet 4.5) - Step-by-step execution
- Verify (Opus 4.5) - Standards validation with BLOCKING
- Explore (Haiku 4.5) - Fast exploration

✅ **7 Custom Commands**
- `/project-init` - Initialize project structure (new or existing) 🆕
- `/rpi [description]` - Full Research → Plan → Implement workflow 🔥
- `/research [topic]` - Analyze codebase and create research snapshot
- `/planner [task]` - Create detailed implementation plan
- `/implement` - Execute the implementation plan
- `/verify` - Validate code against standards
- `/compact` - Compress context into research snapshot

✅ **Standards Validation**
- SOLID principles
- Atomic design patterns (frontend)
- Security best practices
- Type safety enforcement
- Project-specific standards

## Documentation

- **[Complete Documentation](docs/README.md)** - Full system overview
- **[Setup Guide](docs/SETUP.md)** - Installation and configuration
- **[Quick Reference](docs/QUICKREF.md)** - Command cheat sheet
- **[Architecture](docs/ARCHITECTURE.md)** - System diagrams and design
- **[Changelog](docs/CHANGELOG.md)** - Version history

## Structure

```
.
├── agent/              # Agent definitions
│   ├── research.md
│   ├── planner.md
│   ├── implement.md
│   ├── verify.md
│   └── explore.md
├── command/            # Custom commands
│   ├── rpi.md
│   ├── research.md
│   ├── planner.md
│   ├── implement.md
│   ├── verify.md
│   └── compact.md
├── prompt/             # System prompts
│   ├── research.txt
│   ├── plan.txt
│   └── verify-standards.txt
├── rules/              # Verification rules
│   └── rpi-blocking-criteria.md
├── scripts/            # Utility scripts
│   └── sync-config.sh
├── opencode.json       # Main configuration
└── docs/               # Documentation
```

## Usage Example

```bash
# Start OpenCode
opencode

# Run the RPI workflow with arguments (recommended)
/rpi "Add email verification to user registration"

# Or run without arguments (interactive mode)
/rpi
# Then describe your feature when prompted

# The system will:
# 1. Research the codebase
# 2. Create an atomic implementation plan
# 3. Execute the plan step-by-step
# 4. Verify against standards (BLOCKS on critical issues)
```

### Usage Patterns

```bash
# Detailed feature request
/rpi "Add user authentication with JWT tokens. Must support refresh tokens and role-based access control"

# Bug fix
/rpi "Fix memory leak in dashboard component when unmounting"

# Refactoring
/rpi "Refactor payment processing to use strategy pattern"

# Quick task
/rpi "Add loading spinner to login button"
```

## Requirements

- [OpenCode](https://opencode.ai) installed and configured
- Claude API access (Opus, Sonnet, and Haiku models)
- Git (for version control)

## Installation

### Method 1: Direct Copy (Recommended)

```bash
# Clone this repository
git clone https://github.com/obiwormxlii/opencode-rpi-system.git
cd opencode-rpi-system

# Copy to OpenCode config directory
cp -r agent command prompt rules scripts opencode.json ~/.config/opencode/

# Verify installation
ls ~/.config/opencode/agent/
```

### Method 2: Symlink

```bash
# Clone this repository
git clone https://github.com/obiwormxlii/opencode-rpi-system.git

# Create symlinks
ln -s "$(pwd)/opencode-rpi-system/agent" ~/.config/opencode/agent
ln -s "$(pwd)/opencode-rpi-system/command" ~/.config/opencode/command
# ... (repeat for other directories)
```

### Method 3: Sync Script

```bash
# Set repository URL
export RPI_REPO_URL="https://github.com/obiwormxlii/opencode-rpi-system.git"

# Run setup
~/.config/opencode/scripts/sync-config.sh setup

# Pull updates anytime
~/.config/opencode/scripts/sync-config.sh pull
```

## Project Setup

For each project, create project-specific standards:

```bash
cd /your/project

# Create project config
mkdir -p .opencode/standards

# Copy template
cp ~/.config/opencode/templates/custom-standards.md .opencode/standards/

# Edit for your project
vim .opencode/standards/custom-standards.md

# Create ephemeral data directory
mkdir -p .tmp/{research,plans,verification}

# Add to .gitignore
echo ".tmp/" >> .gitignore
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## Credits

Based on concepts from:
- **Dex's "12 Factor Agents"** talk at AI Engineer Summit
- **OpenCode** architecture and documentation
- **Context Engineering** principles from the AI development community

## License

MIT License - See LICENSE file for details

## Support

- **Documentation**: See [docs/](docs/) directory
- **Issues**: [GitHub Issues](https://github.com/obiwormxlii/opencode-rpi-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/obiwormxlii/opencode-rpi-system/discussions)

## Version

Current version: **v1.0.1**

See [CHANGELOG.md](docs/CHANGELOG.md) for version history.

---

**Happy coding with RPI!** 🚀
