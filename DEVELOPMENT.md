# Development Guide

This document provides a comprehensive guide for developers working on mdx-steroids.

## Overview

The mdx-steroids project now includes:

1. **Git-tag-based semantic versioning** - Automatically derives version from git tags
2. **Comprehensive test suite** - Full coverage of all extensions
3. **Automated CI/CD** - GitHub Actions for testing, building, and releasing
4. **Multi-platform support** - Builds for Linux, Windows, and macOS
5. **Development scripts** - Convenient scripts for common tasks

## Quick Start

### Development Setup

```bash
# Clone the repository
git clone https://github.com/twardoch/markdown-steroids.git
cd markdown-steroids

# Set up development environment
./scripts/dev-setup.sh
```

### Running Tests

```bash
# Run all tests
./scripts/test.sh

# Run specific test file
source .venv/bin/activate
python -m pytest tests/test_version.py -v
```

### Building the Package

```bash
# Build source distribution and wheel
./scripts/build.sh
```

### Code Formatting

```bash
# Format code with black and ruff
./scripts/format.sh
```

## Version Management

The project uses git-tag-based semantic versioning:

- **Tagged versions**: `v1.0.0` → `1.0.0`
- **Development versions**: `1.0.0.dev5+abc1234` (5 commits after v1.0.0)
- **Dirty development**: `1.0.0.dev5+abc1234.dirty` (uncommitted changes)

### Creating a Release

1. Ensure all changes are committed and pushed
2. Create and push a git tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. The GitHub Actions will automatically:
   - Run tests
   - Build packages
   - Create GitHub release
   - Publish to PyPI

## CI/CD Workflows

### GitHub Actions

- **CI** (`.github/workflows/ci.yml`): Runs on push/PR to main branches
  - Tests across Python 3.8-3.12 on Linux, Windows, macOS
  - Code formatting and linting checks
  - Build verification
  
- **Release** (`.github/workflows/release.yml`): Runs on git tags
  - Full test suite
  - Package building
  - GitHub release creation
  - PyPI publication
  
- **Multi-platform Build** (`.github/workflows/multiplatform-build.yml`): 
  - Creates platform-specific artifacts
  - Uploads to GitHub releases

### Required Secrets

For automated PyPI publishing, set these GitHub secrets:

- `PYPI_API_TOKEN`: PyPI API token for publishing

## Project Structure

```
mdx-steroids/
├── mdx_steroids/           # Main package
│   ├── __init__.py         # Package initialization with version
│   ├── _version.py         # Version management system
│   └── *.py                # Extension modules
├── tests/                  # Test suite
│   ├── test_version.py     # Version system tests
│   └── test_*.py           # Extension tests
├── scripts/                # Development scripts
│   ├── dev-setup.sh        # Development environment setup
│   ├── test.sh             # Run tests
│   ├── build.sh            # Build packages
│   ├── format.sh           # Format code
│   └── release.sh          # Release workflow
├── .github/workflows/      # GitHub Actions
├── pyproject.toml          # Modern Python project configuration
├── setup.py                # Legacy setup (still needed for some tools)
└── README.md               # User documentation
```

## Testing

### Test Categories

1. **Unit Tests**: Test individual extensions
2. **Integration Tests**: Test extension combinations
3. **Version Tests**: Test version detection system
4. **Build Tests**: Test package building

### Running Tests

```bash
# All tests
python -m pytest

# Specific test file
python -m pytest tests/test_version.py

# With coverage
python -m pytest --cov=mdx_steroids

# Verbose output
python -m pytest -v
```

## Code Quality

### Tools Used

- **Black**: Code formatting
- **Flake8**: Linting
- **Ruff**: Additional linting and auto-fixes
- **MyPy**: Type checking (optional)

### Pre-commit Hooks

The project supports pre-commit hooks for automatic code formatting:

```bash
pip install pre-commit
pre-commit install
```

## Extension Development

### Adding New Extensions

1. Create the extension module in `mdx_steroids/`
2. Add to `__init__.py` `__all__` list
3. Create comprehensive tests in `tests/`
4. Update documentation

### Extension Structure

Each extension should follow the standard Python-Markdown extension pattern:

```python
from markdown import Extension

class MyExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'option1': ['default', 'Description'],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md, md_globals=None):
        # Register processors
        pass

def makeExtension(**kwargs):
    return MyExtension(**kwargs)
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure package is installed in development mode with `pip install -e .`
2. **Version detection fails**: Ensure you're in a git repository with proper tags
3. **Build fails**: Check that all dependencies are installed
4. **Tests fail**: Ensure development dependencies are installed

### Debug Mode

Enable debug logging for version detection:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from mdx_steroids import __version__
print(__version__)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Format code with `./scripts/format.sh`
7. Submit a pull request

## Release Process

### Manual Release

```bash
# Ensure clean working directory
git status

# Create and push tag
git tag v1.0.0
git push origin v1.0.0

# Or use the release script (for testing)
./scripts/release.sh
```

### Automated Release

Simply push a git tag - the GitHub Actions will handle the rest:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The automated process will:
1. Run full test suite
2. Build source distribution and wheel
3. Create GitHub release with artifacts
4. Publish to PyPI
5. Update documentation