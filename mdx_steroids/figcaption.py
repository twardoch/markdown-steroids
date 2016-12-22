#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mdx_steroids.figcaption
=======================
Python Markdown extension.
Input:
    ![](https://avatars2.githubusercontent.com/u/519108)
    :   Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Praesent at consequat magna, faucibus ornare eros. Nam et
        mattis urna. Cras sodales, massa id gravida
Output:
    <figure>
        <img alt="" src="https://avatars2.githubusercontent.com/u/519108" />
        <figcaption>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Praesent at consequat magna, faucibus ornare eros. Nam et
            mattis urna. Cras sodales, massa id gravida</p>
        </figcaption>
    </figure>

Copyright (c) 2016 Adam Twardoch <adam+github@twardoch.com>
Based on original code
Copyright (c) 2008 [Waylan Limberg](http://achinghead.com)
Copyright (c) 2008-2014 The Python Markdown Project
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""

from __future__ import unicode_literals

import re

from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import IMAGE_LINK_RE, IMAGE_REFERENCE_RE
from markdown.util import etree

__version__ = '0.4.1'

FIGURES = [IMAGE_LINK_RE, IMAGE_REFERENCE_RE]


class MDXFigcaptionProcessor(BlockProcessor):
    RE = re.compile(r'(^|\n)[ ]{0,3}:[ ]{1,3}(?P<caption>.*?)(\n|$)')
    FIGURES_RE = re.compile('|'.join(f for f in FIGURES))
    NO_INDENT_RE = re.compile(r'^[ ]{0,3}[^ :]')

    def check(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        # pop the entire block as a single string
        raw_block = blocks.pop(0)

        # Get list of figure elements before the colon (:)
        m = self.RE.search(raw_block)

        # Get elements
        elements = raw_block[:m.start()]
        check_elements = self.FIGURES_RE.search(elements)

        if not check_elements:
            # This is not a figure item.
            blocks.insert(0, raw_block)
            return False

        # Get caption
        block = raw_block[m.end():]
        no_indent = self.NO_INDENT_RE.match(block)

        if no_indent:
            caption, theRest = (block, None)
        else:
            caption, theRest = self.detab(block)
        if caption:
            caption = '%s\n%s' % (m.group('caption'), caption)
        else:
            caption = m.group('caption')

        # Create figure
        figure = etree.SubElement(parent, 'figure')
        figure.text = elements

        # Add definition
        self.parser.state.set('fig')
        figcaption = etree.SubElement(figure, 'figcaption')
        self.parser.parseBlocks(figcaption, [caption])
        self.parser.state.reset()

        if theRest:
            blocks.insert(0, theRest)


class MDXFigcaptionExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add(
            'figcaption',
            MDXFigcaptionProcessor(md.parser),
            '<ulist'
        )


def makeExtension(configs={}):
    return MDXFigcaptionExtension(configs=configs)
