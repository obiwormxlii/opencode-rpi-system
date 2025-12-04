# RPI System - Changelog

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

- **v1.0.1** (2025-01-04): Agent naming fix
- **v1.0.0** (2025-01-04): Initial release
