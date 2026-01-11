# UDS Examples

This directory contains example UDS dashboards demonstrating various features and patterns of the Universal Dashboard Specification v0.1.0.

## Overview

**Total Examples**: 44 YAML files
**Specification Version**: 0.1.0
**Purpose**: Documentation, test fixtures, reference implementations

## Directory Structure

### Core Panel Types (`core/` - 11 files)
REQUIRED panel types that all conformant implementations MUST support:

- `kpi-basic.uds.yaml` - Single KPI with currency formatting
- `kpi-comparison.uds.yaml` - KPI with period-over-period comparison, sparkline, and thresholds
- `trend-basic.uds.yaml` - Simple line chart showing metric over time
- `trend-multi-series.uds.yaml` - Multiple metrics with dimensional breakdown
- `bar-basic.uds.yaml` - Horizontal bar chart with top N grouping
- `bar-stacked.uds.yaml` - Stacked/grouped bar with two dimensions
- `table-basic.uds.yaml` - Data table with sorting and pagination
- `table-conditional.uds.yaml` - Table with conditional formatting and data bars
- `pie-basic.uds.yaml` - Donut chart with top N grouping
- `text-basic.uds.yaml` - Text panel with markdown and metric interpolation
- `progress-basic.uds.yaml` - Progress toward target with time-adjusted status

### Extended Panel Types (`extended/` - 9 files)
RECOMMENDED panel types for richer visualisations:

- `scatter-basic.uds.yaml` - Scatter plot with size and colour encoding
- `heatmap-basic.uds.yaml` - Two-dimensional heatmap with colour intensity
- `funnel-basic.uds.yaml` - Conversion funnel with stage progression
- `gauge-basic.uds.yaml` - Gauge with threshold zones and target marker
- `map-choropleth.uds.yaml` - Geographic choropleth map
- `treemap-basic.uds.yaml` - Hierarchical treemap with size and colour metrics
- `histogram-basic.uds.yaml` - Distribution histogram with auto binning
- `waterfall-basic.uds.yaml` - Waterfall chart showing cumulative changes
- `bullet-basic.uds.yaml` - Bullet chart with target and qualitative ranges

### Goal-Oriented Types (`goal-oriented/` - 6 files)
RECOMMENDED panel types using hybrid data binding pattern:

- `progress-milestones.uds.yaml` - Progress with quarterly milestones
- `okr-company.uds.yaml` - Company-level OKRs with weighted scoring
- `okr-team.uds.yaml` - Team OKRs grouped by department
- `scorecard-balanced.uds.yaml` - Balanced scorecard with dynamic bindings
- `scorecard-static.uds.yaml` - Scorecard with static perspective definitions
- `roadmap-product.uds.yaml` - Product roadmap with dependencies and swim lanes

### Layout Types (`layouts/` - 4 files)
Different layout patterns for organising panels:

- `grid-responsive.uds.yaml` - Responsive grid with breakpoints
- `sections-collapsible.uds.yaml` - Collapsible sections layout
- `tabs-multi.uds.yaml` - Multi-tab layout with badges
- `flow-cards.uds.yaml` - Auto-flowing card layout

### Persona Examples (`personas/` - 5 files)
Dashboards optimised for different user personas:

- `executive-summary.uds.yaml` - High-level summary for executives
- `analyst-exploration.uds.yaml` - Comprehensive analysis workbench
- `manager-team.uds.yaml` - Team performance monitoring
- `operator-realtime.uds.yaml` - Real-time operations monitoring
- `external-client.uds.yaml` - Client-facing dashboard with embedding

### Advanced Examples (`advanced/` - 3 files)
Complex real-world scenarios:

- `sales-executive-q4.uds.yaml` - Multi-source executive dashboard with theming and i18n
- `multi-source.uds.yaml` - Combining data from multiple semantic sources
- `derived-metrics.uds.yaml` - Arithmetic, conditional, window, and case expressions

### Edge Cases (`edge-cases/` - 3 files)
Error handling and special scenarios:

- `empty-data.uds.yaml` - Graceful handling of empty data states
- `error-fallback.uds.yaml` - Error handling and retry configuration
- `conditional-display.uds.yaml` - Conditional panel visibility

### Generation Examples (`generation/` - 2 files)
AI generation workflow:

- `generation-request.uds.yaml` - AI generation request with constraints
- `generation-output.uds.yaml` - AI-generated dashboard with confidence scores

### Minimal Example (`minimal.uds.yaml`)
The absolute minimum valid UDS document (from Phase 0).

## Usage

### Viewing Examples

Each example includes:
- Header comment explaining purpose and demonstrated features
- Relevant specification section references
- Inline comments explaining non-obvious choices
- Realistic fictional data

### Running Validation

To validate YAML syntax:
```bash
# Check all files are valid YAML
find examples -name "*.yaml" -exec python3 -c "import yaml; yaml.safe_load(open('{}'))" \;

# Count examples
find examples -name "*.uds.yaml" | wc -l

# Check all have UDS version
grep -l "^uds:" examples/**/*.yaml | wc -l

# Check all have intent
grep -l "intent:" examples/**/*.yaml | wc -l
```

### Testing Against JSON Schema

When the JSON Schema is available (Phase 3), validate with:
```bash
# Validate all examples against schema
for file in examples/**/*.yaml; do
  echo "Validating $file"
  ajv validate -s schema/uds-0.1.0.json -d "$file"
done
```

## Fictional Data Sources

Examples use consistent fictional semantic sources:

**Sales/Revenue**:
```yaml
- id: sales
  type: cube
  endpoint: "https://cube.example.com/cubejs-api/v1"
```

**HR/People**:
```yaml
- id: hr
  type: dbt
  endpoint: "https://dbt.example.com/semantic-layer/v1"
```

**Goals/OKRs**:
```yaml
- id: goals
  type: cube
  endpoint: "https://cube.example.com/cubejs-api/v1"
```

**Metrics/Finance**:
```yaml
- id: metrics
  type: cube
  endpoint: "https://cube.example.com/cubejs-api/v1"
```

## Metric References

Common fictional metrics used across examples:

- `sales.total_revenue`
- `sales.total_orders`
- `sales.average_order_value`
- `sales.conversion_rate`
- `sales.quota_attainment`
- `customers.nps_score`
- `customers.satisfaction_score`
- `hr.employee_count`
- `goals.progress`
- `goals.confidence_score`

## Conformance Testing

Examples are designed to become test fixtures for:

1. **Parser validation** - Do parsers correctly read all properties?
2. **Renderer testing** - Do renderers produce expected output?
3. **Conformance levels** - Which examples require Core/Standard/Complete support?

### Conformance Level Mapping

| Level | Required Examples |
|-------|-------------------|
| **Core** | All `core/` examples, `minimal.uds.yaml` |
| **Standard** | Core + `extended/` + `goal-oriented/` (partial) |
| **Complete** | All examples |

## Contributing

When adding new examples:

1. Use the standard header template
2. Include relevant spec section references
3. Use consistent fictional sources and metrics
4. Add inline comments for complex patterns
5. Use British English spelling (organisation, behaviour, colour)
6. Test YAML validity before committing

## Quality Checklist

- [ ] Valid YAML 1.2 syntax
- [ ] Includes `uds: "0.1.0"`
- [ ] All REQUIRED properties present
- [ ] Realistic fictional data
- [ ] Clear comments explaining patterns
- [ ] British English spelling
- [ ] Consistent formatting

## Version History

- **0.1.0** (2026-01) - Initial example collection (44 files)

---

Copyright 2026 Tortoise AI Ltd
Licensed under Apache License 2.0
