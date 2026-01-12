#!/usr/bin/env bash

# =============================================================================
# UDS Example Validation Script
# =============================================================================
# Purpose: Validate all UDS example files against the JSON Schema
# Usage: ./scripts/validate-examples.sh
# Requirements: ajv-cli, ajv-formats (install: npm install -g ajv-cli ajv-formats)
# =============================================================================

set -e  # Exit on error

# Colours for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Colour

# Counters
TOTAL=0
PASSED=0
FAILED=0

# Schema file
SCHEMA="schemas/uds-schema-0.1.0.json"

# Check if schema exists
if [ ! -f "$SCHEMA" ]; then
  echo -e "${RED}Error: Schema file not found: $SCHEMA${NC}"
  exit 1
fi

# Check if ajv is installed
if ! command -v ajv &> /dev/null; then
  echo -e "${RED}Error: ajv-cli is not installed${NC}"
  echo "Install with: npm install -g ajv-cli ajv-formats"
  exit 1
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}UDS Example Validation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Schema: $SCHEMA"
echo ""

# Function to validate a single file
validate_file() {
  local file=$1
  TOTAL=$((TOTAL + 1))

  # Run ajv validation
  if ajv validate -s "$SCHEMA" -d "$file" --strict=false 2>&1 | grep -q "valid"; then
    echo -e "${GREEN}✓${NC} $file"
    PASSED=$((PASSED + 1))
  else
    echo -e "${RED}✗${NC} $file"
    FAILED=$((FAILED + 1))

    # Show errors if verbose mode
    if [ "$VERBOSE" = "true" ]; then
      echo -e "${YELLOW}Errors:${NC}"
      ajv validate -s "$SCHEMA" -d "$file" --strict=false 2>&1 || true
      echo ""
    fi
  fi
}

# Parse arguments
VERBOSE=false
CATEGORY=""

while [[ $# -gt 0 ]]; do
  case $1 in
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    -c|--category)
      CATEGORY="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  -v, --verbose    Show detailed error messages"
      echo "  -c, --category   Validate only specific category (core, extended, etc.)"
      echo "  -h, --help       Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate files
if [ -n "$CATEGORY" ]; then
  # Validate specific category
  echo -e "${YELLOW}Category:${NC} $CATEGORY"
  echo ""

  if [ ! -d "examples/$CATEGORY" ]; then
    echo -e "${RED}Error: Category not found: examples/$CATEGORY${NC}"
    exit 1
  fi

  for file in examples/$CATEGORY/*.yaml; do
    if [ -f "$file" ]; then
      validate_file "$file"
    fi
  done
else
  # Validate all examples

  # Minimal example
  if [ -f "examples/minimal.uds.yaml" ]; then
    echo -e "${BLUE}Minimal Example${NC}"
    validate_file "examples/minimal.uds.yaml"
    echo ""
  fi

  # Core examples
  if [ -d "examples/core" ]; then
    echo -e "${BLUE}Core Panel Types (11 files)${NC}"
    for file in examples/core/*.yaml; do
      if [ -f "$file" ]; then
        validate_file "$file"
      fi
    done
    echo ""
  fi

  # Extended examples
  if [ -d "examples/extended" ]; then
    echo -e "${BLUE}Extended Panel Types (9 files)${NC}"
    for file in examples/extended/*.yaml; do
      if [ -f "$file" ]; then
        validate_file "$file"
      fi
    done
    echo ""
  fi

  # Goal-oriented examples
  if [ -d "examples/goal-oriented" ]; then
    echo -e "${BLUE}Goal-Oriented Types (6 files)${NC}"
    for file in examples/goal-oriented/*.yaml; do
      if [ -f "$file" ]; then
        validate_file "$file"
      fi
    done
    echo ""
  fi

  # Layout examples
  if [ -d "examples/layouts" ]; then
    echo -e "${BLUE}Layout Types (4 files)${NC}"
    for file in examples/layouts/*.yaml; do
      if [ -f "$file" ]; then
        validate_file "$file"
      fi
    done
    echo ""
  fi

  # Persona examples
  if [ -d "examples/personas" ]; then
    echo -e "${BLUE}Persona Examples (5 files)${NC}"
    for file in examples/personas/*.yaml; do
      if [ -f "$file" ]; then
        validate_file "$file"
      fi
    done
    echo ""
  fi

  # Advanced examples
  if [ -d "examples/advanced" ]; then
    echo -e "${BLUE}Advanced Examples (3 files)${NC}"
    for file in examples/advanced/*.yaml; do
      if [ -f "$file" ]; then
        validate_file "$file"
      fi
    done
    echo ""
  fi

  # Edge cases
  if [ -d "examples/edge-cases" ]; then
    echo -e "${BLUE}Edge Cases (3 files)${NC}"
    for file in examples/edge-cases/*.yaml; do
      if [ -f "$file" ]; then
        validate_file "$file"
      fi
    done
    echo ""
  fi

  # Generation examples
  if [ -d "examples/generation" ]; then
    echo -e "${BLUE}Generation Examples (2 files)${NC}"
    for file in examples/generation/*.yaml; do
      if [ -f "$file" ]; then
        validate_file "$file"
      fi
    done
    echo ""
  fi
fi

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Validation Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Total files:  $TOTAL"
echo -e "${GREEN}Passed:       $PASSED${NC}"

if [ $FAILED -gt 0 ]; then
  echo -e "${RED}Failed:       $FAILED${NC}"
  echo ""
  echo -e "${YELLOW}Tip: Run with --verbose to see detailed error messages${NC}"
  exit 1
else
  echo -e "${GREEN}Failed:       $FAILED${NC}"
  echo ""
  echo -e "${GREEN}All examples passed validation! ✓${NC}"
  exit 0
fi
