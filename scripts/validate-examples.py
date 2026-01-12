#!/usr/bin/env python3

"""
UDS Example Validation Script (Python)
=======================================
Purpose: Validate all UDS example files against the JSON Schema
Usage: python scripts/validate-examples.py [--verbose] [--category CATEGORY]
Requirements: pip install jsonschema pyyaml
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Tuple

import yaml
from jsonschema import Draft202012Validator, ValidationError


# ANSI colour codes
class Colours:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Colour


def load_schema(schema_path: Path) -> dict:
    """Load the JSON Schema file."""
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Colours.RED}Error: Schema file not found: {schema_path}{Colours.NC}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"{Colours.RED}Error: Invalid JSON in schema: {e}{Colours.NC}")
        sys.exit(1)


def load_yaml_file(file_path: Path) -> dict:
    """Load a YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"{Colours.RED}Error: Invalid YAML in {file_path}: {e}{Colours.NC}")
        return None
    except FileNotFoundError:
        print(f"{Colours.RED}Error: File not found: {file_path}{Colours.NC}")
        return None


def validate_file(file_path: Path, validator: Draft202012Validator, verbose: bool = False) -> bool:
    """Validate a single UDS file."""
    document = load_yaml_file(file_path)
    if document is None:
        return False

    errors = list(validator.iter_errors(document))

    if not errors:
        print(f"{Colours.GREEN}PASS{Colours.NC} {file_path}")
        return True
    else:
        print(f"{Colours.RED}FAIL{Colours.NC} {file_path}")
        if verbose:
            print(f"{Colours.YELLOW}Errors:{Colours.NC}")
            for error in errors:
                path = '.'.join(str(p) for p in error.path) if error.path else 'root'
                print(f"  - {path}: {error.message}")
            print()
        return False


def get_example_files(category: str = None) -> List[Tuple[str, List[Path]]]:
    """Get example files organized by category."""
    examples_dir = Path('examples')

    if category:
        # Specific category
        category_dir = examples_dir / category
        if not category_dir.exists():
            print(f"{Colours.RED}Error: Category not found: {category_dir}{Colours.NC}")
            sys.exit(1)
        return [(category, list(category_dir.glob('*.yaml')))]

    # All categories
    categories = []

    # Minimal example
    minimal = examples_dir / 'minimal.uds.yaml'
    if minimal.exists():
        categories.append(('Minimal Example', [minimal]))

    # Core examples
    core_dir = examples_dir / 'core'
    if core_dir.exists():
        categories.append(('Core Panel Types (11 files)', list(core_dir.glob('*.yaml'))))

    # Extended examples
    extended_dir = examples_dir / 'extended'
    if extended_dir.exists():
        categories.append(('Extended Panel Types (9 files)', list(extended_dir.glob('*.yaml'))))

    # Goal-oriented examples
    goal_dir = examples_dir / 'goal-oriented'
    if goal_dir.exists():
        categories.append(('Goal-Oriented Types (6 files)', list(goal_dir.glob('*.yaml'))))

    # Layout examples
    layouts_dir = examples_dir / 'layouts'
    if layouts_dir.exists():
        categories.append(('Layout Types (4 files)', list(layouts_dir.glob('*.yaml'))))

    # Persona examples
    personas_dir = examples_dir / 'personas'
    if personas_dir.exists():
        categories.append(('Persona Examples (5 files)', list(personas_dir.glob('*.yaml'))))

    # Advanced examples
    advanced_dir = examples_dir / 'advanced'
    if advanced_dir.exists():
        categories.append(('Advanced Examples (3 files)', list(advanced_dir.glob('*.yaml'))))

    # Edge cases
    edge_cases_dir = examples_dir / 'edge-cases'
    if edge_cases_dir.exists():
        categories.append(('Edge Cases (3 files)', list(edge_cases_dir.glob('*.yaml'))))

    # Generation examples
    generation_dir = examples_dir / 'generation'
    if generation_dir.exists():
        categories.append(('Generation Examples (2 files)', list(generation_dir.glob('*.yaml'))))

    return categories


def main():
    """Main validation function."""
    parser = argparse.ArgumentParser(description='Validate UDS example files against JSON Schema')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed error messages')
    parser.add_argument('-c', '--category', type=str, help='Validate only specific category')
    args = parser.parse_args()

    # Load schema
    schema_path = Path('schemas/uds-schema-0.1.0.json')
    print(f"{Colours.BLUE}========================================{Colours.NC}")
    print(f"{Colours.BLUE}UDS Example Validation{Colours.NC}")
    print(f"{Colours.BLUE}========================================{Colours.NC}")
    print()
    print(f"Schema: {schema_path}")
    print()

    schema = load_schema(schema_path)
    validator = Draft202012Validator(schema)

    # Counters
    total = 0
    passed = 0
    failed = 0

    # Get example files
    categories = get_example_files(args.category)

    # Validate files
    for category_name, files in categories:
        if files:
            print(f"{Colours.BLUE}{category_name}{Colours.NC}")
            for file_path in sorted(files):
                total += 1
                if validate_file(file_path, validator, args.verbose):
                    passed += 1
                else:
                    failed += 1
            print()

    # Summary
    print(f"{Colours.BLUE}========================================{Colours.NC}")
    print(f"{Colours.BLUE}Validation Summary{Colours.NC}")
    print(f"{Colours.BLUE}========================================{Colours.NC}")
    print()
    print(f"Total files:  {total}")
    print(f"{Colours.GREEN}Passed:       {passed}{Colours.NC}")

    if failed > 0:
        print(f"{Colours.RED}Failed:       {failed}{Colours.NC}")
        print()
        print(f"{Colours.YELLOW}Tip: Run with --verbose to see detailed error messages{Colours.NC}")
        sys.exit(1)
    else:
        print(f"{Colours.GREEN}Failed:       {failed}{Colours.NC}")
        print()
        print(f"{Colours.GREEN}All examples passed validation!{Colours.NC}")
        sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colours.YELLOW}Validation interrupted{Colours.NC}")
        sys.exit(130)
    except Exception as e:
        print(f"{Colours.RED}Unexpected error: {e}{Colours.NC}")
        sys.exit(1)
