#!/usr/bin/env python3
"""
Create History Snapshot Script

Archives completed epics or phases to .opencode/project/planning/history/
Creates timestamped snapshots with summary and task file copies.

Usage:
    python create_history_snapshot.py --epic epic-003
    python create_history_snapshot.py --epic epic-003 --phase phase-2
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import argparse

try:
    from git import Repo
except ImportError:
    print("ERROR: GitPython not installed. Install with: pip install GitPython")
    exit(1)


@dataclass
class TaskInfo:
    """Represents a task for snapshot."""
    task_id: str
    task_name: str
    file_path: Path
    status: str
    completion_date: Optional[str]
    

def parse_task_file(task_file: Path) -> TaskInfo:
    """
    Parse task file and extract metadata.
    
    Args:
        task_file: Path to task markdown file
        
    Returns:
        TaskInfo object
    """
    content = task_file.read_text()
    
    # Extract task ID from filename (task-001-name.md)
    task_id = task_file.stem.split('-')[1]
    task_name = '-'.join(task_file.stem.split('-')[2:])
    
    # Extract status
    status_match = content.find('**Status**:')
    status = 'unknown'
    if status_match >= 0:
        status_line = content[status_match:content.find('\n', status_match)]
        if 'completed' in status_line.lower():
            status = 'completed'
        elif 'in_progress' in status_line.lower():
            status = 'in_progress'
        else:
            status = 'pending'
    
    # Try to find completion date from RPI Sessions
    completion_date = None
    if '## RPI Sessions' in content:
        sessions_start = content.find('## RPI Sessions')
        sessions_section = content[sessions_start:sessions_start+1000]
        
        # Look for completed status
        if 'Status**: completed' in sessions_section:
            # Find the date for this session
            date_start = sessions_section.find('### Session:')
            if date_start >= 0:
                date_line = sessions_section[date_start:sessions_section.find('\n', date_start)]
                # Extract YYYY-MM-DD
                import re
                date_match = re.search(r'\d{4}-\d{2}-\d{2}', date_line)
                if date_match:
                    completion_date = date_match.group(0)
    
    return TaskInfo(
        task_id=task_id,
        task_name=task_name,
        file_path=task_file,
        status=status,
        completion_date=completion_date
    )


def get_git_metrics(repo_path: str, task_files: List[Path]) -> Dict:
    """
    Get git metrics for snapshot period.
    
    Args:
        repo_path: Path to git repository
        task_files: List of task files to analyze
        
    Returns:
        Dictionary with git metrics
    """
    repo = Repo(repo_path)
    
    # Get all commits that modified task-related files
    commits = set()
    files_changed = set()
    
    for task_file in task_files:
        try:
            # Get commits that touched this task file
            task_commits = list(repo.iter_commits(paths=str(task_file), max_count=50))
            for commit in task_commits:
                commits.add(commit.hexsha)
                files_changed.update([item.a_path for item in commit.diff(commit.parents[0] if commit.parents else None)])
        except:
            pass  # Task file might not be committed yet
    
    return {
        'total_commits': len(commits),
        'files_modified': len(files_changed),
        'commit_hashes': list(commits)[:10]  # First 10
    }


def calculate_duration(tasks: List[TaskInfo]) -> Optional[Dict]:
    """
    Calculate duration from first task start to last task completion.
    
    Args:
        tasks: List of TaskInfo objects
        
    Returns:
        Dictionary with start_date, end_date, duration_days
    """
    dates = [t.completion_date for t in tasks if t.completion_date]
    
    if not dates:
        return None
    
    dates.sort()
    start_date = dates[0]
    end_date = dates[-1]
    
    # Calculate duration
    from datetime import datetime
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    duration = (end - start).days + 1
    
    return {
        'start_date': start_date,
        'end_date': end_date,
        'duration_days': duration
    }


def create_summary(epic_id: str, phase_id: Optional[str], tasks: List[TaskInfo], git_metrics: Dict, duration: Optional[Dict]) -> str:
    """
    Create summary markdown for snapshot.
    
    Args:
        epic_id: Epic identifier (e.g., 'epic-003')
        phase_id: Optional phase identifier
        tasks: List of TaskInfo objects
        git_metrics: Git metrics dictionary
        duration: Duration dictionary
        
    Returns:
        Markdown summary content
    """
    completed_tasks = [t for t in tasks if t.status == 'completed']
    
    summary = f"""# History Snapshot: {epic_id}"""
    
    if phase_id:
        summary += f" - {phase_id}\n"
    else:
        summary += "\n"
    
    summary += f"""
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This snapshot captures the completion of {epic_id}"""
    
    if phase_id:
        summary += f" {phase_id}"
    
    summary += f""".

## Metrics

- **Total Tasks**: {len(tasks)}
- **Completed Tasks**: {len(completed_tasks)} ({int(len(completed_tasks)/len(tasks)*100)}%)
- **Pending/In Progress**: {len(tasks) - len(completed_tasks)}
"""
    
    if duration:
        summary += f"""
## Timeline

- **Start Date**: {duration['start_date']}
- **End Date**: {duration['end_date']}
- **Duration**: {duration['duration_days']} days
"""
    
    summary += f"""
## Git Activity

- **Commits**: {git_metrics['total_commits']}
- **Files Modified**: {git_metrics['files_modified']}

### Recent Commits
"""
    
    for commit_hash in git_metrics['commit_hashes'][:5]:
        summary += f"- `{commit_hash[:8]}`\n"
    
    summary += f"""
## Tasks Completed

"""
    
    for task in completed_tasks:
        completion = f" ({task.completion_date})" if task.completion_date else ""
        summary += f"- ✅ task-{task.task_id} - {task.task_name}{completion}\n"
    
    if len(tasks) > len(completed_tasks):
        summary += f"\n## Tasks Not Completed\n\n"
        for task in tasks:
            if task.status != 'completed':
                status_emoji = '🔄' if task.status == 'in_progress' else '⏳'
                summary += f"- {status_emoji} task-{task.task_id} - {task.task_name}\n"
    
    summary += f"""
## Files Archived

This snapshot includes copies of all task files at the time of completion:
"""
    
    for task in tasks:
        summary += f"- {task.file_path.name}\n"
    
    summary += f"""
## Notes

Add any lessons learned, blockers encountered, or important decisions made during this epic/phase.

---

*This snapshot was automatically generated by the project-manager agent.*
"""
    
    return summary


def create_snapshot(project_dir: str, epic_id: str, phase_id: Optional[str] = None, repo_path: str = '.'):
    """
    Create history snapshot for epic or phase.
    
    Args:
        project_dir: Path to .opencode/project directory
        epic_id: Epic identifier (e.g., 'epic-003')
        phase_id: Optional phase identifier (e.g., 'phase-2')
        repo_path: Path to git repository
    """
    project_path = Path(project_dir)
    epics_dir = project_path / 'planning' / 'epics'
    
    # Find epic directory
    epic_dir = None
    for d in epics_dir.iterdir():
        if d.is_dir() and d.name.startswith(epic_id):
            epic_dir = d
            break
    
    if not epic_dir:
        print(f"ERROR: Epic directory not found for {epic_id}")
        return False
    
    # Find tasks
    task_files = []
    
    if phase_id:
        # Find phase directory
        phase_dir = None
        for d in epic_dir.iterdir():
            if d.is_dir() and d.name.startswith(phase_id):
                phase_dir = d
                break
        
        if not phase_dir:
            print(f"ERROR: Phase directory not found for {phase_id}")
            return False
        
        task_files = list(phase_dir.glob('task-*.md'))
    else:
        # All tasks in epic
        task_files = list(epic_dir.rglob('task-*.md'))
    
    if not task_files:
        print(f"ERROR: No task files found")
        return False
    
    print(f"Found {len(task_files)} task files")
    
    # Parse task files
    tasks = [parse_task_file(f) for f in task_files]
    
    # Get git metrics
    print("Analyzing git history...")
    git_metrics = get_git_metrics(repo_path, task_files)
    
    # Calculate duration
    duration = calculate_duration(tasks)
    
    # Create snapshot directory
    timestamp = datetime.now().strftime('%Y-%m-%d')
    snapshot_name = f"{timestamp}-{epic_id}"
    if phase_id:
        snapshot_name += f"-{phase_id}"
    
    snapshot_dir = project_path / 'planning' / 'history' / snapshot_name
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating snapshot: {snapshot_dir}")
    
    # Copy task files
    for task_file in task_files:
        dest_file = snapshot_dir / task_file.name
        shutil.copy2(task_file, dest_file)
        print(f"  Copied: {task_file.name}")
    
    # Create summary
    summary = create_summary(epic_id, phase_id, tasks, git_metrics, duration)
    summary_file = snapshot_dir / 'SUMMARY.md'
    summary_file.write_text(summary)
    print(f"  Created: SUMMARY.md")
    
    # Create metadata JSON
    metadata = {
        'created': datetime.now().isoformat(),
        'epic_id': epic_id,
        'phase_id': phase_id,
        'total_tasks': len(tasks),
        'completed_tasks': len([t for t in tasks if t.status == 'completed']),
        'duration': duration,
        'git_metrics': git_metrics
    }
    metadata_file = snapshot_dir / 'metadata.json'
    metadata_file.write_text(json.dumps(metadata, indent=2))
    print(f"  Created: metadata.json")
    
    print(f"\n✓ Snapshot created successfully: {snapshot_dir}")
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Create history snapshot for completed epic/phase')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--epic-id', required=True, help='Epic ID (e.g., epic-003)')
    parser.add_argument('--phase-id', help='Phase ID (e.g., phase-2)')
    
    args = parser.parse_args()
    
    project_dir = Path(args.project_root) / '.opencode' / 'project'
    
    if not project_dir.exists():
        print(f"ERROR: Project directory not found: {project_dir}")
        print("Run /project-init first to initialize project structure")
        return 1
    
    success = create_snapshot(
        project_dir=str(project_dir),
        epic_id=args.epic_id,
        phase_id=args.phase_id,
        repo_path=args.project_root
    )
    
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
