# Extensions Overview

mdx-steroids provides a comprehensive collection of Markdown extensions, each designed to solve specific content authoring challenges. This page provides an overview of all available extensions and helps you choose the right ones for your project.

## Extension Categories

### Image Processing

These extensions handle image-related tasks:

- **[absimgsrc](absimgsrc.md)** - Convert relative image URLs to absolute URLs
- **[figcap](figcap.md)** - Transform images with titles into figures with captions
- **[img_smart](img_smart.md)** - Advanced image processing with dimension detection and optimization
- **[replimgsrc](replimgsrc.md)** - Find and replace patterns in image sources

### Content Processing

Extensions that modify or enhance content:

- **[comments](comments.md)** - Remove special HTML comments from output
- **[kill_tags](kill_tags.md)** - Remove specific HTML elements using CSS/XPath selectors
- **[translate_no](translate_no.md)** - Prevent automatic translation of specified elements
- **[md_mako](md_mako.md)** - Enable Mako templating for dynamic content

### Link Management

Handle various link types and formats:

- **[wikilink](wikilink.md)** - Convert wiki-style `[[links]]` to standard Markdown links
- **[interlink](interlink.md)** - Process internal links with configurable base/end URLs

### Formatting

Enhance text formatting capabilities:

- **[keys](keys.md)** / **[kbd](kbd.md)** - Style keyboard shortcuts and key combinations

### Metadata

Process document metadata:

- **[meta_yaml](meta_yaml.md)** - Parse YAML front matter at the beginning of documents

## Quick Selection Guide

### For Documentation Sites

Essential extensions for technical documentation:

```yaml
markdown_extensions:
  - mdx_steroids.meta_yaml     # Document metadata
  - mdx_steroids.keys          # Keyboard shortcuts
  - mdx_steroids.figcap        # Figure captions
  - mdx_steroids.wikilink      # Cross-references
  - mdx_steroids.translate_no  # Protect code
```

### For Blogs

Ideal for blog posts and articles:

```yaml
markdown_extensions:
  - mdx_steroids.meta_yaml     # Post metadata
  - mdx_steroids.figcap        # Image captions
  - mdx_steroids.absimgsrc     # CDN images
  - mdx_steroids.comments      # Draft notes
```

### For Knowledge Bases

Perfect for wiki-style content:

```yaml
markdown_extensions:
  - mdx_steroids.wikilink      # Wiki links
  - mdx_steroids.interlink     # Internal links
  - mdx_steroids.meta_yaml     # Page metadata
  - mdx_steroids.md_mako       # Dynamic content
```

### For Static Sites with CDN

Optimize for content delivery networks:

```yaml
markdown_extensions:
  - mdx_steroids.absimgsrc     # CDN URLs
  - mdx_steroids.img_smart     # Image optimization
  - mdx_steroids.replimgsrc    # URL migration
```

## Extension Processing Order

The order in which extensions are listed can affect the final output. Here's the recommended order:

1. **Preprocessors** (modify raw Markdown):
   - `meta_yaml` - Parse front matter first
   - `md_mako` - Process templates
   - `comments` - Remove comments
   - `wikilink` - Convert wiki links
   - `interlink` - Process internal links

2. **Inline/Block Processors** (during parsing):
   - `keys` - Keyboard shortcuts
   - `figcap` - Figure captions

3. **Tree Processors** (modify HTML tree):
   - `absimgsrc` - Absolute image URLs
   - `replimgsrc` - Replace image sources
   - `img_smart` - Smart image processing

4. **Postprocessors** (modify final HTML):
   - `kill_tags` - Remove elements
   - `translate_no` - Add translation attributes

## Performance Considerations

Some extensions have performance implications:

### Lightweight Extensions
These have minimal performance impact:
- `comments`
- `keys`
- `wikilink`
- `meta_yaml`

### Resource-Intensive Extensions
These may impact build times:
- `img_smart` - Reads image files (use caching)
- `md_mako` - Template processing
- `kill_tags` - HTML parsing with BeautifulSoup

### Optimization Tips

1. **Enable caching** where available (e.g., `img_smart`)
2. **Limit selector complexity** in `kill_tags` and `translate_no`
3. **Use specific extensions** rather than loading all
4. **Profile your build** to identify bottlenecks

## Compatibility Matrix

Most extensions are compatible with each other, but some considerations apply:

| Extension | Works Well With | Potential Conflicts | Notes |
|-----------|----------------|-------------------|-------|
| `meta_yaml` | All extensions | None | Should be listed first |
| `md_mako` | `meta_yaml` | None | Can use metadata variables |
| `figcap` | `img_smart` | None | Process in correct order |
| `wikilink` | `interlink` | None | Different link patterns |
| `kill_tags` | All | `translate_no` | May remove translated elements |

## Creating Custom Extensions

mdx-steroids extensions follow the Python-Markdown extension API. To create your own:

1. Study existing extensions for patterns
2. Inherit from appropriate base class
3. Follow the naming convention
4. Add configuration options
5. Include comprehensive tests

See our [Development Guide](../development/contributing.md) for details.

## Getting Help

- Check individual extension documentation
- Review [configuration examples](../getting-started/configuration.md)
- See [troubleshooting guide](../development/troubleshooting.md)
- Open an [issue on GitHub](https://github.com/twardoch/markdown-steroids/issues)