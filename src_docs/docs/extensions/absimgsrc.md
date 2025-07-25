# absimgsrc - Absolute Image URLs

The `absimgsrc` extension converts relative image URLs to absolute URLs by prepending a configurable base URL. This is essential when serving images from a CDN or when your content will be viewed from different URL contexts.

## Features

- Automatically converts relative image paths to absolute URLs
- Preserves existing absolute URLs
- Supports all common URL schemes
- Simple configuration with just one parameter
- Lightweight with minimal performance impact

## Basic Usage

### Python Example

```python
import markdown

text = '''
![Logo](images/logo.png)
![Photo](photos/sunset.jpg)
![External](https://example.com/image.png)
'''

html = markdown.markdown(
    text,
    extensions=['mdx_steroids.absimgsrc'],
    extension_configs={
        'mdx_steroids.absimgsrc': {
            'base_url': 'https://cdn.mysite.com/'
        }
    }
)
```

**Output:**
```html
<p><img alt="Logo" src="https://cdn.mysite.com/images/logo.png" /></p>
<p><img alt="Photo" src="https://cdn.mysite.com/photos/sunset.jpg" /></p>
<p><img alt="External" src="https://example.com/image.png" /></p>
```

### MkDocs Configuration

```yaml
# mkdocs.yml
markdown_extensions:
  - mdx_steroids.absimgsrc:
      base_url: 'https://cdn.example.com/docs/'
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `base_url` | string | `None` | The base URL to prepend to relative image paths |

## Use Cases

### 1. CDN Integration

Serve images from a content delivery network:

```yaml
mdx_steroids.absimgsrc:
  base_url: 'https://cdn.jsdelivr.net/gh/username/repo@main/'
```

### 2. Multi-Environment Deployment

Use environment variables for different deployments:

```python
import os
import markdown

base_url = os.environ.get('IMAGE_BASE_URL', '/images/')

html = markdown.markdown(
    content,
    extensions=['mdx_steroids.absimgsrc'],
    extension_configs={
        'mdx_steroids.absimgsrc': {'base_url': base_url}
    }
)
```

### 3. GitHub Pages

Serve images from your repository:

```yaml
mdx_steroids.absimgsrc:
  base_url: 'https://raw.githubusercontent.com/username/repo/main/docs/'
```

### 4. Documentation Versioning

Include version in image paths:

```python
version = '2.0'
base_url = f'https://docs.example.com/v{version}/images/'

html = markdown.markdown(
    content,
    extensions=['mdx_steroids.absimgsrc'],
    extension_configs={
        'mdx_steroids.absimgsrc': {'base_url': base_url}
    }
)
```

## Advanced Examples

### Conditional Base URL

Apply different base URLs based on image location:

```python
# Custom wrapper around absimgsrc
def process_markdown(text, environment='dev'):
    if environment == 'production':
        base_url = 'https://cdn.production.com/'
    elif environment == 'staging':
        base_url = 'https://cdn.staging.com/'
    else:
        base_url = '/local/images/'
    
    return markdown.markdown(
        text,
        extensions=['mdx_steroids.absimgsrc'],
        extension_configs={
            'mdx_steroids.absimgsrc': {'base_url': base_url}
        }
    )
```

### Integration with Build Tools

Example with a static site generator build script:

```python
# build.py
import markdown
import os
from pathlib import Path

def build_docs():
    # Determine base URL from build context
    if os.environ.get('CI'):
        base_url = 'https://cdn.myproject.com/'
    else:
        base_url = '/assets/images/'
    
    md = markdown.Markdown(
        extensions=['mdx_steroids.absimgsrc'],
        extension_configs={
            'mdx_steroids.absimgsrc': {'base_url': base_url}
        }
    )
    
    # Process all markdown files
    for md_file in Path('docs').glob('**/*.md'):
        html = md.convert(md_file.read_text())
        # Save HTML files...
```

## How It Works

The extension uses a `TreeProcessor` that:

1. Parses the HTML tree after Markdown conversion
2. Finds all `<img>` elements
3. Checks if the `src` attribute contains a relative URL
4. Prepends the `base_url` to relative URLs
5. Preserves absolute URLs (http://, https://, etc.)

### Recognized URL Schemes

The following URL schemes are considered absolute and won't be modified:

- `http://`, `https://`
- `ftp://`, `ftps://`
- `mailto:`
- `file://`
- `data:`
- `tel:`
- And others...

## Best Practices

1. **Always use trailing slash**: Include a trailing slash in your `base_url` to avoid path issues:
   ```yaml
   base_url: 'https://cdn.example.com/'  # Good
   base_url: 'https://cdn.example.com'   # May cause issues
   ```

2. **Use HTTPS**: Always prefer HTTPS URLs for security:
   ```yaml
   base_url: 'https://cdn.example.com/'  # Recommended
   ```

3. **Environment-specific configuration**: Use environment variables for flexibility:
   ```python
   base_url = os.getenv('CDN_URL', 'https://default-cdn.com/')
   ```

4. **Version your assets**: Include version numbers or hashes in paths:
   ```yaml
   base_url: 'https://cdn.example.com/v2.1.0/'
   ```

## Common Issues and Solutions

### Issue: Images not loading

**Symptom**: Images return 404 errors

**Solution**: Verify the base URL is correct and accessible:
```bash
curl -I https://your-cdn.com/test-image.png
```

### Issue: Double slashes in URLs

**Symptom**: URLs like `https://cdn.com//images/photo.png`

**Solution**: Ensure your image paths don't start with `/`:
```markdown
![Good](images/photo.png)
![Bad](/images/photo.png)
```

### Issue: Mixed content warnings

**Symptom**: Browser shows mixed content warnings

**Solution**: Use HTTPS for your base URL:
```yaml
base_url: 'https://cdn.example.com/'  # Not http://
```

## Integration with Other Extensions

`absimgsrc` works well with:

- **[img_smart](img_smart.md)**: Process images first with img_smart, then apply absolute URLs
- **[replimgsrc](replimgsrc.md)**: Use replimgsrc for pattern replacement, absimgsrc for base URL
- **[figcap](figcap.md)**: Convert to figures first, then apply absolute URLs

Example combined usage:

```yaml
markdown_extensions:
  - mdx_steroids.figcap          # First: create figures
  - mdx_steroids.img_smart        # Second: process images
  - mdx_steroids.absimgsrc:       # Last: apply CDN URLs
      base_url: 'https://cdn.example.com/'
```

## Performance Considerations

- **Lightweight**: Minimal performance impact
- **No external requests**: Only modifies URLs, doesn't fetch images
- **Efficient tree traversal**: Uses ElementTree's efficient iterator

## See Also

- [replimgsrc](replimgsrc.md) - For pattern-based URL replacement
- [img_smart](img_smart.md) - For advanced image processing
- [Configuration Guide](../getting-started/configuration.md) - General configuration help