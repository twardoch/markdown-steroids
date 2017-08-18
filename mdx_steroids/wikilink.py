#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# mdx_steroids.wikilink

The `mdx_steroids.wikilink` extension parses wikilinks in the style of the  [Gollum](https://github.com/gollum/gollum) wiki and the [Github Wiki system](https://help.github.com/articles/about-github-wikis/). It will convert links such as `[[Page name]]` to `[Page name](/Page-name/)`. You can specify the start, end and separator strings.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids

### Options

```yaml
  steroids.wikilink:
    base_url       : '/'                  # String to append to beginning or URL.
    end_url        : '/'                  # String to append to end of URL.
    html_class     : 'wikilink'           # CSS hook. Leave blank for none.
    space_sep      : '-'                  # String that replaces the space, "-" by default.
    build_url      : build_url            # Alternative callable formats URL from label.
```

### Example

#### Input Markdown

This is a [[Wiki Link]] of some sorts.

```markdown
This is a [[Wiki Link]] of some sorts. 
```

#### Output HTML

<p>This is a <a class="wikilink" href="/Wiki-Link/">Wiki Link</a> of some sorts.</p>

```html
<p>This is a <a class="wikilink" href="/Wiki-Link/">Wiki Link</a> of some sorts.</p>
```

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

__version__ = '0.4.4'


def build_url(label, base, end, space_sep='-'):
    """Build a url from the label, a base, an end, 
    and optionally, a separator.

    Args:
        label ():
        base ():
        end ():
        space_sep (): 

    Returns:

    """
    clean_label = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', space_sep, label)
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
            base_url, end_url, html_class, space_sep = self._getMeta()
            label = m.group(2).strip()
            url = self.config['build_url'](label, base_url, end_url, space_sep)
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
        space_sep = self.config['space_sep']
        if hasattr(self.md, 'Meta'):
            if 'wiki_base_url' in self.md.Meta:
                base_url = self.md.Meta['wiki_base_url'][0]
            if 'wiki_end_url' in self.md.Meta:
                end_url = self.md.Meta['wiki_end_url'][0]
            if 'wiki_html_class' in self.md.Meta:
                html_class = self.md.Meta['wiki_html_class'][0]
            if 'wiki_space_sep' in self.md.Meta:
                space_sep = self.md.Meta['wiki_space_sep'][0]
        return base_url, end_url, html_class, space_sep


class MDXWikiLinkExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'base_url'  : ['/', 'String to append to beginning or URL.'],
            'end_url'   : ['/', 'String to append to end of URL.'],
            'html_class': ['wikilink', 'CSS hook. Leave blank for none.'],
            'space_sep': ['-', 'String that replaces the space, "-" by default.'],
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
