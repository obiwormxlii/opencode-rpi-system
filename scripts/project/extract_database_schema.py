#!/usr/bin/env python3
"""
Database Schema Extraction Script

Extracts database schema from:
- Migration files (Alembic, Knex, Rails, Django, Prisma)
- ORM models (SQLAlchemy, Sequelize, Django, ActiveRecord)
- Schema files (schema.sql, schema.prisma)

Generates:
- Entity list with fields and types
- Relationship mapping
- Mermaid ERD diagram (calls generate_erd.py)
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict, field


@dataclass
class Field:
    """Represents a database field/column."""
    name: str
    type: str
    nullable: bool = True
    primary_key: bool = False
    foreign_key: Optional[str] = None
    unique: bool = False
    default: Optional[str] = None


@dataclass
class Entity:
    """Represents a database table/entity."""
    name: str
    table_name: str
    fields: List[Field] = field(default_factory=list)
    indexes: List[str] = field(default_factory=list)
    relationships: List[Dict] = field(default_factory=list)


@dataclass
class SchemaReport:
    """Complete database schema report."""
    entities: List[Entity]
    relationships: List[Dict]
    database_type: Optional[str] = None
    orm_framework: Optional[str] = None


def find_schema_files(root_dir: str = '.') -> Dict[str, List[Path]]:
    """
    Find schema-related files in project.
    
    Args:
        root_dir: Root directory to search
        
    Returns:
        Dictionary mapping file type to list of Paths
    """
    root = Path(root_dir).resolve()
    schema_files = {
        'django_models': [],
        'sqlalchemy_models': [],
        'prisma_schema': [],
        'rails_migrations': [],
        'knex_migrations': [],
        'sql_schema': []
    }
    
    # Django models (models.py)
    for models_file in root.rglob('models.py'):
        if 'migrations' not in models_file.parts and 'venv' not in models_file.parts:
            schema_files['django_models'].append(models_file)
    
    # SQLAlchemy models (often models.py or database.py)
    # TODO: Better detection
    
    # Prisma schema
    for prisma_file in root.rglob('schema.prisma'):
        schema_files['prisma_schema'].append(prisma_file)
    
    # Rails migrations
    rails_migrations_dir = root / 'db' / 'migrate'
    if rails_migrations_dir.exists():
        schema_files['rails_migrations'] = list(rails_migrations_dir.glob('*.rb'))
    
    # Knex migrations
    for migrations_dir in root.rglob('migrations'):
        if migrations_dir.is_dir():
            schema_files['knex_migrations'].extend(migrations_dir.glob('*.js'))
            schema_files['knex_migrations'].extend(migrations_dir.glob('*.ts'))
    
    # SQL schema files
    for sql_file in root.rglob('schema.sql'):
        schema_files['sql_schema'].append(sql_file)
    
    return {k: v for k, v in schema_files.items() if v}


def parse_django_models(file_path: Path) -> List[Entity]:
    """
    Parse Django models.py file.
    
    Args:
        file_path: Path to models.py
        
    Returns:
        List of Entity objects
    """
    entities = []
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all class definitions that inherit from models.Model
    class_pattern = r'class\s+(\w+)\(.*models\.Model.*\):\s*\n((?:\s{4}.*\n)*)'
    
    for match in re.finditer(class_pattern, content):
        class_name = match.group(1)
        class_body = match.group(2)
        
        # Extract table name if specified
        meta_match = re.search(r'class\s+Meta:.*db_table\s*=\s*[\'"](\w+)[\'"]', class_body)
        table_name = meta_match.group(1) if meta_match else class_name.lower() + 's'
        
        entity = Entity(name=class_name, table_name=table_name)
        
        # Extract fields
        field_patterns = [
            (r'(\w+)\s*=\s*models\.CharField', 'string'),
            (r'(\w+)\s*=\s*models\.TextField', 'text'),
            (r'(\w+)\s*=\s*models\.IntegerField', 'integer'),
            (r'(\w+)\s*=\s*models\.BooleanField', 'boolean'),
            (r'(\w+)\s*=\s*models\.DateTimeField', 'datetime'),
            (r'(\w+)\s*=\s*models\.DateField', 'date'),
            (r'(\w+)\s*=\s*models\.ForeignKey', 'foreign_key'),
        ]
        
        for pattern, field_type in field_patterns:
            for field_match in re.finditer(pattern, class_body):
                field_name = field_match.group(1)
                field_obj = Field(name=field_name, type=field_type)
                
                # Check for primary key
                if 'primary_key=True' in field_match.group(0):
                    field_obj.primary_key = True
                
                # Check for nullable
                if 'null=False' in field_match.group(0):
                    field_obj.nullable = False
                
                entity.fields.append(field_obj)
        
        entities.append(entity)
    
    return entities


def parse_prisma_schema(file_path: Path) -> List[Entity]:
    """
    Parse Prisma schema.prisma file.
    
    Args:
        file_path: Path to schema.prisma
        
    Returns:
        List of Entity objects
    """
    entities = []
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all model definitions
    model_pattern = r'model\s+(\w+)\s*\{([^}]+)\}'
    
    for match in re.finditer(model_pattern, content):
        model_name = match.group(1)
        model_body = match.group(2)
        
        entity = Entity(name=model_name, table_name=model_name.lower())
        
        # Extract fields
        field_pattern = r'(\w+)\s+(\w+)(\??)\s*(.*)'
        
        for line in model_body.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('@@') or line.startswith('//'):
                continue
            
            field_match = re.match(field_pattern, line)
            if field_match:
                field_name = field_match.group(1)
                field_type = field_match.group(2)
                optional = field_match.group(3) == '?'
                attributes = field_match.group(4)
                
                field_obj = Field(
                    name=field_name,
                    type=field_type,
                    nullable=optional,
                    primary_key='@id' in attributes,
                    unique='@unique' in attributes
                )
                
                # Check for relations
                if '@relation' in attributes:
                    field_obj.foreign_key = field_type
                
                entity.fields.append(field_obj)
        
        entities.append(entity)
    
    return entities


def extract_schema(root_dir: str = '.') -> SchemaReport:
    """
    Main schema extraction function.
    
    Args:
        root_dir: Root directory of project
        
    Returns:
        SchemaReport with extracted schema
    """
    schema_files = find_schema_files(root_dir)
    entities = []
    orm_framework = None
    
    # Parse Django models
    if 'django_models' in schema_files:
        orm_framework = 'Django ORM'
        for models_file in schema_files['django_models']:
            entities.extend(parse_django_models(models_file))
    
    # Parse Prisma schema
    if 'prisma_schema' in schema_files:
        orm_framework = 'Prisma'
        for prisma_file in schema_files['prisma_schema']:
            entities.extend(parse_prisma_schema(prisma_file))
    
    # TODO: Add parsers for SQLAlchemy, Sequelize, Rails, etc.
    
    # Extract relationships
    relationships = []
    for entity in entities:
        for field in entity.fields:
            if field.foreign_key:
                relationships.append({
                    'from': entity.name,
                    'to': field.foreign_key,
                    'type': '1:N',
                    'field': field.name
                })
    
    return SchemaReport(
        entities=entities,
        relationships=relationships,
        orm_framework=orm_framework
    )


def generate_markdown_report(report: SchemaReport, output_file: str = '.tmp/project-init/schema-extraction.md'):
    """
    Generate markdown report from schema extraction.
    
    Args:
        report: SchemaReport object
        output_file: Output file path
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write("# Database Schema Extraction\n\n")
        f.write(f"**ORM Framework**: {report.orm_framework or 'Unknown'}\n")
        f.write(f"**Total Entities**: {len(report.entities)}\n\n")
        
        for entity in report.entities:
            f.write(f"## {entity.name}\n\n")
            f.write(f"**Table**: `{entity.table_name}`\n\n")
            f.write("### Fields\n\n")
            f.write("| Name | Type | Nullable | Constraints |\n")
            f.write("|------|------|----------|-------------|\n")
            
            for field in entity.fields:
                constraints = []
                if field.primary_key:
                    constraints.append("PRIMARY KEY")
                if field.unique:
                    constraints.append("UNIQUE")
                if field.foreign_key:
                    constraints.append(f"FK → {field.foreign_key}")
                
                f.write(f"| {field.name} | {field.type} | {'Yes' if field.nullable else 'No'} | {', '.join(constraints) or '-'} |\n")
            
            f.write("\n")
        
        if report.relationships:
            f.write("## Relationships\n\n")
            f.write("| From | To | Type | Field |\n")
            f.write("|------|----|----- |-------|\n")
            for rel in report.relationships:
                f.write(f"| {rel['from']} | {rel['to']} | {rel['type']} | {rel['field']} |\n")
            f.write("\n")
    
    print(f"✓ Schema extraction saved to {output_file}")


def main():
    """Main entry point."""
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"Extracting database schema from: {root_dir}")
    report = extract_schema(root_dir)
    
    if not report.entities:
        print("WARNING: No schema files found or no entities extracted")
        print("Supported formats: Django models, Prisma schema")
        return 1
    
    # Generate markdown report
    generate_markdown_report(report)
    
    # Save JSON
    json_output = '.tmp/project-init/schema-extraction.json'
    os.makedirs(os.path.dirname(json_output), exist_ok=True)
    with open(json_output, 'w') as f:
        json.dump(asdict(report), f, indent=2, default=str)
    
    print(f"✓ JSON schema saved to {json_output}")
    print(f"\nSummary:")
    print(f"  Entities found: {len(report.entities)}")
    print(f"  Relationships: {len(report.relationships)}")
    print(f"  ORM: {report.orm_framework or 'Unknown'}")
    
    return 0


if __name__ == '__main__':
    exit(main())
