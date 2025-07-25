# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Documentation Infrastructure
- Comprehensive MkDocs-based documentation system
  - Material theme with custom CSS styling
  - Complete navigation structure for all sections
  - mkdocstrings plugin for API documentation
  - mike plugin for version management
- New documentation pages:
  - Project overview with feature cards (index.md)
  - Detailed installation guide
  - Quick start tutorial with examples
  - Comprehensive configuration guide
  - Extensions overview and selection guide
  - Detailed absimgsrc extension documentation
- Prepared documentation deployment infrastructure (GitHub Actions workflow template available)

#### Testing
- New comprehensive test suites:
  - test_keys.py - Tests for keyboard shortcut formatting
  - test_md_mako.py - Tests for Mako templating extension
  - test_img_smart.py - Tests for smart image processing

#### Code Quality
- Comprehensive docstrings added to:
  - absimgsrc.py - Google-style docstrings with examples
  - comments.py - Complete module documentation
- Type hints added throughout:
  - comments.py - Full type annotations
  - absimgsrc.py - Type hints for better IDE support

#### Build System
- Git-tag-based semantic versioning system
- Comprehensive test suite covering all extensions
- Automated CI/CD pipeline with GitHub Actions
- Multi-platform build support (Linux, Windows, macOS)
- Convenient build, test, and release scripts
- Code formatting and linting configuration
- Automated PyPI publishing on git tags

### Changed
- comments.py completely rewritten with:
  - Better code organization and structure
  - Comprehensive docstrings
  - Type hints throughout
  - Improved readability
- Updated package structure to support modern development workflows
- Improved error handling in version detection
- Enhanced build system with proper dependency management

### Fixed
- Missing `known_schemes` definition in absimgsrc.py
- Duplicate import statement in absimgsrc.py
- Version detection now works correctly in all environments
- Build system properly handles git repositories and source distributions

## [0.7.0] - Previous Release

### Added
- Original mdx-steroids functionality
- Collection of Python Markdown extensions
- Basic build system with setup.py