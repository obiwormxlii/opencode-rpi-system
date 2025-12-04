#!/usr/bin/env python3
"""
Project Status Update Script

Analyzes git commits since last update and determines if project docs need updating.

Triggers on commit messages containing:
- "feat: complete X" or "feat: finish X"
- "closes #task-NNN" or "closes task-NNN"
- Keywords: "milestone", "epic complete", "phase complete"

Updates:
- Task STATUS.md files
- Epic progress calculations
- Roadmap current status
- Creates history snapshots
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    from git import Repo
except ImportError:
    print("ERROR: GitPython not installed. Install with: pip install GitPython")
    exit(1)


@dataclass
class CommitInfo:
    """Represents a single commit."""
    hash: str
    message: str
    author: str
    date: datetime
    

@dataclass
class TaskUpdate:
    """Represents a task status update."""
    task_id: str
    epic_id: str
    phase_id: str
    new_status: str
    commit_hash: str
    commit_message: str


# Moderate sensitivity patterns
COMPLETION_PATTERNS = [
    r'feat:\s*complete\s+(.+)',
    r'feat:\s*finish\s+(.+)',
    r'complete\s+task[- ](\d+)',
    r'finish\s+task[- ](\d+)',
    r'epic\s+complete',
    r'phase\s+complete',
    r'milestone',
]

TASK_REFERENCE_PATTERNS = [
    r'closes\s+#task[- ](\d+)',
    r'closes\s+task[- ](\d+)',
    r'task[- ](\d+)',
]


def get_last_update_time(project_dir: str = '.opencode/project') -> Optional[str]:
    """
    Get timestamp of last project update.
    
    Args:
        project_dir: Path to project directory
        
    Returns:
        ISO timestamp string or None
    """
    timestamp_file = Path(project_dir) / '.last_update'
    
    if timestamp_file.exists():
        return timestamp_file.read_text().strip()
    
    return None


def save_last_update_time(project_dir: str = '.opencode/project'):
    """
    Save current timestamp as last update time.
    
    Args:
        project_dir: Path to project directory
    """
    timestamp_file = Path(project_dir) / '.last_update'
    timestamp_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp_file.write_text(datetime.now().isoformat())


def get_commits_since(repo_path: str = '.', since: Optional[str] = None) -> List[CommitInfo]:
    """
    Get commits since specified time.
    
    Args:
        repo_path: Path to git repository
        since: ISO timestamp to get commits since
        
    Returns:
        List of CommitInfo objects
    """
    repo = Repo(repo_path)
    
    if since:
        commits = list(repo.iter_commits(f'--since="{since}"'))
    else:
        # Get last 10 commits if no timestamp
        commits = list(repo.iter_commits(max_count=10))
    
    return [
        CommitInfo(
            hash=commit.hexsha[:8],
            message=commit.message.strip(),
            author=commit.author.name,
            date=datetime.fromtimestamp(commit.committed_date)
        )
        for commit in commits
    ]


def should_trigger_update(commit: CommitInfo) -> bool:
    """
    Check if commit should trigger project update.
    
    Args:
        commit: CommitInfo object
        
    Returns:
        True if update should be triggered
    """
    message_lower = commit.message.lower()
    
    for pattern in COMPLETION_PATTERNS:
        if re.search(pattern, message_lower):
            return True
    
    return False


def extract_task_references(commit: CommitInfo) -> List[str]:
    """
    Extract task IDs from commit message.
    
    Args:
        commit: CommitInfo object
        
    Returns:
        List of task IDs (e.g., ['001', '002'])
    """
    task_ids = []
    
    for pattern in TASK_REFERENCE_PATTERNS:
        matches = re.findall(pattern, commit.message, re.IGNORECASE)
        task_ids.extend(matches)
    
    return list(set(task_ids))  # Unique IDs


def find_task_file(task_id: str, project_dir: str = '.opencode/project') -> Optional[Path]:
    """
    Find task file by ID.
    
    Args:
        task_id: Task number (e.g., '001')
        project_dir: Path to project directory
        
    Returns:
        Path to task file or None
    """
    planning_dir = Path(project_dir) / 'planning' / 'epics'
    
    # Search for task-{task_id}-*.md
    pattern = f'task-{task_id.zfill(3)}-*.md'
    
    for task_file in planning_dir.rglob(pattern):
        return task_file
    
    return None


def update_task_status(task_file: Path, commit: CommitInfo) -> bool:
    """
    Update task file with completion status.
    
    Args:
        task_file: Path to task file
        commit: CommitInfo that triggered update
        
    Returns:
        True if updated successfully
    """
    if not task_file.exists():
        return False
    
    content = task_file.read_text()
    
    # Update status field
    content = re.sub(
        r'(\*\*Status\*\*:\s*)(pending|in_progress)',
        r'\1completed',
        content
    )
    
    # Add RPI session entry
    session_entry = f"""
### Session: {commit.date.strftime('%Y-%m-%d')}

**Status**: completed
**Commit**: `{commit.hash}`
**Notes**: {commit.message.split('\n')[0]}
**Outcome**: Task completed successfully

---
"""
    
    # Find RPI Sessions section and append
    if '## RPI Sessions' in content:
        content = content.replace(
            '## RPI Sessions',
            f'## RPI Sessions{session_entry}'
        )
    else:
        content += f'\n## RPI Sessions{session_entry}'
    
    # Update last updated date
    content = re.sub(
        r'(\*\*Last Updated\*\*:\s*)\[.*?\]',
        f'\\1[{datetime.now().strftime("%Y-%m-%d")}]',
        content
    )
    
    task_file.write_text(content)
    return True


def calculate_epic_progress(epic_dir: Path) -> Tuple[int, int]:
    """
    Calculate epic completion progress.
    
    Args:
        epic_dir: Path to epic directory
        
    Returns:
        Tuple of (completed_tasks, total_tasks)
    """
    completed = 0
    total = 0
    
    for task_file in epic_dir.rglob('task-*.md'):
        total += 1
        content = task_file.read_text()
        
        if re.search(r'\*\*Status\*\*:\s*completed', content):
            completed += 1
    
    return completed, total


def update_epic_status(epic_dir: Path):
    """
    Update epic STATUS.md file with current progress.
    
    Args:
        epic_dir: Path to epic directory
    """
    status_file = epic_dir / 'STATUS.md'
    
    if not status_file.exists():
        return
    
    completed, total = calculate_epic_progress(epic_dir)
    completion_percent = int((completed / total * 100)) if total > 0 else 0
    
    content = status_file.read_text()
    
    # Update completion percentage
    content = re.sub(
        r'(\*\*Overall Completion\*\*:\s*)\d+%',
        f'\\1{completion_percent}%',
        content
    )
    
    # Update counts
    content = re.sub(
        r'(\*\*Completed\*\*:\s*)\d+\s*/\s*\d+',
        f'\\1{completed} / {total}',
        content
    )
    
    # Update timestamp
    content = re.sub(
        r'(\*\*Last Updated\*\*:\s*)\[.*?\]',
        f'\\1[{datetime.now().strftime("%Y-%m-%d")}]',
        content
    )
    
    status_file.write_text(content)


def create_history_snapshot(project_dir: str = '.opencode/project'):
    """
    Create timestamped snapshot of roadmap and epic overviews.
    
    Args:
        project_dir: Path to project directory
    """
    history_dir = Path(project_dir) / 'planning' / '.history'
    history_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    
    # Snapshot roadmap
    roadmap_file = Path(project_dir) / 'planning' / 'roadmap.md'
    if roadmap_file.exists():
        snapshot_file = history_dir / f'{timestamp}-roadmap.md'
        snapshot_file.write_text(roadmap_file.read_text())
    
    # Snapshot epic overviews
    epics_dir = Path(project_dir) / 'planning' / 'epics'
    for epic_dir in epics_dir.iterdir():
        if epic_dir.is_dir():
            overview_file = epic_dir / 'overview.md'
            if overview_file.exists():
                epic_name = epic_dir.name
                snapshot_file = history_dir / f'{timestamp}-{epic_name}-overview.md'
                snapshot_file.write_text(overview_file.read_text())


def main():
    """Main entry point."""
    import sys
    
    repo_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    project_dir = '.opencode/project'
    
    if not Path(project_dir).exists():
        print(f"ERROR: Project directory not found: {project_dir}")
        print("Run /project-init first to initialize project structure")
        return 1
    
    print("Analyzing commits for project updates...")
    
    # Get last update time
    last_update = get_last_update_time(project_dir)
    
    if last_update:
        print(f"Last update: {last_update}")
    else:
        print("No previous update found, analyzing recent commits")
    
    # Get commits
    commits = get_commits_since(repo_path, last_update)
    
    if not commits:
        print("No new commits found")
        return 0
    
    print(f"Found {len(commits)} commit(s) since last update")
    
    # Analyze commits
    updates_made = False
    
    for commit in commits:
        if should_trigger_update(commit):
            print(f"\n✓ Trigger found: {commit.hash} - {commit.message[:60]}")
            
            # Extract task references
            task_ids = extract_task_references(commit)
            
            for task_id in task_ids:
                task_file = find_task_file(task_id, project_dir)
                
                if task_file:
                    print(f"  Updating task-{task_id}: {task_file.name}")
                    update_task_status(task_file, commit)
                    
                    # Update parent epic
                    epic_dir = task_file.parent.parent
                    update_epic_status(epic_dir)
                    
                    updates_made = True
                else:
                    print(f"  WARNING: Task file not found for task-{task_id}")
    
    if updates_made:
        # Create history snapshot
        print("\nCreating history snapshot...")
        create_history_snapshot(project_dir)
        
        # Update timestamp
        save_last_update_time(project_dir)
        
        print(f"\n✓ Project status updated successfully")
    else:
        print("\nNo updates needed")
    
    return 0


if __name__ == '__main__':
    exit(main())
