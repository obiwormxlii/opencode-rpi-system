#!/usr/bin/env python3
"""
Dependency Analysis Script

Analyzes project dependencies from various package manager files and extracts:
- Frameworks and their versions
- Database drivers
- Key libraries (authentication, payments, email, etc.)
- Categorized dependencies
- Optional: Security vulnerability detection

Supported formats:
- package.json (Node.js/npm/yarn/pnpm)
- requirements.txt, Pipfile, pyproject.toml (Python)
- Gemfile, Gemfile.lock (Ruby)
- go.mod (Go)
- Cargo.toml (Rust)
- composer.json (PHP)
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict


@dataclass
class Dependency:
    """Represents a single dependency."""
    name: str
    version: str
    category: str
    description: Optional[str] = None


@dataclass
class DependencyReport:
    """Complete dependency analysis report."""
    frameworks: List[Dependency]
    databases: List[Dependency]
    authentication: List[Dependency]
    testing: List[Dependency]
    utilities: List[Dependency]
    other: List[Dependency]
    language_breakdown: Dict[str, int]
    total_dependencies: int
    package_managers: List[str]


# Category mapping - maps package names to categories
FRAMEWORK_PATTERNS = {
    'react', 'vue', 'angular', 'svelte', 'next', 'nuxt', 'remix',
    'django', 'flask', 'fastapi', 'express', 'nestjs', 'koa',
    'rails', 'sinatra', 'gin', 'echo', 'axum', 'actix',
    'laravel', 'symfony', 'spring', 'quarkus'
}

DATABASE_PATTERNS = {
    'pg', 'postgres', 'postgresql', 'mysql', 'mysql2', 'mongodb', 'mongoose',
    'redis', 'sqlite', 'sqlalchemy', 'sequelize', 'typeorm', 'prisma',
    'knex', 'kysely', 'drizzle'
}

AUTH_PATTERNS = {
    'auth', 'passport', 'jwt', 'oauth', 'auth0', 'firebase-admin',
    'bcrypt', 'argon2', 'session', 'cookie'
}

TEST_PATTERNS = {
    'jest', 'mocha', 'chai', 'pytest', 'unittest', 'vitest', 'cypress',
    'playwright', 'selenium', 'testing-library', 'rspec', 'minitest'
}


def find_package_files(root_dir: str = '.') -> Dict[str, Path]:
    """
    Find all package manager files in the project.
    
    Args:
        root_dir: Root directory to search from
        
    Returns:
        Dictionary mapping file type to Path object
    """
    root = Path(root_dir).resolve()
    package_files = {}
    
    search_patterns = {
        'package.json': 'npm',
        'requirements.txt': 'pip',
        'Pipfile': 'pipenv',
        'pyproject.toml': 'poetry/pip',
        'Gemfile': 'bundler',
        'go.mod': 'go',
        'Cargo.toml': 'cargo',
        'composer.json': 'composer'
    }
    
    for pattern, manager in search_patterns.items():
        matches = list(root.rglob(pattern))
        # Exclude node_modules, vendor, etc.
        matches = [m for m in matches if not any(
            excluded in m.parts for excluded in ['node_modules', 'vendor', '.venv', 'venv', '__pycache__']
        )]
        if matches:
            package_files[manager] = matches[0]  # Use first found
    
    return package_files


def parse_package_json(file_path: Path) -> List[Dependency]:
    """Parse Node.js package.json file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    dependencies = []
    for dep_type in ['dependencies', 'devDependencies']:
        if dep_type in data:
            for name, version in data[dep_type].items():
                category = categorize_dependency(name)
                dependencies.append(Dependency(
                    name=name,
                    version=version.lstrip('^~>=<'),
                    category=category
                ))
    
    return dependencies


def parse_requirements_txt(file_path: Path) -> List[Dependency]:
    """Parse Python requirements.txt file."""
    dependencies = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse: package==1.0.0 or package>=1.0.0
            match = re.match(r'^([a-zA-Z0-9_-]+)([><=!]+)?(.+)?', line)
            if match:
                name = match.group(1)
                version = match.group(3) if match.group(3) else 'latest'
                category = categorize_dependency(name)
                dependencies.append(Dependency(
                    name=name,
                    version=version,
                    category=category
                ))
    
    return dependencies


def parse_pyproject_toml(file_path: Path) -> List[Dependency]:
    """Parse Python pyproject.toml (Poetry/PEP 621)."""
    try:
        import tomli
    except ImportError:
        # Python 3.11+ has tomllib built-in
        import tomllib as tomli
    
    with open(file_path, 'rb') as f:
        data = tomli.load(f)
    
    dependencies = []
    
    # Poetry format
    if 'tool' in data and 'poetry' in data['tool']:
        deps = data['tool']['poetry'].get('dependencies', {})
        for name, version_spec in deps.items():
            if name == 'python':
                continue
            version = version_spec if isinstance(version_spec, str) else 'latest'
            category = categorize_dependency(name)
            dependencies.append(Dependency(name=name, version=version, category=category))
    
    # PEP 621 format
    if 'project' in data:
        deps_list = data['project'].get('dependencies', [])
        for dep_str in deps_list:
            match = re.match(r'^([a-zA-Z0-9_-]+)([><=!]+)?(.+)?', dep_str)
            if match:
                name = match.group(1)
                version = match.group(3) if match.group(3) else 'latest'
                category = categorize_dependency(name)
                dependencies.append(Dependency(name=name, version=version, category=category))
    
    return dependencies


def categorize_dependency(name: str) -> str:
    """
    Categorize a dependency based on its name.
    
    Args:
        name: Dependency name
        
    Returns:
        Category string
    """
    name_lower = name.lower()
    
    if any(pattern in name_lower for pattern in FRAMEWORK_PATTERNS):
        return 'framework'
    elif any(pattern in name_lower for pattern in DATABASE_PATTERNS):
        return 'database'
    elif any(pattern in name_lower for pattern in AUTH_PATTERNS):
        return 'authentication'
    elif any(pattern in name_lower for pattern in TEST_PATTERNS):
        return 'testing'
    elif any(keyword in name_lower for keyword in ['util', 'helper', 'lodash', 'underscore']):
        return 'utilities'
    else:
        return 'other'


def analyze_dependencies(root_dir: str = '.') -> DependencyReport:
    """
    Main analysis function.
    
    Args:
        root_dir: Root directory of project
        
    Returns:
        DependencyReport with full analysis
    """
    package_files = find_package_files(root_dir)
    
    all_dependencies = []
    
    for manager, file_path in package_files.items():
        if manager == 'npm':
            all_dependencies.extend(parse_package_json(file_path))
        elif manager in ['pip', 'pipenv']:
            all_dependencies.extend(parse_requirements_txt(file_path))
        elif manager in ['poetry/pip']:
            all_dependencies.extend(parse_pyproject_toml(file_path))
        # TODO: Add parsers for Gemfile, go.mod, Cargo.toml, composer.json
    
    # Categorize dependencies
    frameworks = [d for d in all_dependencies if d.category == 'framework']
    databases = [d for d in all_dependencies if d.category == 'database']
    authentication = [d for d in all_dependencies if d.category == 'authentication']
    testing = [d for d in all_dependencies if d.category == 'testing']
    utilities = [d for d in all_dependencies if d.category == 'utilities']
    other = [d for d in all_dependencies if d.category == 'other']
    
    # Language breakdown (based on package managers found)
    language_breakdown = {}
    if 'npm' in package_files:
        language_breakdown['JavaScript/TypeScript'] = len([d for d in all_dependencies if d in parse_package_json(package_files['npm'])])
    if any(pm in package_files for pm in ['pip', 'pipenv', 'poetry/pip']):
        language_breakdown['Python'] = len([d for d in all_dependencies if d.category in ['framework', 'database', 'authentication', 'testing', 'utilities', 'other']])
    
    return DependencyReport(
        frameworks=frameworks,
        databases=databases,
        authentication=authentication,
        testing=testing,
        utilities=utilities,
        other=other,
        language_breakdown=language_breakdown,
        total_dependencies=len(all_dependencies),
        package_managers=list(package_files.keys())
    )


def generate_markdown_report(report: DependencyReport, output_file: str = '.tmp/project-init/dependency-analysis.md'):
    """
    Generate markdown report from analysis.
    
    Args:
        report: DependencyReport object
        output_file: Output file path
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write("# Dependency Analysis Report\n\n")
        f.write(f"**Total Dependencies**: {report.total_dependencies}\n")
        f.write(f"**Package Managers**: {', '.join(report.package_managers)}\n\n")
        
        f.write("## Language Breakdown\n\n")
        for lang, count in report.language_breakdown.items():
            f.write(f"- **{lang}**: {count} packages\n")
        f.write("\n")
        
        sections = [
            ("Frameworks", report.frameworks),
            ("Databases", report.databases),
            ("Authentication", report.authentication),
            ("Testing", report.testing),
            ("Utilities", report.utilities),
            ("Other", report.other)
        ]
        
        for section_name, deps in sections:
            if deps:
                f.write(f"## {section_name}\n\n")
                f.write("| Package | Version |\n")
                f.write("|---------|----------|\n")
                for dep in deps:
                    f.write(f"| {dep.name} | {dep.version} |\n")
                f.write("\n")
    
    print(f"✓ Dependency analysis saved to {output_file}")


def main():
    """Main entry point."""
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"Analyzing dependencies in: {root_dir}")
    report = analyze_dependencies(root_dir)
    
    # Generate markdown report
    generate_markdown_report(report)
    
    # Also save JSON for programmatic access
    json_output = '.tmp/project-init/dependency-analysis.json'
    os.makedirs(os.path.dirname(json_output), exist_ok=True)
    with open(json_output, 'w') as f:
        json.dump(asdict(report), f, indent=2, default=str)
    
    print(f"✓ JSON analysis saved to {json_output}")
    print(f"\nSummary:")
    print(f"  Total dependencies: {report.total_dependencies}")
    print(f"  Frameworks: {len(report.frameworks)}")
    print(f"  Databases: {len(report.databases)}")
    print(f"  Package managers: {', '.join(report.package_managers)}")


if __name__ == '__main__':
    main()
