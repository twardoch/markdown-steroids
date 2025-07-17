#!/bin/bash
# this_file: scripts/release.sh
# Release script for mdx-steroids package

set -e  # Exit on any error

echo "🚀 Preparing release for mdx-steroids package..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository"
    exit 1
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Working directory is not clean. Please commit your changes first."
    git status
    exit 1
fi

# Get the version from git tags
VERSION=$(python3 -c "from mdx_steroids import __version__; print(__version__)")
echo "📋 Current version: $VERSION"

# Check if this is a development version
if [[ "$VERSION" == *"dev"* ]]; then
    echo "❌ Cannot release development version: $VERSION"
    echo "Please create a git tag first with: git tag v<version>"
    exit 1
fi

# Run tests first
echo "🧪 Running tests before release..."
./scripts/test.sh

# Build the package
echo "🏗️  Building package..."
./scripts/build.sh

# Check if we have the necessary credentials for PyPI
echo "🔑 Checking PyPI credentials..."
if [ -z "$TWINE_USERNAME" ] && [ -z "$TWINE_PASSWORD" ] && [ ! -f "$HOME/.pypirc" ]; then
    echo "⚠️  No PyPI credentials found. Please set TWINE_USERNAME and TWINE_PASSWORD environment variables"
    echo "   or configure ~/.pypirc file"
    echo "   For now, we'll skip the upload step."
    SKIP_UPLOAD=1
fi

# Install twine if not present
python3 -m pip install --upgrade twine

# Check the distribution
echo "🔍 Checking distribution files..."
twine check dist/*

if [ -z "$SKIP_UPLOAD" ]; then
    # Upload to PyPI
    echo "📤 Uploading to PyPI..."
    twine upload dist/*
    
    echo "✅ Release $VERSION uploaded to PyPI successfully!"
else
    echo "⚠️  Skipping upload to PyPI (no credentials found)"
    echo "📦 Distribution files are ready in dist/ directory"
fi

# Create GitHub release if gh CLI is available
if command -v gh &> /dev/null; then
    echo "📝 Creating GitHub release..."
    
    # Check if we have a tag for this version
    if git tag -l | grep -q "^v$VERSION$"; then
        TAG="v$VERSION"
    else
        echo "⚠️  No git tag found for version $VERSION"
        echo "   Please create a tag with: git tag v$VERSION"
        exit 1
    fi
    
    # Create the release
    gh release create "$TAG" \
        --title "Release $VERSION" \
        --generate-notes \
        dist/*
    
    echo "✅ GitHub release created successfully!"
else
    echo "⚠️  GitHub CLI (gh) not found. Skipping GitHub release creation."
fi

echo "🎉 Release process completed!"