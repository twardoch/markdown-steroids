# Configuration Guide

This guide covers how to configure mdx-steroids extensions for your specific needs.

## Configuration Basics

### Python-Markdown Configuration

When using mdx-steroids with Python-Markdown directly, you can pass configuration options via the `extension_configs` parameter:

```python
import markdown

html = markdown.markdown(
    text,
    extensions=['mdx_steroids.wikilink', 'mdx_steroids.keys'],
    extension_configs={
        'mdx_steroids.wikilink': {
            'base_url': '/wiki/',
            'end_url': '.html',
            'space_sep': '_'
        },
        'mdx_steroids.keys': {
            'separator': ' + ',
            'strict': True
        }
    }
)
```

### MkDocs Configuration

In MkDocs, configure extensions in your `mkdocs.yml` file:

```yaml
markdown_extensions:
  - mdx_steroids.wikilink:
      base_url: '/wiki/'
      end_url: '.html'
  - mdx_steroids.keys:
      separator: ' + '
      strict: true
```

## Extension Configuration Reference

### absimgsrc

Converts relative image URLs to absolute URLs.

```yaml
mdx_steroids.absimgsrc:
  base_url: 'https://cdn.example.com/images/'
```

**Options:**
- `base_url` (str): Base URL to prepend to relative image paths

### comments

Removes special HTML comments `<!--- ... -->` from output.

```yaml
mdx_steroids.comments:
  # No configuration options
```

### figcap

Converts images with titles to figure elements with captions.

```yaml
mdx_steroids.figcap:
  # No configuration options currently
```

### img_smart

Advanced image processing with automatic dimension detection and optimization.

```yaml
mdx_steroids.img_smart:
  find: '/local/path'
  repl_path: '/actual/path'
  repl_url: '/public/url'
  alt_figure: true
  cache: '.img_cache.json'
  lazy: true
```

**Options:**
- `find` (str): String to find in image URLs
- `repl_path` (str): Replacement for local path resolution
- `repl_url` (str): Replacement for final URL
- `alt_figure` (bool): Use alt text as figure caption
- `cache` (str): Path to cache file for image metadata
- `lazy` (bool): Add loading="lazy" attribute

### interlink

Processes internal Markdown links.

```yaml
mdx_steroids.interlink:
  base_url: '/docs/'
  end_url: '/'
```

**Options:**
- `base_url` (str): Prepend to relative links
- `end_url` (str): Append to relative links

### keys / kbd

Formats keyboard shortcuts with proper styling.

```yaml
mdx_steroids.keys:
  separator: ' + '
  strict: false
  class: 'keyboard-keys'
  camel_case: true
  key_map:
    MyKey: 'Custom Key'
```

**Options:**
- `separator` (str): Character(s) between keys (default: '+')
- `strict` (bool): Use strict HTML5 nesting (default: false)
- `class` (str): CSS class for wrapper (default: 'keys')
- `camel_case` (bool): Allow CamelCase key names (default: false)
- `key_map` (dict): Custom key mappings

### kill_tags

Removes HTML elements matching selectors.

```yaml
mdx_steroids.kill_tags:
  normalize: true
  kill:
    - '.draft-only'
    - '#temp-content'
    - '!//div[@class="remove-me"]'  # XPath
  kill_known: true
  kill_empty: ['p', 'div', 'span']
```

**Options:**
- `normalize` (bool): Normalize HTML before/after processing
- `kill` (list): CSS/XPath selectors to remove
- `kill_known` (bool): Remove known problematic elements
- `kill_empty` (list): Remove empty elements of these types

### md_mako

Enables Mako templating in Markdown.

```yaml
mdx_steroids.md_mako:
  include_base: 'templates/'
  include_encoding: 'utf-8'
  include_auto: 'templates/base.mako'
  python_block: 'helpers/functions.py'
  meta:
    site_name: 'My Site'
    year: 2024
```

**Options:**
- `include_base` (str/list): Base directory for includes
- `include_encoding` (str): Encoding for included files
- `include_auto` (str): Auto-include template file
- `python_block` (str): Python file to include as module-level block
- `meta` (dict): Variables available in templates

### meta_yaml

Parses YAML front matter.

```yaml
mdx_steroids.meta_yaml:
  # No configuration options
```

### replimgsrc

Find and replace in image sources.

```yaml
mdx_steroids.replimgsrc:
  find: 'http://old-domain.com/'
  replace: 'https://new-domain.com/'
```

**Options:**
- `find` (str): String to find in image src
- `replace` (str): Replacement string

### translate_no

Prevents translation of specified elements.

```yaml
mdx_steroids.translate_no:
  normalize: false
  add:
    - 'code'
    - 'pre'
    - '.technical-term'
    - '!//span[@class="no-translate"]'  # XPath
```

**Options:**
- `normalize` (bool): Normalize HTML before/after
- `add` (list): Selectors for elements to mark as no-translate

### wikilink

Converts wiki-style links `[[Page Name]]` to standard links.

```yaml
mdx_steroids.wikilink:
  base_url: '/wiki/'
  end_url: '.html'
  space_sep: '-'
  html_class: 'wiki-link'
```

**Options:**
- `base_url` (str): Prepend to generated URLs (default: '/')
- `end_url` (str): Append to generated URLs (default: '/')
- `space_sep` (str): Replace spaces with this (default: '-')
- `html_class` (str): CSS class for links (default: 'wikilink')

## Advanced Configuration

### Combining Extensions

Some extensions work well together. Here are recommended combinations:

**Documentation Sites:**
```yaml
markdown_extensions:
  - mdx_steroids.meta_yaml        # First, to parse metadata
  - mdx_steroids.md_mako          # For dynamic content
  - mdx_steroids.comments         # Remove draft comments
  - mdx_steroids.wikilink         # Wiki-style links
  - mdx_steroids.keys             # Keyboard shortcuts
  - mdx_steroids.figcap           # Figure captions
  - mdx_steroids.translate_no     # Protect code from translation
```

**Blogs with CDN:**
```yaml
markdown_extensions:
  - mdx_steroids.meta_yaml
  - mdx_steroids.absimgsrc:
      base_url: 'https://cdn.blog.com/'
  - mdx_steroids.figcap
  - mdx_steroids.interlink:
      base_url: '/posts/'
      end_url: '/'
```

### Environment-Specific Configuration

Use environment variables for different deployments:

```python
import os
import markdown

base_url = os.environ.get('CDN_URL', 'https://default-cdn.com/')

html = markdown.markdown(text,
    extensions=['mdx_steroids.absimgsrc'],
    extension_configs={
        'mdx_steroids.absimgsrc': {
            'base_url': base_url
        }
    }
)
```

### Dynamic Configuration

Generate configuration programmatically:

```python
def get_markdown_config(environment='development'):
    config = {
        'mdx_steroids.wikilink': {
            'base_url': '/wiki/',
            'end_url': '.html' if environment == 'production' else '/'
        }
    }
    
    if environment == 'production':
        config['mdx_steroids.absimgsrc'] = {
            'base_url': 'https://cdn.production.com/'
        }
    
    return config

html = markdown.markdown(text,
    extensions=['mdx_steroids.wikilink', 'mdx_steroids.absimgsrc'],
    extension_configs=get_markdown_config('production')
)
```

## Troubleshooting Configuration

### Common Issues

1. **Extension not working**: Ensure the extension name is correct and installed
2. **Configuration ignored**: Check YAML indentation in MkDocs
3. **Conflicts between extensions**: Order matters - arrange extensions appropriately
4. **Performance issues**: Disable unused extensions, enable caching where available

### Debugging Configuration

Enable verbose output to debug configuration issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now markdown processing will show detailed debug info
html = markdown.markdown(text, extensions=['mdx_steroids.wikilink'])
```

## Best Practices

1. **Start simple**: Begin with minimal configuration and add options as needed
2. **Document your configuration**: Comment your mkdocs.yml or configuration files
3. **Test thoroughly**: Different extension combinations may interact unexpectedly
4. **Use version control**: Track configuration changes over time
5. **Consider performance**: Some extensions (like img_smart) benefit from caching