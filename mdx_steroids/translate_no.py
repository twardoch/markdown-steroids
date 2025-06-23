#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# mdx_steroids.translate_no

The `mdx_steroids.translate_no` extension for Python Markdown adds the `translate="no"` attribute to specified HTML selectors.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids

### Options

* The `add` option allows to specify a list of CSS selectors or (when using the "!" prefix), XPath selectors. Elements matching to these selectors will get the `translate="no"` attribute.

* The `normalize` option will pass the final HTML through BeautifulSoup if true.

```yaml
  mdx_steroids.translate_no:
    normalize: false  # Do not use BeautifulSoup for post-processing
    add:             # List of CSS selectors or (with "!" prefix) XPath selectors
      - kbd
      - code
      - pre
```

Copyright (c) 2017 Adam Twardoch <adam+github@twardoch.com>
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from future.utils import bytes_to_native_str as n
import six

__version__ = "0.5.4"

from markdown import Extension
from markdown.postprocessors import Postprocessor
import lxml.html
import lxml.html.soupparser
import lxml.cssselect as cssselect
from bs4 import BeautifulSoup
import lxml.etree as et


class NoTranslatePostprocessor(Postprocessor):
    def add_attribute_to_element(self, element):
        element.attrib["translate"] = "no"
        element.classes.add("notranslate")

    def normalize_html(self):
        out = BeautifulSoup(self.html, "html5lib")
        self.html = six.text_type(out)

    def parse_selector(self, selector):
        cx = cssselect.LxmlHTMLTranslator()
        if selector[:1] == "!":  # direct XPath selector
            xpath_sel = selector[1:]
        else:
            xpath_sel = cx.css_to_xpath(selector)  # CSS selector
        return xpath_sel

    def process_selectors(self):
        tree = lxml.html.fromstring(self.html)
        for process_selector in self.selectors:
            for el in tree.xpath(process_selector):
                self.add_attribute_to_element(el)
        out = n(et.tostring(tree, pretty_print=False))
        self.html = six.text_type(out)

    def run(self, html):
        self.html = html
        self.selectors = [
            self.parse_selector(sel) for sel in self.config.get("add", [])
        ]
        if self.config.get("normalize", False):
            self.normalize_html()
        self.process_selectors()
        if self.config.get("normalize", False):
            self.normalize_html()
        return six.text_type(self.html)


class NoTranslateExtensions(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            "normalize": [False, "Normalize HTML"],
            "add": [
                ["code", "mark", "pre", "kbd"],
                'List of element CSS selectors where translate="no" is added',
            ],
        }
        super(NoTranslateExtensions, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        processor = NoTranslatePostprocessor(md)
        processor.config = self.getConfigs()
        md.postprocessors.add("translate_no", processor, "_end")
        # md.registerExtension(self)


def makeExtension(*args, **kwargs):
    return NoTranslateExtensions(*args, **kwargs)
