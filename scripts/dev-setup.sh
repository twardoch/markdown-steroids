#!/bin/bash
# this_file: scripts/dev-setup.sh
# Development environment setup script

set -e  # Exit on any error

echo "🔧 Setting up development environment for mdx-steroids..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "📥 Upgrading pip..."
python -m pip install --upgrade pip

# Install development dependencies
echo "📦 Installing development dependencies..."
python -m pip install -e .
python -m pip install -r py-requirements.txt
python -m pip install pytest pytest-cov black flake8 ruff build twine

# Install pre-commit hooks if available
if command -v pre-commit &> /dev/null; then
    echo "🪝 Installing pre-commit hooks..."
    pre-commit install
fi

echo "✅ Development environment setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "Available scripts:"
echo "  ./scripts/test.sh     - Run tests"
echo "  ./scripts/build.sh    - Build package"
echo "  ./scripts/release.sh  - Release package"