#!/bin/bash
# this_file: scripts/format.sh
# Code formatting script

set -e  # Exit on any error

echo "🎨 Formatting code..."

# Install formatting tools
python3 -m pip install black ruff

# Format with black
echo "🔧 Running black formatter..."
black .

# Fix with ruff
echo "🔧 Running ruff auto-fixes..."
ruff check --fix .

echo "✅ Code formatting complete!"