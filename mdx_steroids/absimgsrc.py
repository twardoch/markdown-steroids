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

__version__ = "0.4.4"

from urllib.parse import urljoin  # Use direct import for Python 3

from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class MDXAbsoluteImagesTreeprocessor(Treeprocessor):
    def __init__(self, md, config):
        super().__init__(md)  # Python 3 style super()
        self.config = config

    def run(self, root):
        imgs = root.iter("img")  # Modern ElementTree method
        for image in imgs:
            if "src" in image.attrib and self.is_relative(
                image.attrib["src"]
            ):  # Check if src exists
                image.set("src", self.make_external(image.attrib["src"]))

    def make_external(self, path):
        base_url = self.config["base_url"]
        # Ensure base_url ends with a slash if it's not empty and path isn't absolute
        if base_url and not base_url.endswith("/") and not path.startswith("/"):
            base_url += "/"
        return urljoin(base_url, path)

    def is_relative(self, link):
        # Consider a link relative if it doesn't start with a known scheme
        # or protocol-relative double slash. Also, consider data URIs as absolute.
        known_schemes = ["http://", "https://", "ftp://", "file://", "data:"]
        if link.startswith("//"):  # Protocol-relative
            return False
        for scheme in known_schemes:
            if link.startswith(scheme):
                return False
        return True


class MDXAbsoluteImagesExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            "base_url": [
                "",  # Changed default from None to empty string
                "The base URL to which the relative paths will be appended",
            ],
        }

        super().__init__(*args, **kwargs)  # Python 3 style super()

    def extendMarkdown(self, md):  # md_globals is not used by modern extensions
        absoluteImages = MDXAbsoluteImagesTreeprocessor(md, self.getConfigs())
        # Modern way to add treeprocessors
        md.treeprocessors.register(
            absoluteImages, "absoluteImages", 5
        )  # Priority 5, adjust as needed
        # md.registerExtension(self) # Deprecated


def makeExtension(*args, **kwargs):
    return MDXAbsoluteImagesExtension(*args, **kwargs)
