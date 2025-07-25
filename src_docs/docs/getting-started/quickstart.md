# Quick Start Guide

This guide will help you get started with mdx-steroids in just a few minutes.

## Basic Usage

### Using with Python-Markdown

The simplest way to use mdx-steroids is with the Python-Markdown library:

```python
import markdown

# Your Markdown text
text = """
# Hello World

Press ++Ctrl+S++ to save this document.

Check out this [[Wiki Link]] for more information.

![A beautiful image](sunset.jpg "Sunset over the mountains")
"""

# Convert with extensions
html = markdown.markdown(text, extensions=[
    'mdx_steroids.keys',
    'mdx_steroids.wikilink',
    'mdx_steroids.figcap'
])

print(html)
```

### Result

The above code produces:

```html
<h1>Hello World</h1>
<p>Press <span class="keys"><kbd>Ctrl</kbd> + <kbd>S</kbd></span> to save this document.</p>
<p>Check out this <a href="/Wiki-Link/">Wiki Link</a> for more information.</p>
<figure>
  <img src="sunset.jpg" alt="A beautiful image">
  <figcaption>Sunset over the mountains</figcaption>
</figure>
```

## Common Use Cases

### 1. Keyboard Shortcuts

Use the `keys` extension to format keyboard shortcuts:

```markdown
Common shortcuts:
- Save: ++Ctrl+S++
- Copy: ++Ctrl+C++
- Paste: ++Ctrl+V++
- Type exactly: ++"Hello World"++
```

### 2. Wiki-Style Links

Enable GitHub-style wiki links with the `wikilink` extension:

```markdown
See the [[Installation Guide]] for setup instructions.
Visit our [[FAQ|Frequently Asked Questions]] page.
```

### 3. Figure Captions

Automatically convert images with titles to figures:

```markdown
![Chart](sales-2024.png "Annual sales data for 2024")
```

### 4. YAML Front Matter

Parse metadata at the beginning of your documents:

```markdown
---
title: My Article
author: Jane Doe
date: 2024-01-15
tags: [python, markdown, tutorial]
---

# My Article

Content goes here...
```

```python
md = markdown.Markdown(extensions=['mdx_steroids.meta_yaml'])
html = md.convert(text)
print(md.Meta)  # Access the metadata
```

### 5. Dynamic Content with Mako

Use Mako templating for dynamic content:

```markdown
---
user: John
items: ['Apple', 'Banana', 'Orange']
---

Hello ${user}!

Your shopping list:
% for item in items:
- ${item}
% endfor
```

## Configuration Examples

### Customizing Extensions

Most extensions accept configuration options:

```python
html = markdown.markdown(text, 
    extensions=['mdx_steroids.wikilink', 'mdx_steroids.keys'],
    extension_configs={
        'mdx_steroids.wikilink': {
            'base_url': '/docs/',
            'end_url': '.html',
            'space_sep': '_'
        },
        'mdx_steroids.keys': {
            'separator': '-',
            'strict': True,
            'camel_case': True
        }
    }
)
```

### Using with MkDocs

In your `mkdocs.yml`:

```yaml
site_name: My Documentation

markdown_extensions:
  # Enable YAML front matter
  - mdx_steroids.meta_yaml
  
  # Style keyboard shortcuts
  - mdx_steroids.keys:
      camel_case: true
      separator: ' + '
  
  # Wiki-style links
  - mdx_steroids.wikilink:
      base_url: '/docs/'
      end_url: '/'
  
  # Figure captions
  - mdx_steroids.figcap
  
  # Remove comments
  - mdx_steroids.comments
  
  # Absolute image URLs
  - mdx_steroids.absimgsrc:
      base_url: 'https://cdn.example.com/images/'
```

## Extension Combinations

Some extensions work great together:

### Documentation Site Setup

```python
extensions = [
    'mdx_steroids.meta_yaml',     # Parse front matter
    'mdx_steroids.wikilink',       # Wiki links
    'mdx_steroids.keys',           # Keyboard shortcuts
    'mdx_steroids.figcap',         # Figure captions
    'mdx_steroids.comments',       # Remove draft comments
    'mdx_steroids.translate_no',   # Protect code from translation
]
```

### Blog Setup

```python
extensions = [
    'mdx_steroids.meta_yaml',      # Post metadata
    'mdx_steroids.md_mako',        # Dynamic content
    'mdx_steroids.figcap',         # Image captions
    'mdx_steroids.absimgsrc',      # CDN images
    'mdx_steroids.interlink',      # Internal links
]
```

## Tips and Best Practices

1. **Start Simple**: Begin with one or two extensions and add more as needed
2. **Test Combinations**: Some extensions may interact, so test thoroughly
3. **Use Configuration**: Most extensions have useful configuration options
4. **Check Output**: Always verify the generated HTML meets your needs
5. **Performance**: For large documents, consider which extensions you really need

## Next Steps

- Explore individual [extension documentation](../extensions/index.md)
- Learn about [advanced configuration](configuration.md)
- See [API reference](../api/index.md) for programmatic usage
- Check out [examples](https://github.com/twardoch/markdown-steroids/tree/master/examples) in the repository