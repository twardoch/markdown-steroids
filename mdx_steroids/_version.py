# this_file: mdx_steroids/_version.py
import subprocess
import re
import os
from typing import Optional


def get_version_from_git() -> Optional[str]:
    """Get version from git tags, following semver format."""
    try:
        # Get the latest tag
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            tag = result.stdout.strip()
            # Remove 'v' prefix if present
            if tag.startswith('v'):
                tag = tag[1:]
            
            # Validate semver format
            if re.match(r'^\d+\.\d+\.\d+$', tag):
                return tag
            else:
                print(f"Warning: Git tag '{tag}' doesn't follow semver format")
                return None
        else:
            print("Warning: No git tags found")
            return None
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: Git not available or not in a git repository")
        return None


def get_version_from_git_describe() -> Optional[str]:
    """Get version from git describe, handling commits after tags."""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--dirty", "--always"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            describe = result.stdout.strip()
            
            # If it's exactly a tag
            if re.match(r'^v?\d+\.\d+\.\d+$', describe):
                return describe[1:] if describe.startswith('v') else describe
            
            # If it's commits after a tag: v1.0.0-5-g1234567
            match = re.match(r'^v?(\d+\.\d+\.\d+)-(\d+)-g([a-f0-9]+)(-dirty)?$', describe)
            if match:
                version, commits, sha, dirty = match.groups()
                suffix = f".dev{commits}+{sha}"
                if dirty:
                    suffix += ".dirty"
                return version + suffix
                
            # If no tags exist, use commit sha
            if re.match(r'^[a-f0-9]+(-dirty)?$', describe):
                return f"0.0.0.dev0+{describe}"
                
        return None
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_version() -> str:
    """Get version from git tags or fallback to default."""
    # First try git describe for development versions
    version = get_version_from_git_describe()
    if version:
        return version
    
    # Fallback to simple tag lookup
    version = get_version_from_git()
    if version:
        return version
    
    # Final fallback
    return "0.0.0.dev0"


# Module level version
__version__ = get_version()