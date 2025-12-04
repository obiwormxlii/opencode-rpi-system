# Project Initialization System - User Guide

## Overview

The Project Initialization System creates comprehensive project documentation and structure for both **greenfield** (new) and **brownfield** (existing) projects. It integrates seamlessly with the RPI (Research → Plan → Implement) workflow.

## Quick Start

### Initialize a New Project

```bash
/project-init
```

You'll be asked if this is a greenfield or brownfield project:

- **Greenfield**: New project - I'll interview you about requirements
- **Brownfield**: Existing project - I'll analyze your codebase

## Greenfield Projects (New)

### What to Expect

The `project-architect` agent will guide you through an 8-phase interview:

#### Phase 1: Project Fundamentals (5-7 questions)
- Project name and description
- Primary goal and value proposition
- Target users
- Expected scale (10 users? 10k? 1M?)
- Timeline and MVP definition

#### Phase 2: Technical Stack (4-6 questions)
- Backend language/framework
- Frontend framework
- Database choice
- Authentication strategy
- Hosting platform
- External services

#### Phase 3: Database Design (conversational)
- Core entities (Users, Products, Orders, etc.)
- Relationships (User has many Orders)
- Special data needs (real-time, file uploads, etc.)

The agent will generate an Entity Relationship Diagram for your review.

#### Phase 4: API Design
- API style (REST, GraphQL, tRPC)
- Key endpoints
- Authentication approach

#### Phase 5: Frontend Architecture
- Page structure
- Component patterns (Atomic Design, feature-based)
- State management (Context, Redux, etc.)
- Design system

#### Phase 6: Infrastructure & DevOps
- Deployment strategy (Docker, serverless, VPS)
- CI/CD platform (GitHub Actions, etc.)
- Environments (dev, staging, prod)
- Monitoring and logging

#### Phase 7: Project Breakdown
- Define MVP scope
- Propose epic structure (3-10 epics)
- Break epics into phases
- Create day-sized tasks

#### Phase 8: Custom Agents
- Review standard RPI agents
- Discuss project-specific needs
- Create custom agents if needed

### Example Session

```
User: /project-init

Agent: Is this a greenfield (new) or brownfield (existing) project?

User: greenfield

Agent: Great! Let's start with the fundamentals.

**Phase 1: Project Fundamentals**

1. What is your project called and what does it do?

User: TaskFlow - A modern task management app for remote teams

Agent: Excellent! What's the main problem TaskFlow solves?

User: Remote teams struggle with async collaboration and task visibility

Agent: Who are your target users?

User: Small to medium remote teams (5-50 people)

Agent: What scale are you expecting?

User: Let's start with 1,000 users and design to scale to 100k

Agent: When do you need an MVP?

User: 3 months

[Interview continues through all 8 phases...]

Agent: Based on our discussion, I'm creating your project structure...

✓ Created .opencode/project/INDEX.md
✓ Created .opencode/project/architecture/overview.md
✓ Created .opencode/project/architecture/database-schema.md
✓ Created .opencode/project/planning/roadmap.md
✓ Created 5 epics with 23 tasks total

Your project is initialized! Run `/project-status` to see what to work on first.
```

### What Gets Created

After initialization, you'll have:

```
.opencode/
├── project/
│   ├── INDEX.md                          # Project overview & navigation
│   ├── AGENTS.md                         # Project-specific instructions
│   ├── opencode.json                     # Project config
│   │
│   ├── architecture/
│   │   ├── _CONTEXT.md
│   │   ├── overview.md                   # System design
│   │   ├── database-schema.md            # ERD & entities
│   │   ├── api-design.md                 # Endpoints & contracts
│   │   ├── frontend-architecture.md      # UI structure
│   │   └── infrastructure.md             # Deployment & DevOps
│   │
│   └── planning/
│       ├── _CONTEXT.md
│       ├── roadmap.md                    # Project timeline
│       └── epics/
│           ├── epic-001-authentication/
│           │   ├── _CONTEXT.md
│           │   ├── overview.md
│           │   ├── STATUS.md
│           │   ├── phase-1-backend/
│           │   │   ├── task-001-setup-db.md
│           │   │   ├── task-002-auth-endpoints.md
│           │   │   └── ...
│           │   └── phase-2-frontend/
│           │       └── ...
│           └── epic-002-task-management/
│               └── ...
```

## Brownfield Projects (Existing)

### What to Expect

The `project-archaeologist` agent will analyze your codebase through a 6-step process:

#### Step 1: Documentation Discovery
- Search for README, CONTRIBUTING, ARCHITECTURE docs
- Parse existing documentation
- Check for ADRs (Architecture Decision Records)

#### Step 2: File Structure Analysis
- Identify project type (monolith, microservices, monorepo)
- Detect architectural patterns (MVC, feature-based, etc.)
- Calculate language breakdown

#### Step 3: Dependency Analysis
- Parse package.json, requirements.txt, etc.
- Identify frameworks and versions
- Detect database drivers, auth libraries, etc.

#### Step 4: Database Schema Extraction
- Parse migration files (Alembic, Knex, Rails, Django)
- Extract entities and relationships from ORM models
- Generate ERD diagram

#### Step 5: Git History Analysis
- Project age and commit frequency
- Top contributors
- Branching strategy detection
- Commit message patterns

#### Step 6: Architecture Synthesis
- Combine all analysis into comprehensive docs
- Reverse-engineer API design
- Propose improvement roadmap

### Interactive Refinement

After analysis, the agent will:
- Present findings for your review
- Ask clarifying questions about ambiguities
- Allow corrections to generated docs
- Get your approval before finalizing

### Example Session

```
User: /project-init

Agent: Is this a greenfield (new) or brownfield (existing) project?

User: brownfield

Agent: I'll analyze your existing codebase...

Step 1/6: Discovering documentation...
  ✓ Found README.md
  ✓ Found docs/api.md
  
Step 2/6: Analyzing file structure...
  ✓ Detected: Feature-based architecture
  ✓ Languages: TypeScript (60%), Python (40%)
  
Step 3/6: Analyzing dependencies...
  ✓ Framework: React + FastAPI
  ✓ Database: PostgreSQL (pg driver)
  ✓ Auth: Custom JWT
  
Step 4/6: Extracting database schema...
  ✓ Found 12 entities
  ✓ Generated ERD
  
Step 5/6: Analyzing git history...
  ✓ Project age: 487 days
  ✓ 342 commits, 5 contributors
  ✓ Strategy: Feature-branch workflow
  
Step 6/6: Synthesizing architecture docs...
  ✓ Created comprehensive documentation

Let me show you what I found. Does this accurately represent your system?
[Shows overview.md preview]

User: Yes, but we also use Redis for caching

Agent: Good catch! Updating infrastructure.md...

✓ Project documentation complete!
```

## After Initialization

### Check Project Status

```bash
/project-status
```

Shows:
- Current epic and phase
- Next recommended task
- Overall completion percentage
- Any blockers

### Start Development

```bash
/rpi "implement task-001"
```

The RPI workflow will now:
- **Research** reads `.opencode/project/architecture/` for context
- **Planner** references task acceptance criteria
- **Implement** updates task STATUS automatically
- **Verify** checks against project-specific standards

### Update Progress

Progress updates automatically after commits with keywords like:
- `feat: complete task-001`
- `closes #task-001`
- `milestone` or `epic complete`

Or manually run:

```bash
/project-update
```

## Project Structure Reference

### INDEX.md
Main navigation file with:
- Quick links to all docs
- Current project status
- Technology stack summary
- Quick command reference

### AGENTS.md
Project-specific agent instructions:
- Project overview and context
- Architecture summary
- Key patterns and conventions
- Links to detailed docs

### Architecture Docs

**overview.md**
- High-level system design
- Component interactions
- Technology stack details
- System diagrams

**database-schema.md**
- Entity definitions
- Relationships (ERD)
- Indexes and constraints
- Migration strategy

**api-design.md**
- Endpoint specifications
- Request/response examples
- Authentication details
- Error handling

**frontend-architecture.md**
- Component hierarchy
- State management approach
- Routing structure
- Styling conventions

**infrastructure.md**
- Deployment procedures
- Environment configuration
- CI/CD pipeline
- Monitoring setup

### Planning Docs

**roadmap.md**
- Epic overview and timeline
- Current focus
- Completed and pending work
- Milestones

**Epic Structure**
Each epic contains:
- `overview.md` - Goals and success criteria
- `STATUS.md` - Progress tracking
- `phase-N-name/` - Phases with tasks

**Task Files**
Each task includes:
- Goal and context
- Implementation approach
- Acceptance criteria
- Testing requirements
- RPI session history

## Best Practices

### For Greenfield Projects

1. **Be Specific**: The more details you provide, the better the documentation
2. **Start Simple**: Choose proven technologies for MVP
3. **Define MVP Clearly**: Cut scope aggressively to ship faster
4. **Review Epics**: Make sure the breakdown makes sense for your team
5. **Iterate**: You can update docs as project evolves

### For Brownfield Projects

1. **Clean Up First**: Remove dead code before analysis
2. **Review Findings**: Agent may miss project-specific patterns
3. **Correct Misunderstandings**: Provide clarifications during refinement
4. **Document Gaps**: Add missing context that analysis couldn't capture
5. **Prioritize Improvements**: Use generated roadmap to plan tech debt work

### Working with RPI Workflow

1. **Always Check Status**: Run `/project-status` before starting work
2. **Follow Task Order**: Tasks are designed to build on each other
3. **Update Regularly**: Run `/project-update` after completing tasks
4. **Reference Architecture**: Read relevant architecture docs before implementation
5. **Keep Docs Updated**: Update architecture docs when design changes

## Troubleshooting

### "No project structure found"
- Run `/project-init` first to initialize structure

### "Task file not found"
- Check task ID format: `task-001` not `task-1`
- Verify you're in the correct epic directory

### "Analysis failed to find schema"
- Brownfield analysis supports: Django, Prisma, SQLAlchemy (partially)
- You may need to manually create database-schema.md

### Agent seems confused during interview
- Provide more specific answers
- Ask agent to clarify the question
- You can always go back and revise answers

### Generated roadmap too aggressive/conservative
- Work with agent to adjust epic breakdown
- Combine or split epics as needed
- Remember: tasks should be ~1 RPI session each

## Advanced Usage

### Custom Agents

If your project needs specialized agents (e.g., `database-migrator`, `component-generator`), discuss during Phase 8 of initialization. These will be:
- Defined in `.opencode/opencode.json`
- Documented in `.opencode/AGENTS.md`
- Available as commands (e.g., `/migrate-schema`)

### Project-Specific Standards

Add custom coding standards to:
```
.opencode/standards/custom-standards.md
```

The `verify` agent will check implementations against these standards.

### History Tracking

The system automatically creates snapshots in:
```
.opencode/project/planning/.history/
```

These track changes to roadmap and epics over time.

### Manual Documentation Updates

You can edit any doc in `.opencode/project/` manually. The system will respect your changes and build on them.

## Integration with Git

### Commit Messages

Use these patterns for auto-tracking:

**Complete a task:**
```bash
git commit -m "feat: complete task-001 - setup database schema"
```

**Close a task:**
```bash
git commit -m "feat: add user authentication

closes #task-002"
```

**Milestone reached:**
```bash
git commit -m "feat: complete authentication epic

All auth features implemented and tested. Ready for production."
```

### Branching Strategy

The system adapts to your branching strategy:
- **Feature branches**: One branch per task/epic
- **Trunk-based**: Direct commits to main
- **Git-flow**: Feature/develop/main workflow

## Next Steps

After initialization:
1. Review generated documentation
2. Run `/project-status` to see first task
3. Start development with `/rpi "implement task-001"`
4. Commit frequently with descriptive messages
5. Let the system track your progress automatically

## Getting Help

- Check architecture docs for system context
- Review task files for specific requirements
- Use `/research` to understand codebase
- Refer to [RPI workflow docs](QUICKREF.md) for commands

Happy building! 🚀