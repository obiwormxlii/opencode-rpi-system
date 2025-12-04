#!/usr/bin/env python3
"""
Git History Analysis Script

Analyzes git repository history to extract:
- Project age (first and last commit dates)
- Commit frequency and patterns
- Top contributors
- Branching strategy (feature branches, trunk-based, git-flow)
- Commit message patterns
- Recent activity

Requires: GitPython
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from collections import Counter, defaultdict

try:
    from git import Repo, GitCommandError
except ImportError:
    print("ERROR: GitPython not installed. Install with: pip install GitPython")
    exit(1)


@dataclass
class ContributorStats:
    """Statistics for a single contributor."""
    name: str
    email: str
    commits: int
    first_commit: str
    last_commit: str


@dataclass
class GitAnalysisReport:
    """Complete git history analysis report."""
    project_age_days: int
    first_commit_date: str
    last_commit_date: str
    total_commits: int
    total_contributors: int
    top_contributors: List[ContributorStats]
    branching_strategy: str
    commit_frequency: Dict[str, int]
    commit_message_patterns: Dict[str, int]
    recent_activity: List[Dict]
    active_branches: int
    default_branch: str


def analyze_git_repo(repo_path: str = '.') -> GitAnalysisReport:
    """
    Analyze git repository history.
    
    Args:
        repo_path: Path to git repository
        
    Returns:
        GitAnalysisReport with analysis results
        
    Raises:
        ValueError: If path is not a git repository
    """
    try:
        repo = Repo(repo_path)
    except Exception as e:
        raise ValueError(f"Not a git repository: {repo_path}") from e
    
    if repo.bare:
        raise ValueError("Cannot analyze bare repository")
    
    # Get all commits
    commits = list(repo.iter_commits('HEAD'))
    
    if not commits:
        raise ValueError("No commits found in repository")
    
    # Basic stats
    total_commits = len(commits)
    first_commit = commits[-1]
    last_commit = commits[0]
    
    first_date = datetime.fromtimestamp(first_commit.committed_date)
    last_date = datetime.fromtimestamp(last_commit.committed_date)
    project_age = (last_date - first_date).days
    
    # Contributor analysis
    contributor_stats = defaultdict(lambda: {
        'commits': 0,
        'first': None,
        'last': None,
        'email': None
    })
    
    for commit in commits:
        author = commit.author.name
        email = commit.author.email
        commit_date = datetime.fromtimestamp(commit.committed_date)
        
        contributor_stats[author]['commits'] += 1
        contributor_stats[author]['email'] = email
        
        if contributor_stats[author]['first'] is None or commit_date < contributor_stats[author]['first']:
            contributor_stats[author]['first'] = commit_date
        
        if contributor_stats[author]['last'] is None or commit_date > contributor_stats[author]['last']:
            contributor_stats[author]['last'] = commit_date
    
    # Top contributors
    top_contributors = sorted(
        [
            ContributorStats(
                name=name,
                email=stats['email'],
                commits=stats['commits'],
                first_commit=stats['first'].isoformat(),
                last_commit=stats['last'].isoformat()
            )
            for name, stats in contributor_stats.items()
        ],
        key=lambda x: x.commits,
        reverse=True
    )[:10]  # Top 10
    
    # Commit frequency (by month for last year)
    commit_frequency = defaultdict(int)
    one_year_ago = last_date - timedelta(days=365)
    
    for commit in commits:
        commit_date = datetime.fromtimestamp(commit.committed_date)
        if commit_date > one_year_ago:
            month_key = commit_date.strftime('%Y-%m')
            commit_frequency[month_key] += 1
    
    # Commit message patterns
    message_patterns = Counter()
    for commit in commits[:100]:  # Analyze last 100 commits
        message = commit.message.lower().strip()
        
        # Extract conventional commit types
        if message.startswith('feat:') or message.startswith('feature:'):
            message_patterns['feat'] += 1
        elif message.startswith('fix:'):
            message_patterns['fix'] += 1
        elif message.startswith('docs:'):
            message_patterns['docs'] += 1
        elif message.startswith('refactor:'):
            message_patterns['refactor'] += 1
        elif message.startswith('test:'):
            message_patterns['test'] += 1
        elif message.startswith('chore:'):
            message_patterns['chore'] += 1
        elif message.startswith('style:'):
            message_patterns['style'] += 1
        else:
            message_patterns['other'] += 1
    
    # Branching strategy detection
    branches = list(repo.branches)
    active_branches = len(branches)
    
    branch_names = [b.name for b in branches]
    branching_strategy = detect_branching_strategy(branch_names)
    
    # Recent activity (last 10 commits)
    recent_activity = []
    for commit in commits[:10]:
        recent_activity.append({
            'hash': commit.hexsha[:8],
            'author': commit.author.name,
            'date': datetime.fromtimestamp(commit.committed_date).isoformat(),
            'message': commit.message.strip().split('\n')[0][:80]
        })
    
    # Default branch
    try:
        default_branch = repo.active_branch.name
    except:
        default_branch = 'main' if 'main' in branch_names else 'master'
    
    return GitAnalysisReport(
        project_age_days=project_age,
        first_commit_date=first_date.isoformat(),
        last_commit_date=last_date.isoformat(),
        total_commits=total_commits,
        total_contributors=len(contributor_stats),
        top_contributors=top_contributors,
        branching_strategy=branching_strategy,
        commit_frequency=dict(commit_frequency),
        commit_message_patterns=dict(message_patterns),
        recent_activity=recent_activity,
        active_branches=active_branches,
        default_branch=default_branch
    )


def detect_branching_strategy(branch_names: List[str]) -> str:
    """
    Detect branching strategy from branch names.
    
    Args:
        branch_names: List of branch names
        
    Returns:
        Strategy name (git-flow, feature-branch, trunk-based, other)
    """
    branch_names_lower = [b.lower() for b in branch_names]
    
    # Git-flow: develop + master/main + feature/hotfix/release branches
    has_develop = 'develop' in branch_names_lower or 'dev' in branch_names_lower
    has_main = 'main' in branch_names_lower or 'master' in branch_names_lower
    has_feature_branches = any(b.startswith('feature/') for b in branch_names_lower)
    has_hotfix = any(b.startswith('hotfix/') for b in branch_names_lower)
    has_release = any(b.startswith('release/') for b in branch_names_lower)
    
    if has_develop and has_main and (has_feature_branches or has_hotfix or has_release):
        return 'git-flow'
    
    # Feature branch workflow: main/master + feature branches
    if has_main and has_feature_branches:
        return 'feature-branch'
    
    # Trunk-based: mainly main/master, few short-lived branches
    if has_main and len(branch_names) <= 3:
        return 'trunk-based'
    
    return 'other'


def generate_markdown_report(report: GitAnalysisReport, output_file: str = '.tmp/project-init/git-analysis.md'):
    """
    Generate markdown report from git analysis.
    
    Args:
        report: GitAnalysisReport object
        output_file: Output file path
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write("# Git History Analysis\n\n")
        
        f.write("## Project Age\n\n")
        f.write(f"- **First Commit**: {report.first_commit_date}\n")
        f.write(f"- **Last Commit**: {report.last_commit_date}\n")
        f.write(f"- **Age**: {report.project_age_days} days (~{report.project_age_days // 365} years)\n")
        f.write(f"- **Total Commits**: {report.total_commits}\n")
        f.write(f"- **Default Branch**: `{report.default_branch}`\n\n")
        
        f.write("## Branching Strategy\n\n")
        f.write(f"**Detected Strategy**: {report.branching_strategy}\n\n")
        f.write(f"- **Active Branches**: {report.active_branches}\n\n")
        
        f.write("## Contributors\n\n")
        f.write(f"**Total Contributors**: {report.total_contributors}\n\n")
        f.write("### Top Contributors\n\n")
        f.write("| Name | Commits | First Commit | Last Commit |\n")
        f.write("|------|---------|--------------|-------------|\n")
        for contrib in report.top_contributors[:5]:
            f.write(f"| {contrib.name} | {contrib.commits} | {contrib.first_commit[:10]} | {contrib.last_commit[:10]} |\n")
        f.write("\n")
        
        f.write("## Commit Message Patterns\n\n")
        f.write("Analysis of last 100 commits:\n\n")
        for pattern, count in sorted(report.commit_message_patterns.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{pattern}**: {count} commits\n")
        f.write("\n")
        
        f.write("## Recent Activity\n\n")
        f.write("Last 10 commits:\n\n")
        for commit in report.recent_activity:
            f.write(f"- `{commit['hash']}` - {commit['author']} ({commit['date'][:10]}): {commit['message']}\n")
        f.write("\n")
        
        f.write("## Commit Frequency (Last Year)\n\n")
        if report.commit_frequency:
            f.write("| Month | Commits |\n")
            f.write("|-------|----------|\n")
            for month in sorted(report.commit_frequency.keys(), reverse=True)[:12]:
                f.write(f"| {month} | {report.commit_frequency[month]} |\n")
        else:
            f.write("No recent commits in last year.\n")
        f.write("\n")
    
    print(f"✓ Git analysis saved to {output_file}")


def main():
    """Main entry point."""
    import sys
    repo_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"Analyzing git repository: {repo_path}")
    
    try:
        report = analyze_git_repo(repo_path)
    except ValueError as e:
        print(f"ERROR: {e}")
        return 1
    
    # Generate markdown report
    generate_markdown_report(report)
    
    # Save JSON
    json_output = '.tmp/project-init/git-analysis.json'
    os.makedirs(os.path.dirname(json_output), exist_ok=True)
    with open(json_output, 'w') as f:
        json.dump(asdict(report), f, indent=2, default=str)
    
    print(f"✓ JSON analysis saved to {json_output}")
    print(f"\nSummary:")
    print(f"  Project age: {report.project_age_days} days")
    print(f"  Total commits: {report.total_commits}")
    print(f"  Contributors: {report.total_contributors}")
    print(f"  Branching strategy: {report.branching_strategy}")
    
    return 0


if __name__ == '__main__':
    exit(main())
