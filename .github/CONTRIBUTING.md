# Contributing to UDS (Universal Data Standard)

## Branching Strategy

We use a two-branch workflow:

- **`main`** - Production branch, always deployable
- **`dev`** - Development branch for integrating features

### Branch Protection Rules

**⚠️ IMPORTANT:** While GitHub doesn't enforce these rules automatically on our current plan, all team members must follow these guidelines:

#### Main Branch (`main`)
- **No direct commits** - All changes must come through pull requests
- **Require 1 approving review** - PRs need at least one approval before merging
- **Dismiss stale reviews** - Re-request review when pushing new commits
- **Status checks** - Ensure validation passes before merging
- **Includes administrators** - Admins must also follow these rules

## Development Workflow

### 1. Create a Feature Branch
```bash
# Start from dev branch
git checkout dev
git pull origin dev

# Create your feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Follow existing schema patterns
- Maintain consistency with UDS specification
- Update documentation for schema changes
- Add examples for new features

### 3. Validate Your Changes
```bash
# Validate schemas (if validation scripts exist)
npm run validate  # or python validate.py

# Check JSON formatting
# Ensure all JSON files are properly formatted

# Review specification documents
# Ensure documentation matches schema changes
```

### 4. Commit Your Changes
```bash
git add <files>
git commit -m "Brief description of changes"
```

For commits on feature branches, use:
```bash
git config user.name "antnewman"
git config user.email "antjsnewman@outlook.com"
```

### 5. Push and Create Pull Request
```bash
# Push your branch
git push origin feature/your-feature-name

# Create PR via GitHub UI targeting 'dev' branch
```

### 6. Code Review Process
- At least **one approving review** required
- Address all review comments
- Re-request review after making changes
- Ensure schema validation passes

### 7. Merging
- Merge feature branches into `dev` after approval
- Merge `dev` into `main` only for releases

## Pull Request Guidelines

- Provide clear description of changes
- Link related issues if applicable
- Keep PRs focused and reasonably sized
- Ensure all validation passes
- Target `dev` branch (not `main`) for feature PRs

## Schema Guidelines

- **Consistency** - Maintain consistent naming conventions
- **Documentation** - Document all schema fields
- **Versioning** - Follow semantic versioning for schema changes
- **Examples** - Provide example data for new schemas
- **Backward Compatibility** - Consider impact of breaking changes

## Feature Branch Naming Convention

Use consistent `feature/` prefix for all feature branches:

✅ **Good:**
- `feature/add-risk-schema`
- `feature/update-specification`
- `feature/improve-examples`

❌ **Avoid:**
- `updates` (too generic)
- `my-changes` (unclear purpose)
- `testing` (not descriptive)

## Project Structure

```
/schemas         - JSON schema definitions
/specification   - UDS specification documents
/examples        - Example data files
/scripts         - Validation and utility scripts
```

## Validation

- **Schema Validation** - Ensure schemas are valid JSON Schema
- **Example Validation** - Verify examples conform to schemas
- **Documentation** - Check documentation is up to date
- **Consistency** - Verify naming and structure consistency

## Getting Help

- Check existing documentation (README.md, specification)
- Review similar schemas in the codebase
- Ask team members for clarification
- Create an issue for questions or proposals

## Important Notes

- **Specification Alignment** - Changes must align with UDS goals
- **Community Input** - Consider impact on UDS adopters
- **Documentation** - Update specification alongside schema changes
- **Examples** - Maintain comprehensive examples

---

**Remember:** Even though GitHub doesn't automatically enforce branch protection, maintaining this workflow ensures quality and prevents issues with the specification.
