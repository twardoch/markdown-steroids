#!/bin/bash
# this_file: scripts/build.sh
# Build script for mdx-steroids package

set -e  # Exit on any error

echo "🔧 Building mdx-steroids package..."

# Clean previous builds
echo "📦 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
echo "📥 Installing build dependencies..."
python3 -m pip install --upgrade pip setuptools wheel build

# Build the package
echo "🏗️  Building source distribution and wheel..."
python3 -m build

# Verify the build
echo "✅ Verifying build artifacts..."
if [ -d "dist/" ]; then
    echo "📦 Build artifacts created:"
    ls -la dist/
else
    echo "❌ Build failed - no dist directory found"
    exit 1
fi

echo "✅ Build completed successfully!"