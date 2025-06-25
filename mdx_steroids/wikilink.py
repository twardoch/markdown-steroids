#!/usr/bin/env python
"""
# mdx_steroids.wikilink

The `mdx_steroids.wikilink` extension parses wikilinks in the style of
the [Gollum](https://github.com/gollum/gollum) wiki and
the [Github Wiki system](https://help.github.com/articles/about-github-wikis/).
It will convert links such as `[[Page name]]` to `[Page name](/Page-name/)`.
You can specify the start, end and separator strings.

This is now rewritten as a preprocessor, so [[Wiki Link]] turns into
[Wiki Link](/Wiki-Link/) and can be processed further.

`html_class` is currently not used.

### Installation


pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git


### Docs

* https://github.com/twardoch/markdown-steroids

### Options

  steroids.wikilink:
    base_url       : '/'                  # String to append to beginning or URL.
    end_url        : '/'                  # String to append to end of URL.
    html_class     : 'wikilink'           # CSS hook. Leave blank for none.
    space_sep      : '-'                  # String that replaces the space, "-" by default.


### Example

#### Input Markdown

This is a [[Wiki Link]] of some sorts.


This is a [[Wiki Link]] of some sorts.


#### Output HTML

<p>This is a <a class="wikilink" href="/Wiki-Link/">Wiki Link</a> of some sorts.</p>


<p>This is a <a class="wikilink" href="/Wiki-Link/">Wiki Link</a> of some sorts.</p>


Copyright (c) 2018 Adam Twardoch <adam+github@twardoch.com>
Based on original code
Copyright (c) 2008 [Waylan Limberg](http://achinghead.com)
Copyright (c) 2008-2014 The Python Markdown Project
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""

from __future__ import annotations

import re
from re import Pattern

from markdown import Extension
from markdown.preprocessors import Preprocessor

try:
    from pymdownx.slugs import uslugify_cased_encoded as slugify
except ImportError:
    from loguru import logger

    logger.warning("Install pymdownx: pip install --user pymdown-extensions")

    def slugify(text: str, separator: str = "-") -> str:
        return text.lower().replace(" ", separator)


__version__ = "0.5.0"

WIKI_LINK_RE: Pattern[str] = re.compile(r"\[\[([\w0-9_ -]+)\]\]")


class WikiLinksProcessor(Preprocessor):
    def __init__(self, md: markdown.Markdown, config: dict[str, list[str]]) -> None:
        super().__init__(md)
        self.config = config

    def build_url(self, match: re.Match[str]) -> str:
        base_url = self.config.get("base_url", [""])[0]
        end_url = self.config.get("end_url", [""])[0]
        space_sep = self.config.get("space_sep", ["-"])[0]
        return f"[{match.group(1)}]({base_url}{slugify(match.group(1), space_sep)}{end_url})"

    def run(self, lines: list[str]) -> list[str]:
        return [WIKI_LINK_RE.sub(self.build_url, line) for line in lines]


class WikiLinkExtension(Extension):
    def __init__(self, *args, **kwargs) -> None:
        self.config = {
            "base_url": ["/", "String to append to beginning or URL."],
            "end_url": ["/", "String to append to end of URL."],
            "html_class": ["wikilink", "CSS hook. Leave blank for none."],
            "space_sep": ["-", 'String that replaces the space, "-" by default.'],
        }
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md: markdown.Markdown) -> None:
        md.registerExtension(self)
        md.preprocessors.register(WikiLinksProcessor(md, self.config), "wikilink", 4)


def makeExtension(*args, **kwargs) -> WikiLinkExtension:
    return WikiLinkExtension(*args, **kwargs)
