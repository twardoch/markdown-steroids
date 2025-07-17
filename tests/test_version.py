# this_file: tests/test_version.py
import pytest
import subprocess
import os
from mdx_steroids._version import get_version, get_version_from_git, get_version_from_git_describe
from mdx_steroids import __version__


def test_version_import():
    """Test that version can be imported from package."""
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_get_version_function():
    """Test that get_version returns a string."""
    version = get_version()
    assert isinstance(version, str)
    assert len(version) > 0


def test_version_fallback():
    """Test that fallback version works."""
    # This should work even if not in a git repo
    version = get_version()
    assert version == __version__


def test_version_format():
    """Test that version follows expected format."""
    version = get_version()
    # Should be semver-like or dev version
    assert "." in version
    # Should not be empty
    assert version != ""
    # Should not be None
    assert version is not None


def test_git_version_functions():
    """Test git version functions don't crash."""
    # These functions should not crash even if git is not available
    git_version = get_version_from_git()
    git_describe_version = get_version_from_git_describe()
    
    # Both should return None or a string
    assert git_version is None or isinstance(git_version, str)
    assert git_describe_version is None or isinstance(git_describe_version, str)


def test_development_version_format():
    """Test that development versions follow expected format."""
    version = get_version()
    if "dev" in version:
        # Should contain dev and version parts
        assert "dev" in version
        assert "." in version
    elif "+" in version:
        # Should be commit-based version
        assert "+" in version
    else:
        # Should be a clean semver
        parts = version.split(".")
        assert len(parts) >= 3
        for part in parts[:3]:
            assert part.isdigit()