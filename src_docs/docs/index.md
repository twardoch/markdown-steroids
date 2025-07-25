# mdx-steroids

Welcome to **mdx-steroids** - a powerful collection of Python Markdown extensions that supercharge your Markdown processing workflow!

## What is mdx-steroids?

mdx-steroids provides a comprehensive suite of extensions for the [Python-Markdown](https://python-markdown.github.io/) library, offering enhanced control over HTML output and enabling advanced features not available in standard Markdown.

## Key Features

<div class="grid cards" markdown>

-   **🖼️ Enhanced Image Handling**
    
    Absolute paths, responsive attributes, figure captions, smart processing, and URL replacement
    
-   **🔧 Content Processing**
    
    Mako templating, YAML front matter, comment stripping, tag removal
    
-   **⌨️ Advanced Formatting**
    
    Keyboard shortcuts styling, wikilinks, custom link processing
    
-   **🚀 Easy Integration**
    
    Works seamlessly with MkDocs, Sphinx, and other Python-based tools

</div>

## Quick Example

```python
import markdown

text = """
---
title: My Document
---

Press ++Ctrl+S++ to save.

[[Wiki Link]] to another page.

![Image](photo.jpg "This becomes a figure caption")
"""

html = markdown.markdown(text, extensions=[
    'mdx_steroids.meta_yaml',
    'mdx_steroids.keys',
    'mdx_steroids.wikilink',
    'mdx_steroids.figcap'
])
```

## Getting Started

<div class="grid cards" markdown>

-   **[Installation](getting-started/installation.md)**
    
    Get mdx-steroids up and running in minutes

-   **[Quick Start](getting-started/quickstart.md)**
    
    Learn the basics with practical examples

-   **[Configuration](getting-started/configuration.md)**
    
    Customize extensions to fit your needs

</div>

## Available Extensions

| Extension | Description |
|-----------|-------------|
| [absimgsrc](extensions/absimgsrc.md) | Convert relative image URLs to absolute |
| [comments](extensions/comments.md) | Remove special HTML comments |
| [figcap](extensions/figcap.md) | Convert images with titles to figures with captions |
| [img_smart](extensions/img_smart.md) | Advanced image processing with caching |
| [interlink](extensions/interlink.md) | Process internal Markdown links |
| [keys](extensions/keys.md) | Style keyboard shortcuts |
| [kill_tags](extensions/kill_tags.md) | Remove HTML elements by selector |
| [md_mako](extensions/md_mako.md) | Mako templating in Markdown |
| [meta_yaml](extensions/meta_yaml.md) | YAML front matter parsing |
| [replimgsrc](extensions/replimgsrc.md) | Find and replace in image sources |
| [translate_no](extensions/translate_no.md) | Prevent translation of elements |
| [wikilink](extensions/wikilink.md) | GitHub-style wiki links |

## Use Cases

mdx-steroids is perfect for:

- **Static Site Generators**: Enhanced features for MkDocs, Pelican, and custom generators
- **Documentation**: Technical documentation with advanced formatting needs
- **Content Management**: Blogs and websites requiring dynamic content
- **Academic Writing**: Papers and reports with figure management
- **Knowledge Bases**: Wiki-style documentation with cross-references

## Why mdx-steroids?

- **🎯 Focused**: Each extension does one thing well
- **⚙️ Configurable**: Extensive options to customize behavior
- **🔧 Extensible**: Easy to build upon or customize
- **📦 Modular**: Use only what you need
- **🐍 Pythonic**: Clean, well-documented code

## Contributing

We welcome contributions! See our [Contributing Guide](development/contributing.md) to get started.

## License

mdx-steroids is released under the [BSD 3-Clause License](about/license.md).