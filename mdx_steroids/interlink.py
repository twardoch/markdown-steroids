#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# mdx_steroids.interlink

The `mdx_steroids.interlink` extension preprocesses internal links
in the style of [text](some-link#anchor). You can insert a `base_url` 
or `end_url` strings if the link does not contain a protocol (`://`) 
or a period (`.`). 

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids

### Options

```yaml
  steroids.InterLink:
    base_url       : '/'                  # String to append to beginning or URL.
    end_url        : '/'                  # String to append to end of URL before anchor.
```

### Example

#### Input Markdown

This is a [[Wiki Link]] of some sorts.

```markdown
This is a [[Wiki Link]] of some sorts. 
```

#### Output HTML

<p>This is a <a class="InterLink" href="/Wiki-Link/">Wiki Link</a> of some sorts.</p>

```html
<p>This is a <a class="InterLink" href="/Wiki-Link/">Wiki Link</a> of some sorts.</p>
```

Copyright (c) 2018 Adam Twardoch <adam+github@twardoch.com>
Based on original code
Copyright (c) 2008 [Waylan Limberg](http://achinghead.com)
Copyright (c) 2008-2014 The Python Markdown Project
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from __future__ import print_function
import re

from markdown import Extension
from markdown.preprocessors import Preprocessor
try: 
    from pymdownx.slugs import uslugify_cased_encoded as slugify
except ImportError: 
    print("Install pymdownx: pip install --user pymdown-extensions")

__version__ = '0.5.0'

reInterLink = re.compile(r'(?<!!)\[([^\]]+)\]\((\S+(?=\)))\)')

class MDXInterLinksProcessor(Preprocessor):
    def __init__(self, md, config):
        super(MDXInterLinksProcessor, self).__init__(md)
        self.config = config

    def build_url(self, matcho):
        text = matcho.group(1)
        link = matcho.group(2)
        base = self.config.get('base_url', [''])[0]
        end = self.config.get('end_url', [''])[0]
        if ('://' not in link) and ('.' not in link): 
            alink = link.split('#')
            if alink[0]: 
                linklist = [base] + alink[:1] + [end]
                if len(alink) > 1: 
                    linklist += ['#'] + alink[1:]
                link = "".join(linklist)
        return '[%s](%s)' % (text, link)

    def run(self, lines):
        return [reInterLink.sub(self.build_url, line) for line in lines]

class MDXInterLinkExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'base_url'  : ['', 'String to append to beginning or URL.'],
            'end_url'   : ['', 'String to append to end of URL.'],
        }

        super(MDXInterLinkExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.md = md
        md.registerExtension(self)
        md.preprocessors.register(
            MDXInterLinksProcessor(md, self.config), "interlink", 6
        )

def makeExtension(*args, **kwargs):
    return MDXInterLinkExtension(*args, **kwargs)
