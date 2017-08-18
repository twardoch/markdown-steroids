#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# mdx_steroids.replimgsrc

The `mdx_steroids.replimgsrc` extension finds and replaces portions of an image URL. 

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids/

### Options

```yaml
  steroids.replimgsrc: 
    find           : 'https://github.com/repo/blob/master/images/'
    replace        : '../img/'
```

Copyright (c) 2016 Adam Twardoch <adam+github@twardoch.com>
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""
from __future__ import absolute_import
from __future__ import unicode_literals

__version__ = '0.4.4'

from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class MDXReplaceImageSrcTreeprocessor(Treeprocessor):
    def __init__(self, md, config):
        super(MDXReplaceImageSrcTreeprocessor, self).__init__(md)
        self.config = config

    def run(self, root):
        imgs = root.getiterator("img")
        for image in imgs:
            image.set("src", self.find_replace(image.attrib["src"]))

    def find_replace(self, path):
        return path.replace(self.config["find"], self.config["replace"])

class MDXReplaceImageSrcExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'find'   : ["", "the string to find"],
            'replace': ["", "the string to replace"],
        }

        super(MDXReplaceImageSrcExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        ReplaceImageSrc = MDXReplaceImageSrcTreeprocessor(md, self.getConfigs())
        md.treeprocessors.add(
            "ReplaceImageSrc",
            ReplaceImageSrc,
            "_end"
        )
        md.registerExtension(self)


def makeExtension(*args, **kwargs):
    return MDXReplaceImageSrcExtension(*args, **kwargs)
