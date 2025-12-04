# RPI System - Changelog

## [2.0.0] - 2025-12-04 🚀

### Added - Project Initialization & RPI Integration

**Major new features**: 
1. Comprehensive project initialization for both greenfield and brownfield projects
2. Full RPI integration with project-aware research, planning, and verification
3. Automatic progress tracking after implementation

#### New Agents
- **project-architect** - Guide greenfield project initialization through 8-phase structured interview
- **project-archaeologist** - Analyze existing codebases and reverse-engineer documentation
- **project-manager** - Track progress and update planning documents

#### New Commands
- `/project-init` - Initialize comprehensive project structure
- `/project-status` - Show current project progress
- `/project-update` - Update tracking after commits

#### Project Structure Generation
Creates `.opencode/project/` with:
- **INDEX.md** - Main navigation and project overview
- **AGENTS.md** - Project-specific agent instructions
- **architecture/** - 5 comprehensive architecture documents
  - overview.md - System design and components
  - database-schema.md - ERD and entity documentation
  - api-design.md - Endpoint specifications
  - frontend-architecture.md - UI structure and patterns
  - infrastructure.md - Deployment and DevOps
- **planning/** - Project roadmap and task breakdown
  - roadmap.md - Epic timeline and milestones
  - epics/epic-NNN-name/ - Epic breakdown with phases and tasks
  - .history/ - Historical snapshots

#### Templates
- 14 markdown templates for all project documentation
- Detailed placeholders with examples
- Supports both greenfield and brownfield workflows

#### Python Analysis Scripts
- **analyze_dependencies.py** - Parse package managers (npm, pip, etc.)
- **analyze_git_history.py** - Extract commit patterns and contributors
- **extract_database_schema.py** - Parse Django/Prisma models
- **generate_erd.py** - Create Mermaid ERD diagrams
- **update_project_status.py** - Auto-track progress from git commits

#### Auto-Tracking System (Epic 004)
- **project-manager agent** - Tracks task completion and maintains STATUS.md
- Monitors git commits for completion keywords
- Updates task STATUS automatically with moderate sensitivity (70% confidence threshold)
- Recalculates epic progress percentages
- Creates history snapshots on epic/phase completion
- Provides velocity metrics and completion projections

#### RPI Integration (Epic 005)
- **research agent** - Now checks `.opencode/project/architecture/` first before code exploration
- **plan agent** - References task acceptance criteria and validates plan satisfies all criteria
- **verify agent** - Checks project-specific standards from `.opencode/project/AGENTS.md`
- **Auto-update after /implement** - Automatically triggers project-manager to update progress
- Closes feedback loop: Plan → Research → Implement → Verify → **Auto-Update** → Next Plan
- Moderate sensitivity: `feat: complete X`, `closes #task-NNN`, `milestone`

#### Documentation
- **PROJECT_INIT_GUIDE.md** - Complete user guide for greenfield/brownfield workflows
- **PROJECT_SYSTEM.md** (planned) - System architecture documentation
- Updated README, QUICKREF with new commands

### Features
- **Greenfield Interview**: 8-phase semi-structured interview for new projects
- **Epic/Phase/Task Structure**: Day-sized tasks optimized for RPI workflow
- **Numbered Epics**: epic-001-authentication format for organization
- **Task Templates**: Detailed task files with goals, context, acceptance criteria
- **Architecture Documentation**: Comprehensive system design docs
- **RPI Integration**: Research/planner/implement read project context automatically
- **History Tracking**: Snapshot system for audit trails

### Technical Details
- Temperature 0.3 for project-architect (conversational but structured)
- Opus 4.5 model for architectural decisions
- JSON storage for interview responses
- Mermaid diagram generation
- GitPython integration for commit analysis

### Breaking Changes
None. Fully backward compatible. Existing RPI workflow unchanged.

---

## [1.0.1] - 2025-01-04

### Changed
- **BREAKING**: Renamed `plan` agent to `planner` to avoid conflict with OpenCode's built-in `plan` agent
- **BREAKING**: Renamed `/plan` command to `/planner`

### Fixed
- Agent naming conflict with OpenCode built-in agents

### Migration Guide
If you were using `/plan`, simply use `/planner` instead:
```bash
# Old
/plan "add feature"

# New
/planner "add feature"
```

The main `/rpi` workflow remains unchanged.

---

## [1.0.0] - 2025-01-04

### Added
- Initial release of RPI (Research → Plan → Implement) system
- 5 agents: research, planner, implement, verify, explore
- 6 commands: /rpi, /research, /planner, /implement, /verify, /compact
- 3 system prompts with detailed methodologies
- Blocking verification for CRITICAL issues
- SOLID principles validation
- Security standards checking
- Type safety enforcement
- Context management and compaction
- Sub-agent delegation system
- Todo list integration for progress tracking
- Session-based ephemeral data structure
- Comprehensive documentation (README, SETUP, QUICKREF, ARCHITECTURE)
- GitHub sync utility script

### Features
- **Context Engineering**: Stay in "smart zone" (<40% token usage)
- **Automatic Delegation**: Spawn sub-agents for exploration
- **Verification Blocking**: CRITICAL issues prevent implementation
- **Standards Validation**: SOLID, security, type safety, atomic design
- **Mental Alignment**: Human-readable research/plans/reports
- **Model Optimization**: Right model for each task (Opus/Sonnet/Haiku)

### Documentation
- README.md - Complete system overview
- SETUP.md - Installation and configuration guide
- QUICKREF.md - Command reference and quick tips
- ARCHITECTURE.md - Visual system diagrams
- IMPLEMENTATION_SUMMARY.md - Build details
- MIGRATION_NOTE.md - Agent naming change explanation

### Configuration Files
- opencode.json - Main OpenCode configuration
- Agent definitions in ~/.config/opencode/agent/
- Command definitions in ~/.config/opencode/command/
- System prompts in ~/.config/opencode/prompt/
- Blocking criteria in ~/.config/opencode/rules/

### Project Templates
- .opencode/standards/custom-standards.md - Project-specific standards
- .tmp/ directory structure for ephemeral data
- .gitignore for temporary files

---

## Version History

- **v2.0.0** (2025-12-04): Project initialization system (greenfield)
- **v1.0.1** (2025-01-04): Agent naming fix
- **v1.0.0** (2025-01-04): Initial release
