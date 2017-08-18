#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
## steroids.kill_tags

The `steroids.kill_tags` removes requested tags from final HTML output.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids

### Options

```yaml
  steroids.kill_tags:
    kill: del strike up     # List of HTML tags to be removed, with contents
    kill_empty: p div       # List of HTML tags to be removed if they’re empty
```

Copyright (c) 2017 Adam Twardoch <adam+github@twardoch.com>
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""

__version__ = '0.5.0'

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
import lxml.html
import lxml.html.soupparser
import lxml.cssselect.LxmlHTMLTranslator
from bs4 import BeautifulSoup
import lxml.etree as et


class KillTagsPostprocessor(Postprocessor):

    def remove_keeping_tail(self, element):
        """Safe the tail text and then delete the element"""
        self._preserve_tail_before_delete(element)
        element.getparent().remove(element)

    def _preserve_tail_before_delete(self, node):
        if node.tail:  # preserve the tail
            previous = node.getprevious()
            if previous is not None:  # if there is a previous sibling it will get the tail
                if previous.tail is None:
                    previous.tail = node.tail
                else:
                    previous.tail = previous.tail + node.tail
            else:  # The parent get the tail as text
                parent = node.getparent()
                if parent.text is None:
                    parent.text = node.tail
                else:
                    parent.text = parent.text + node.tail

    def normalize_html(self):
        soup = BeautifulSoup(self.html, "html5lib")
        self.html = unicode(soup)

    def kill_tags(self):
        tree = lxml.html.fromstring(self.html)
        cx = lxml.cssselect.LxmlHTMLTranslator()
        for kill_tag in self.kill:
            for el in tree.xpath(cx.css_to_xpath(kill_tag)):
                self.remove_keeping_tail(el)
        for kill_empty_tag in self.kill_empty:
            for el in tree.xpath(
                '//{}['
                    'not(descendant-or-self::*/text()[normalize-space()])' 
                    ' and not(descendant-or-self::*/attribute::*)'
                ']'.format(kill_empty_tag)):
                self.remove_keeping_tail(el)
        self.html = et.tostring(tree, pretty_print=False)

    def run(self, html):
        self.html = html
        self.kill = self.config.get('kill', '')
        self.kill_empty = self.config.get('kill_empty', '')
        if self.config.get('normalize', False):
            self.normalize_html()
        self.kill_tags()
        if self.config.get('normalize', False):
            self.normalize_html()
            return self.html

class KillTagsExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'normalize': [False, 'Normalize HTML before processing'],
            'kill': [['del','code.language-del'], 'List of element CSS selectors to be removed, with contents'],
            'kill_empty': [['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre'], 'List of HTML tags to be removed if they are empty'],
        }
        super(KillTagsExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        processor = KillTagsPostprocessor(md)
        processor.config = self.getConfigs()
        md.postprocessors.add('kill_tags', processor, '_end')
        md.registerExtension(self)

def makeExtension(*args, **kwargs):
    return KillTagsExtension(*args, **kwargs)