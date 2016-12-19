"""
Mark.

mdx_steroids.mdx_kbd
Really simple plugin to add support for
<kbd>test</kbd> tags as ||test||

MIT license.

Copyright (c) 2014 - 2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import HtmlPattern
from markdown.odict import OrderedDict
from markdown.inlinepatterns import Pattern

RE_SMART_CONTENT = r'((?:[^\|]|\|(?=[^\W_]|\||\s)|(?<=\s)\|+?(?=\s))+?\|*?)'
RE_DUMB_CONTENT = r'((?:[^\|]|(?<!\|)\|(?=[^\W_]|\|))+?)'
RE_SMART_KBD_BASE = r'(\|{2})(?![\s\|])%s(?<!\s)\|{2}' % RE_SMART_CONTENT
RE_SMART_KBD = r'(?:(?<=_)|(?<![\w\|]))%s(?:(?=_)|(?![\w\|]))' % RE_SMART_KBD_BASE
RE_KBD_BASE = r'(\|{2})(?!\s)%s(?<!\s)\|{2}' % RE_DUMB_CONTENT
RE_KBD = RE_KBD_BASE

class Kbd(Pattern):
    def handleMatch(self, m, repl_mac):
        el = etree.Element('kbd')
        el.text = m.group('text')
        return el

class KbdExtension(Extension):
    """Add the kbd extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'repl_mac': [True, "Replace macOS symbols"], 
        }

        super(KbdExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add support for <kbd>test</kbd> tags as ||test||."""

        if "|" not in md.ESCAPED_CHARS:
            md.ESCAPED_CHARS.append('|')
        config = self.getConfigs()

        if config.get('repl_mac', True):
            md.inlinePatterns.add("kbd", Kbd(RE_SMART_KBD, True), "<not_strong")
        else:
            md.inlinePatterns.add("kbd", Kbd(RE_SMART_KBD, False), "<not_strong")


def makeExtension(*args, **kwargs):
    """Return extension."""

    return KbdExtension(*args, **kwargs)
