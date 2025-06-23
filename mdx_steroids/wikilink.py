#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# mdx_steroids.wikilink

The `mdx_steroids.wikilink` extension parses wikilinks in the style of
the  [Gollum](https://github.com/gollum/gollum) wiki and
the [Github Wiki system](https://help.github.com/articles/about-github-wikis/).
It will convert links such as `[[Page name]]` to `[Page name](/Page-name/)`.
You can specify the start, end and separator strings.

This is now rewritten as a preprocessor, so [[Wiki Link]] turns into
[Wiki Link](/Wiki-Link/) and can be processed further.

`html_class` is currently not used.

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

__version__ = "0.5.0"

reWikiLink = re.compile(r"\[\[([\w0-9_ -]+)\]\]")


class MDXWikiLinksProcessor(Preprocessor):
    def __init__(self, md, config):
        super(MDXWikiLinksProcessor, self).__init__(md)
        self.config = config

    def build_url(self, matcho):
        return "[%s](%s%s%s)" % (
            matcho.group(1),
            self.config.get("base_url", [""])[0],
            slugify(matcho.group(1), self.config.get("space_sep", ["-"])[0]),
            self.config.get("end_url", [""])[0],
        )

    def run(self, lines):
        return [reWikiLink.sub(self.build_url, line) for line in lines]


class MDXWikiLinkExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            "base_url": ["/", "String to append to beginning or URL."],
            "end_url": ["/", "String to append to end of URL."],
            "html_class": ["wikilink", "CSS hook. Leave blank for none."],
            "space_sep": ["-", 'String that replaces the space, "-" by default.'],
        }

        super(MDXWikiLinkExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.md = md
        md.registerExtension(self)
        md.preprocessors.register(MDXWikiLinksProcessor(md, self.config), "wikilink", 4)


def makeExtension(*args, **kwargs):
    return MDXWikiLinkExtension(*args, **kwargs)
