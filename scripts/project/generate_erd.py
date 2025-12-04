#!/usr/bin/env python3
"""
ERD Generation Script

Generates Mermaid Entity Relationship Diagrams from schema data.

Input: JSON schema data from extract_database_schema.py
Output: Mermaid ERD syntax
"""

import json
import os
from pathlib import Path
from typing import Dict, List


def generate_mermaid_erd(schema_data: Dict) -> str:
    """
    Generate Mermaid ERD from schema data.
    
    Args:
        schema_data: Dictionary containing entities and relationships
        
    Returns:
        Mermaid ERD syntax string
    """
    lines = ["erDiagram"]
    
    entities = schema_data.get('entities', [])
    relationships = schema_data.get('relationships', [])
    
    # Generate entity definitions
    for entity in entities:
        entity_name = entity['name']
        fields = entity.get('fields', [])
        
        if fields:
            lines.append(f"    {entity_name} {{")
            for field in fields:
                field_name = field['name']
                field_type = field['type']
                constraints = []
                
                if field.get('primary_key'):
                    constraints.append('PK')
                if field.get('foreign_key'):
                    constraints.append('FK')
                if field.get('unique'):
                    constraints.append('UK')
                if not field.get('nullable', True):
                    constraints.append('NOT NULL')
                
                constraint_str = f" \"{', '.join(constraints)}\"" if constraints else ""
                lines.append(f"        {field_type} {field_name}{constraint_str}")
            
            lines.append("    }")
    
    # Generate relationships
    for rel in relationships:
        from_entity = rel['from']
        to_entity = rel['to']
        rel_type = rel.get('type', '1:N')
        field = rel.get('field', '')
        
        # Convert relationship type to Mermaid syntax
        if rel_type == '1:1':
            mermaid_rel = '||--||'
        elif rel_type == '1:N':
            mermaid_rel = '||--o{'
        elif rel_type == 'N:M':
            mermaid_rel = '}o--o{'
        else:
            mermaid_rel = '||--o{'
        
        label = f' : "{field}"' if field else ''
        lines.append(f"    {from_entity} {mermaid_rel} {to_entity}{label}")
    
    return '\n'.join(lines)


def load_schema_from_json(json_file: str) -> Dict:
    """
    Load schema data from JSON file.
    
    Args:
        json_file: Path to JSON schema file
        
    Returns:
        Schema data dictionary
    """
    with open(json_file, 'r') as f:
        return json.load(f)


def save_erd(erd_content: str, output_file: str):
    """
    Save ERD content to file.
    
    Args:
        erd_content: Mermaid ERD syntax
        output_file: Output file path
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(erd_content)
    
    print(f"✓ ERD saved to {output_file}")


def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python generate_erd.py <schema-json-file> [output-file]")
        print("Example: python generate_erd.py .tmp/project-init/schema-extraction.json")
        return 1
    
    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else '.tmp/project-init/database-erd.mmd'
    
    if not Path(json_file).exists():
        print(f"ERROR: File not found: {json_file}")
        return 1
    
    print(f"Loading schema from: {json_file}")
    schema_data = load_schema_from_json(json_file)
    
    print("Generating Mermaid ERD...")
    erd_content = generate_mermaid_erd(schema_data)
    
    save_erd(erd_content, output_file)
    
    print(f"\nERD Preview:")
    print("=" * 50)
    print(erd_content)
    print("=" * 50)
    
    return 0


if __name__ == '__main__':
    exit(main())
