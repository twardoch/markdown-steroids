# Installation

mdx-steroids can be installed in several ways depending on your needs.

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Installation Methods

### From GitHub (Recommended)

Install the latest version directly from GitHub:

```bash
pip install git+https://github.com/twardoch/markdown-steroids.git
```

### From Source

Clone the repository and install in development mode:

```bash
git clone https://github.com/twardoch/markdown-steroids.git
cd markdown-steroids
pip install -e .
```

### For Development

If you're planning to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/twardoch/markdown-steroids.git
cd markdown-steroids

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install in editable mode with development dependencies
pip install -e .
pip install -r py-requirements.txt
```

## Dependencies

mdx-steroids automatically installs these core dependencies:

- `markdown>=3.5.0` - The Python Markdown library
- `mako>=1.0.7` - Templating engine for md_mako extension
- `pymdown-extensions>=9.0` - Additional Markdown extensions
- `cssselect>=1.0.1` - CSS selector support
- `lxml>=3.8.0` - XML/HTML processing
- `beautifulsoup4>=4.6.0` - HTML parsing and manipulation

### Optional Dependencies

Some extensions may require additional packages:

- `filetype` - For img_smart file type detection
- `imageio` - For img_smart image processing
- `pillow` - For advanced image operations

Install optional dependencies as needed:

```bash
pip install filetype imageio pillow
```

## Verifying Installation

After installation, verify that mdx-steroids is properly installed:

```python
import mdx_steroids
print(mdx_steroids.__version__)

# Test a simple extension
import markdown
html = markdown.markdown("Press ++Ctrl+S++", extensions=['mdx_steroids.keys'])
print(html)
```

## Integration with Tools

### MkDocs

Add mdx-steroids extensions to your `mkdocs.yml`:

```yaml
markdown_extensions:
  - mdx_steroids.keys
  - mdx_steroids.wikilink
  - mdx_steroids.figcap
  # Add more as needed
```

### Pelican

In your Pelican configuration:

```python
MARKDOWN = {
    'extension_configs': {
        'mdx_steroids.keys': {},
        'mdx_steroids.wikilink': {'base_url': '/wiki/'},
        # Add more as needed
    }
}
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you have the correct Python version:

```bash
python --version  # Should be 3.8 or higher
```

### Missing Dependencies

If optional features don't work, install the required optional dependencies:

```bash
pip install mdx-steroids[all]  # When available
# Or install specific packages
pip install filetype imageio
```

### Permission Errors

On Unix-like systems, you might need to use `sudo` or install in user space:

```bash
pip install --user git+https://github.com/twardoch/markdown-steroids.git
```

## Next Steps

- Check out the [Quick Start Guide](quickstart.md) to begin using mdx-steroids
- Learn about [Configuration](configuration.md) options
- Explore individual [Extensions](../extensions/index.md)