# Contributing to RippleMap AI

Thank you for your interest in contributing! This document outlines guidelines and procedures.

## Code of Conduct

- **Respectful**: Treat all contributors with respect
- **Inclusive**: Welcome ideas from diverse perspectives
- **Transparent**: Document decisions and rationale
- **Professional**: Maintain professional standards in all interactions

## Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR-USERNAME/ripplemap-ai.git
cd ripplemap-ai
git remote add upstream https://github.com/ripplemap-ai/ripplemap-ai.git
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Branch naming conventions**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test additions

### 3. Development Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 4. Run Tests

```bash
# Backend
pytest backend/tests/ -v

# Frontend
npm run test
```

### 5. Code Quality

```bash
# Black formatting
black backend/

# Flake8 linting
flake8 backend/

# isort import sorting
isort backend/

# Type checking
mypy backend/
```

## Making Changes

### Guidelines

- **One feature per PR** - Keep changes focused
- **Test coverage** - New code needs tests (>80% target)
- **Documentation** - Update docs for user-facing changes
- **Commit messages** - Clear, descriptive messages
- **Performance** - Consider impact on existing users

### Commit Message Format

```
[TYPE] Brief description

Longer explanation if needed. Reference issues:
Fixes #123
Relates to #456
```

**Types**: feat, fix, docs, style, refactor, test, chore

### Example PR

```
Title: Add rainfall analysis to disruption simulation

Description:
- Integrate IMD rainfall data with disruption scenarios
- Add sensitivity analysis for precipitation thresholds
- Update vulnerability scoring formula
- Include methodology documentation

Testing:
- Added 12 new unit tests
- Manual testing with sample data
- Performance verified (< 10s for 1M population cells)

Breaking Changes: None
```

## Testing Requirements

### Backend

```python
# Example test
def test_calculate_vulnerability_score():
    engine = SimulationEngine()
    
    impact_metrics = {...}
    population_data = {...}
    
    scores = engine.calculate_vulnerability_score(
        impact_metrics,
        population_data
    )
    
    assert scores['cell-001'] > 0
    assert scores['cell-001'] <= 1.0
```

### Frontend

```typescript
// Example test
describe('FeaturesSection', () => {
  it('renders all feature cards', () => {
    render(<FeaturesSection />);
    
    expect(screen.getByText('Interactive Map Workspace')).toBeInTheDocument();
    expect(screen.getByText('Disruption Simulation')).toBeInTheDocument();
  });
});
```

## Documentation

### When to Document

- New features
- API endpoint changes
- Configuration options
- Installation procedures
- Breaking changes

### Documentation Structure

```markdown
# Feature Name

## Overview
Brief description of what the feature does.

## Prerequisites
What's needed to use this feature.

## Usage

### Example 1: Basic usage
Code example

### Example 2: Advanced usage
Code example

## Configuration
Relevant settings and options.

## Troubleshooting
Common issues and solutions.

## References
Links to related documentation.
```

## Pull Request Process

### Before Submitting

1. **Sync with main**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test locally**:
   ```bash
   pytest backend/tests/
   npm run test
   npm run build
   ```

3. **Self-review**: Read your own PR first

4. **Descriptive PR description**: Use the template

### After Submitting

- Respond to review comments promptly
- Don't force-push unless requested
- Keep PR focused (split if too large)
- Address feedback constructively

## Code Style

### Python

- PEP 8 compliant
- Black formatting (line length: 88)
- Type hints for all functions
- Docstrings for all modules/classes/functions

```python
def calculate_distance(
    point1: Tuple[float, float],
    point2: Tuple[float, float]
) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        point1: (latitude, longitude) tuple
        point2: (latitude, longitude) tuple
    
    Returns:
        Distance in meters
    """
    ...
```

### TypeScript

- ESLint compliant
- Prettier formatting (line length: 88)
- Strict type checking enabled
- JSDoc for complex functions

```typescript
/**
 * Calculate disruption impact for a scenario.
 *
 * @param scenarioId - ID of the scenario
 * @param disruptedGraph - Modified road network
 * @returns Impact metrics per population cell
 */
export async function calculateDisruptionImpact(
  scenarioId: string,
  disruptedGraph: NetworkGraph
): Promise<DisruptionImpact> {
  ...
}
```

## Performance Considerations

- API endpoints: p95 < 500ms
- Large simulations: queue async jobs
- Database queries: use indexes
- Frontend: lazy-load components
- Caching: leverage Redis for repeated queries

## Security

- Never commit secrets or credentials
- Use environment variables for sensitive data
- Validate all user inputs
- Sanitize geographic data
- Implement CORS properly
- Use SQL parameterized queries

## Accessibility

- Semantic HTML structure
- ARIA labels where appropriate
- Keyboard navigation support
- Color contrast ratios meet WCAG AA
- Alt text for all images

## Common Tasks

### Adding a New API Endpoint

1. Create schema in `backend/app/schemas/`
2. Add model in `backend/app/models/`
3. Create endpoint in `backend/app/api/v1/endpoints/`
4. Add tests in `backend/tests/`
5. Update `docs/API_SPECIFICATION.md`

### Adding a Frontend Feature

1. Create components in `frontend/components/`
2. Add hooks in `frontend/hooks/`
3. Create tests in `frontend/__tests__/`
4. Update styles in `frontend/styles/`
5. Document usage

## Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Questions and ideas
- **Email**: contributors@ripplemap.ai
- **Chat**: Discord community (link in README)

## Reviewers & Maintainers

- @lead-maintainer
- @data-scientist
- @frontend-lead
- @devops-lead

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to project meetings

---

**Thank you for contributing to RippleMap AI!** 🎉
