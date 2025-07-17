#!/bin/bash
# this_file: scripts/test.sh
# Test script for mdx-steroids package

set -e  # Exit on any error

echo "🧪 Running tests for mdx-steroids package..."

# Install test dependencies
echo "📥 Installing test dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install pytest pytest-cov black flake8 ruff

# Install package in development mode
echo "📦 Installing package in development mode..."
python3 -m pip install -e .

# Run code formatting checks
echo "🎨 Checking code formatting with black..."
black --check . || {
    echo "❌ Code formatting check failed. Run 'black .' to fix."
    exit 1
}

# Run linting
echo "🔍 Running linting with flake8..."
flake8 . --max-line-length=88 --extend-ignore=E203,W503 || {
    echo "❌ Linting check failed."
    exit 1
}

# Run additional linting with ruff
echo "🔍 Running additional linting with ruff..."
ruff check . || {
    echo "❌ Ruff linting check failed."
    exit 1
}

# Run tests
echo "🧪 Running pytest..."
python3 -m pytest tests/ -v --cov=mdx_steroids --cov-report=term-missing --cov-report=html

echo "✅ All tests passed!"