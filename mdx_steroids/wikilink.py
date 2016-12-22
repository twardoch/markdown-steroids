#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mdx_steroids.wikilink
=====================
Python Markdown extension.
Input:
    [[Page Title]]
Equivalent to:
    [Page Title](Page-Title.md)

Copyright (c) 2016 Adam Twardoch <adam+github@twardoch.com>
Based on original code
Copyright (c) 2008 [Waylan Limberg](http://achinghead.com)
Copyright (c) 2008-2014 The Python Markdown Project
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import re

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree

__version__ = '0.4.1'


def build_url(label, base, end):
    """Build a url from the label, a base, and an end.

    Args:
        label ():
        base ():
        end ():

    Returns:

    """
    clean_label = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '-', label)
    return '%s%s%s' % (base, clean_label, end)


class MDXWikiLinks(Pattern):
    def __init__(self, pattern, config):
        """
        Args:
            pattern ():
            config ():
        """
        super(MDXWikiLinks, self).__init__(pattern)
        self.config = config

    def handleMatch(self, m):
        """
        Args:
            m ():
        """
        if m.group(2).strip():
            base_url, end_url, html_class = self._getMeta()
            label = m.group(2).strip()
            url = self.config['build_url'](label, base_url, end_url)
            a = etree.Element('a')
            a.text = label
            a.set('href', url)
            if html_class:
                a.set('class', html_class)
        else:
            a = ''
        return a

    def _getMeta(self):
        """ Return meta data or config data. """
        base_url = self.config['base_url']
        end_url = self.config['end_url']
        html_class = self.config['html_class']
        if hasattr(self.md, 'Meta'):
            if 'wiki_base_url' in self.md.Meta:
                base_url = self.md.Meta['wiki_base_url'][0]
            if 'wiki_end_url' in self.md.Meta:
                end_url = self.md.Meta['wiki_end_url'][0]
            if 'wiki_html_class' in self.md.Meta:
                html_class = self.md.Meta['wiki_html_class'][0]
        return base_url, end_url, html_class


class MDXWikiLinkExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'base_url'  : ['/', 'String to append to beginning or URL.'],
            'end_url'   : ['/', 'String to append to end of URL.'],
            'html_class': ['wikilink', 'CSS hook. Leave blank for none.'],
            'build_url' : [build_url, 'Callable formats URL from label.'],
        }

        super(MDXWikiLinkExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.md = md

        # append to end of inline patterns
        WIKILINK_RE = r'\[\[([\w0-9_ -]+)\]\]'
        wikilinkPattern = MDXWikiLinks(WIKILINK_RE, self.getConfigs())
        wikilinkPattern.md = md
        md.inlinePatterns.add(
            'wikilink',
            wikilinkPattern,
            '<not_strong'
        )


def makeExtension(*args, **kwargs):
    return MDXWikiLinkExtension(*args, **kwargs)
