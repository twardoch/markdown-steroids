#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# mdx_steroids.absimgsrc

The `mdx_steroids.absimgsrc` replaces relative image URLs with absolute ones. 

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids/

### Options

```yaml
  mdx_steroids.absimgsrc:
    base_url       : 'https://github.com/repo/blob/master/images/' 
    # Base URL to which the relative paths will be appended
```

Copyright (c) 2016 Adam Twardoch <adam+github@twardoch.com>
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""
from __future__ import absolute_import
from __future__ import unicode_literals

__version__ = '0.4.4'

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class MDXAbsoluteImagesTreeprocessor(Treeprocessor):
    def __init__(self, md, config):
        super(MDXAbsoluteImagesTreeprocessor, self).__init__(md)
        self.config = config

    def run(self, root):
        imgs = root.getiterator("img")
        for image in imgs:
            if self.is_relative(image.attrib["src"]):
                image.set("src", self.make_external(image.attrib["src"]))

    def make_external(self, path):
        return urljoin(self.config["base_url"], path)

    def is_relative(self, link):
        if link.startswith('http'):
            return False
        return True


class MDXAbsoluteImagesExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'base_url': [None,
                         "The base URL to which the relative paths will be appended"],
        }

        super(MDXAbsoluteImagesExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        absoluteImages = MDXAbsoluteImagesTreeprocessor(md, self.getConfigs())
        md.treeprocessors.add(
            "absoluteImages",
            absoluteImages,
            "_end"
        )
        md.registerExtension(self)


def makeExtension(*args, **kwargs):
    return MDXAbsoluteImagesExtension(*args, **kwargs)
