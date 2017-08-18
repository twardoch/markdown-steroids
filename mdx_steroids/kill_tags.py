#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
## steroids.md_mako

The `steroids.md_mako` feeds Markdown through the Mako templating system.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids

### Options

```yaml
  steroids.kill_tags:
    kill:          # List of HTML tags to be removed, with contents
      - del
      - sup
    kill_empty:    # List of HTML tags to be removed if they’re empty
      - p
      - div
```

Copyright (c) 2017 Adam Twardoch <adam+github@twardoch.com>
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""

__version__ = '0.5.0'

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
import lxml.etree as et

class KillTagsPostprocessor(Postprocessor):
    def kill_tags(self, html):
        tree = et.fromstring(html)
        for kill_tag in self.kill:
            et.strip_elements(tree, kill_tag, with_tail=False)
        for kill_empty_tag in self.kill_empty:
            for el in tree.xpath(
                "//{}[not(descendant-or-self::*/text()[normalize-space()]) and not(descendant-or-self::*/attribute::*)]".format(kill_empty_tag)):
                el.getparent().remove(el)
        return(et.tostring(tree, pretty_print=False))

    def run(self, html):
        self.kill = self.config.get('kill', [])
        self.kill_empty = self.config.get('kill_empty', [])
        return self.kill_tags(html)

class KillTagsExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'kill': [[], 'List of HTML tags to be removed, with contents'],
            'kill_empty': [[
                'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
            ], 'List of HTML tags to be removed if they are empty'],
        }
        super(KillTagsExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        processor = KillTagsPostprocessor(md)
        processor.config = self.getConfigs()
        md.postprocessors.add('kill_tags', processor, '_end')
        md.registerExtension(self)

def makeExtension(*args, **kwargs):
    return KillTagsExtension(*args, **kwargs)