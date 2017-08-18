# mdx_steroids

A small collection of Python Markdown extensions, written by Adam Twardoch except when stated otherwise. 

* [mdx_steroids.absimgsrc](absimgsrc.md) 
* [mdx_steroids.keys](keys.md) by Issac Muse after the idea by Adam Twardoch
* [mdx_steroids.kill_tags](kill_tags.md) 
* [mdx_steroids.md_mako](md_mako.md) 
* [mdx_steroids.meta_yaml](meta_yaml.md) by Bernhard Fisseni
* [mdx_steroids.replimgsrc](replimgsrc.md) 
* [mdx_steroids.wikilink](wikilink.md) adapted from original

# Installation

```
pip install --user --upgrade  git+https://github.com/twardoch/markdown-steroids.git
```

# Code

The code is available on [https://github.com/twardoch/markdown-steroids/](https://github.com/twardoch/markdown-steroids/)

# Usage in MkDocs

In your `mkdocs.yaml` include:

```yaml
markdown_extensions:
- mdx_steroids.absimgsrc:
    base_url       : 'https://github.com/repo/blob/master/images/'
    # Base URL to which the relative paths will be appended
- mdx_steroids.keys:
    camel_case: true
    strict: false
    separator: ''
- mdx_steroids.kill_tags:
    kill_known: true
    kill_empty:
      - p
    normalize: false
- mdx_steroids.md_mako:
    python_block  : 'my_md_mako.py'
    meta:
      author: 'John Doe'
- mdx_steroids.meta_yaml
- mdx_steroids.replimgsrc:
    find           : 'https://github.com/repo/blob/master/images'
    replace        : '../img/'
- mdx_steroids.wikilink:
    base_url       : '/'
    end_url        : '/'
    html_class     : 'wikilink'
    space_sep      : '-'
```


