# UDS JSON Schema

JSON Schema validation for Universal Dashboard Specification v0.1.0.

## Overview

**Schema Version**: JSON Schema Draft 2020-12
**UDS Version**: 0.1.0
**Schema Type**: Monolithic (single file)
**File**: `uds-schema-0.1.0.json`

This schema provides complete structural and type validation for UDS documents, including type-specific options validation for all 19 panel types.

## Features

### Core Validation
- **Required properties**: Validates all REQUIRED fields per specification
- **Type checking**: Enforces correct data types for all properties
- **Pattern validation**: Validates identifiers (snake_case), URIs, dates, emails
- **Enum validation**: Restricts values to allowed options

### Conditional Schemas
- **Layout types**: Different validation for grid/sections/tabs/flow layouts
- **Panel types**: Type-specific options schemas for all 19 panel types
- **Hybrid bindings**: Validates goal-oriented panel bindings (OKR, Scorecard, Roadmap)

### Panel Type Coverage

**Core Types** (7):
- KPI - With comparison, sparkline, target, thresholds
- Trend - Line/area charts with axes, legend, markers
- Bar - Horizontal/vertical with stacking, sorting
- Table - Columns, sorting, pagination, search
- Pie - Pie/donut with labels, legend
- Text - Markdown with metric interpolation
- Progress - Progress bars/rings with targets

**Extended Types** (9):
- Scatter - X/Y with size/colour encoding
- Heatmap - 2D colour intensity
- Funnel - Conversion stages
- Gauge - Zones and targets
- Map - Choropleth geographic
- Treemap - Hierarchical size/colour
- Histogram - Distribution binning
- Waterfall - Cumulative changes
- Bullet - Target with ranges

**Goal-Oriented Types** (3):
- OKR - Objectives and key results
- Scorecard - Balanced scorecard
- Roadmap - Timeline with dependencies

## Usage

### Command-Line Validation

#### Using AJV (Recommended)

Install AJV CLI:
```bash
npm install -g ajv-cli ajv-formats
```

Validate a single file:
```bash
ajv validate -s schemas/uds-schema-0.1.0.json -d examples/minimal.uds.yaml
```

Validate all examples:
```bash
for file in examples/**/*.uds.yaml; do
  echo "Validating $file"
  ajv validate -s schemas/uds-schema-0.1.0.json -d "$file" || echo "FAILED: $file"
done
```

#### Using Python with jsonschema

Install dependencies:
```bash
pip install jsonschema pyyaml
```

Python validation script:
```python
import json
import yaml
from jsonschema import validate, Draft202012Validator

# Load schema
with open('schemas/uds-schema-0.1.0.json', 'r') as f:
    schema = json.load(f)

# Load and validate YAML document
with open('examples/minimal.uds.yaml', 'r') as f:
    document = yaml.safe_load(f)

validator = Draft202012Validator(schema)
errors = list(validator.iter_errors(document))

if errors:
    for error in errors:
        print(f"Error at {'.'.join(str(p) for p in error.path)}: {error.message}")
else:
    print("Validation successful!")
```

#### Using Node.js with Ajv

```javascript
const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const YAML = require('yaml');
const fs = require('fs');

const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv);

// Load schema
const schema = JSON.parse(fs.readFileSync('schemas/uds-schema-0.1.0.json', 'utf8'));
const validate = ajv.compile(schema);

// Load and validate YAML
const doc = YAML.parse(fs.readFileSync('examples/minimal.uds.yaml', 'utf8'));
const valid = validate(doc);

if (!valid) {
  console.error('Validation errors:', validate.errors);
} else {
  console.log('Valid UDS document!');
}
```

### Programmatic Usage

#### TypeScript with type generation

Generate TypeScript types from schema:
```bash
npm install -g json-schema-to-typescript
json2ts schemas/uds-schema-0.1.0.json > src/types/uds.ts
```

#### IDE Integration

**VS Code**

Add to `.vscode/settings.json`:
```json
{
  "yaml.schemas": {
    "./schemas/uds-schema-0.1.0.json": ["**/*.uds.yaml", "**/*.uds.yml"]
  }
}
```

**JetBrains IDEs** (IntelliJ, WebStorm, PyCharm)

1. Go to **Settings → Languages & Frameworks → Schemas and DTDs → JSON Schema Mappings**
2. Add new schema:
   - **Schema file**: `schemas/uds-schema-0.1.0.json`
   - **Schema version**: Draft 2020-12
   - **File path pattern**: `*.uds.yaml`, `*.uds.yml`

## Validation Scripts

### Bash Script

See `scripts/validate-examples.sh` for automated validation of all examples.

### CI/CD Integration

**GitHub Actions**:
```yaml
name: Validate UDS Examples
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install -g ajv-cli ajv-formats
      - run: ./scripts/validate-examples.sh
```

## Schema Structure

### Root Object
```json
{
  "uds": "0.1.0",
  "dashboard": { ... }
}
```

### Main Definitions ($defs)

**Core structures**:
- `Dashboard` - Root dashboard configuration
- `Metadata` - Document metadata
- `Persona` - User persona configuration
- `SemanticSource` - Semantic layer connection
- `Layout` - Layout configuration (grid/sections/tabs/flow)
- `Panel` - Panel definition with type-specific options

**Data binding**:
- `DataBinding` - Metric and dimension bindings
- `MetricRef` - Metric reference (string or object)
- `DimensionRef` - Dimension reference (string or object)
- `FilterExpression` - Filter conditions
- `TimeRange` - Time range specification
- `DerivedMetric` - Calculated metric definitions

**Panel options** (19 types):
- `KpiOptions`, `TrendOptions`, `BarOptions`, `TableOptions`, `PieOptions`, `TextOptions`, `ProgressOptions`
- `ScatterOptions`, `HeatmapOptions`, `FunnelOptions`, `GaugeOptions`, `MapOptions`, `TreemapOptions`, `HistogramOptions`, `WaterfallOptions`, `BulletOptions`
- `OkrOptions`, `ScorecardOptions`, `RoadmapOptions`

**Supporting config**:
- `AxisConfig` - Chart axes configuration
- `LegendConfig` - Legend settings
- `TooltipConfig` - Tooltip configuration
- `ThresholdConfig` - Status thresholds
- `Format` - Number/currency/percent formatting
- `Theme` - Visual theming
- `I18n` - Internationalisation
- `ErrorHandling` - Error handling strategies
- `Generation` - AI generation metadata

## Conditional Validation

### Layout Type Validation

The schema uses `if`/`then` conditional schemas to validate layout-specific properties:

**Grid layout** requires: `columns`, `row_height`
**Sections layout** requires: `sections` array
**Tabs layout** requires: `tabs` array
**Flow layout** allows: `direction`, `wrap`, `gap`, etc.

### Panel Type Validation

Each panel type validates its specific `options` object:

```yaml
panels:
  - id: revenue_kpi
    type: kpi
    options:
      # Validated against KpiOptions schema
      format: { style: currency }
      comparison: { enabled: true }
      sparkline: { enabled: true }
```

Invalid options for a panel type will be rejected.

## Common Validation Errors

### Missing Required Properties

**Error**: `must have required property 'intent'`
**Fix**: Add the missing REQUIRED property to the dashboard object

### Invalid Pattern

**Error**: `must match pattern "^[a-z][a-z0-9_]*$"`
**Fix**: Use snake_case for identifiers (e.g., `revenue_kpi` not `revenueKPI`)

### Type Mismatch

**Error**: `must be integer` or `must be array`
**Fix**: Ensure the value has the correct type per the schema

### Invalid Enum Value

**Error**: `must be equal to one of the allowed values`
**Fix**: Use one of the allowed enum values (check schema for valid options)

### Panel Type Options Mismatch

**Error**: Panel type is `kpi` but options contain `x_axis`
**Fix**: Use only the options valid for that panel type (KPI doesn't have axes)

## Extending the Schema

### Adding Custom Properties

To allow custom properties while maintaining validation:

1. Use `metadata.annotations` for document-level custom data
2. Use `semantic_sources[].options` for source-specific configuration
3. Consider forking the schema for organisation-specific extensions

### Versioning

When UDS specification updates to v0.2.0:
1. Copy `uds-schema-0.1.0.json` to `uds-schema-0.2.0.json`
2. Update `$id` to reference v0.2.0
3. Update schema definitions for spec changes
4. Test against new examples

## Testing

### Validation Test Suite

Run validation against all 44 Phase 2 examples:
```bash
./scripts/validate-examples.sh
```

Expected: All examples should pass validation.

### Manual Testing

Test specific features:
```bash
# Core panel types
ajv validate -s schemas/uds-schema-0.1.0.json -d examples/core/*.yaml

# Extended types
ajv validate -s schemas/uds-schema-0.1.0.json -d examples/extended/*.yaml

# Goal-oriented types
ajv validate -s schemas/uds-schema-0.1.0.json -d examples/goal-oriented/*.yaml

# Edge cases
ajv validate -s schemas/uds-schema-0.1.0.json -d examples/edge-cases/*.yaml
```

## Schema Maintenance

### Quality Checklist

- [ ] All REQUIRED properties from spec are marked as required
- [ ] All enum values match spec exactly
- [ ] Pattern validation for identifiers (snake_case)
- [ ] Format validation for URIs, dates, emails
- [ ] Conditional schemas for all layout types
- [ ] Type-specific options for all 19 panel types
- [ ] Validates against all 44 Phase 2 examples
- [ ] British English spelling in descriptions (colour, not color)
- [ ] `additionalProperties: false` where appropriate

### Contributors

See root CONTRIBUTORS.md for contribution guidelines.

## References

- **JSON Schema Draft 2020-12**: https://json-schema.org/draft/2020-12/schema
- **UDS Specification**: `../specification/uds-specification-0.1.0.md`
- **Examples**: `../examples/`

## Version History

- **0.1.0** (2026-01) - Initial schema release
  - Complete validation for UDS v0.1.0
  - 19 panel type-specific options schemas
  - Conditional layout validation
  - Validates all 44 Phase 2 examples

---

Copyright 2026 Tortoise AI Ltd
Licensed under Apache License 2.0
