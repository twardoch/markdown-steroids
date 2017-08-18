#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
## steroids.kill_tags

The `steroids.kill_tags` removes requested HTML elements from final HTML output.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids

### Options

* The `kill` option allows to specify a list of CSS selectors or (when using the "!" prefix), XPath selectors.
Elements matching to these selectors will be completely removed from the final HTML.

* The `kill_known` option allows to remove (if true) or keep (if false) certain hardcoded selectors.

* The `kill_empty` option allows to specify a list of simple element tags which will be removed if they’re empty.

* The `normalize` option will pass the final HTML through BeautifulSoup if true.

```yaml
  steroids.kill_tags:
    normalize: false  # Do not use BeautifulSoup for post-processing
    kill:             # List of CSS selectors or (with "!" prefix) XPath selectors to delete
      - "!//pre[@class and contains(concat(' ', normalize-space(@class), ' '), ' hilite ') and code[@class and
      contains(concat(' ', normalize-space(@class), ' '), ' language-del ')]]"
      - del
    kill_known: false # Do not remove some hardcoded "known" selectors
    kill_empty:       # List of HTML tags (simple) to be removed if they’re empty
      - p
      - div
```

Copyright (c) 2017 Adam Twardoch <adam+github@twardoch.com>
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""

__version__ = '0.5.0'

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
import lxml.html
import lxml.html.soupparser
import lxml.cssselect
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

    def known_selectors(self):
        return [
            "//pre[@class and contains(concat(' ', normalize-space(@class), ' '), ' hilite ') and code[@class and "
             "contains(concat(' ', normalize-space(@class), ' '), ' language-del ')]]",
            "descendant-or-self::del",
        ]

    def parse_selector(self, selector):
        cx = lxml.cssselect.LxmlHTMLTranslator()
        if selector[:1] == '!':  # direct XPath selector
            xpath_sel = selector[1:]
        else:
            xpath_sel = cx.css_to_xpath(selector)  # CSS selector
        return xpath_sel

    def kill_selectors(self):
        tree = lxml.html.fromstring(self.html)
        for kill_selector in self.kill:
            for el in tree.xpath(kill_selector):
                self.remove_keeping_tail(el)
        for kill_empty_selector in self.kill_empty:
            for el in tree.xpath(
                    '//{}['
                    'not(descendant-or-self::*/text()[normalize-space()])'
                    ' and not(descendant-or-self::*/attribute::*)'
                    ']'.format(kill_empty_selector)):
                self.remove_keeping_tail(el)
        self.html = et.tostring(tree, pretty_print=False)

    def run(self, html):
        self.html = html
        self.kill = [self.parse_selector(sel) for sel in self.config.get('kill', [])]
        if self.config.get('kill_known', False):
            self.kill += self.known_selectors()
        self.kill_empty = self.config.get('kill_empty', [])
        if self.config.get('normalize', False):
            self.normalize_html()
        self.kill_selectors()
        if self.config.get('normalize', False):
            self.normalize_html()
        return self.html


class KillTagsExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'normalize' : [False, 'Normalize HTML before processing'],
            'kill'      : [[], 'List of element CSS selectors to be removed, with contents'],
            'kill_known': [False, 'Also remove some "known" selectors, with contents'],
            'kill_empty': [
                ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre'],
                'List of HTML tags to be removed if they are empty'],
        }
        super(KillTagsExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        processor = KillTagsPostprocessor(md)
        processor.config = self.getConfigs()
        md.postprocessors.add('kill_tags', processor, '_end')
        # md.registerExtension(self)


def makeExtension(*args, **kwargs):
    return KillTagsExtension(*args, **kwargs)
