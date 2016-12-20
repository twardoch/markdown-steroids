#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from __future__ import absolute_import
from __future__ import unicode_literals
from markdown.extensions import Extension  ### Changed to absolute
from markdown.inlinepatterns import Pattern  ### Changed to absolute
from markdown.util import etree  ### Changed to absolute
import re

RE_CONTENT = r"((?:[^\|]|(?<!\|)\|(?=[^\W_]|\|))+?)"
RE_KBD = r"(\|{2})(?!\s)%s(?<!\s)\|{2}" % RE_CONTENT

def mreplacer(*key_values):
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return lambda string: pattern.sub(replacement_function, string)

def mreplace(string, *key_values):
    key_values = (
        (u'Shift', u'\u21e7'),  # ⇧ UPWARDS WHITE ARROW
        (u'Cmd', u'\u2318'),  # ⌘ PLACE OF INTEREST SIGN
        (u'Command', u'\u2318'),  # ⌘ PLACE OF INTEREST SIGN
        (u'Option', u'\u2325'),  # ⌥ OPTION KEY
        (u'Opt', u'\u2325'),  # ⌥ OPTION KEY
        (u'Ctrl', u'\u2303'),  # ⌃ UP ARROWHEAD
        (u'Control', u'\u2303'),  # ⌃ UP ARROWHEAD
        (u'CapsLock', u'\u21ea'),  # ⇪ UPWARDS WHITE ARROW FROM BAR
        (u'Clear', u'\u2327'),  # ⌧ X IN A RECTANGLE BOX
        (u'Backspace', u'\u232b'),  # ⌫ ERASE TO THE LEFT
        (u'Delete', u'\u2326'),  # ⌦ ERASE TO THE RIGHT
        (u'Del', u'\u2326'),  # ⌦ ERASE TO THE RIGHT
        (u'Tab', u'\u21e5'),  # ⇥ RIGHTWARDS ARROW TO BAR
        (u'Return', u'\u21a9'),  # ↩ LEFTWARDS ARROW WITH HOOK
        (u'Enter', u'\u21a9'),  # ↩ LEFTWARDS ARROW WITH HOOK
        (u'Left', u'\u2190'),  # ← LEFTWARDS ARROW
        (u'Right', u'\u2192'),  # → RIGHTWARDS ARROW
        (u'Up', u'\u2191'),  # ↑ UPWARDS ARROW
        (u'Down', u'\u2193'),  # ↓ DOWNWARDS ARROW
        (u'PgUp', u'\u21de'),  # ⇞ UPWARDS ARROW WITH DOUBLE STROKE
        (u'PgDn', u'\u21df'),  # ⇟ DOWNWARDS ARROW WITH DOUBLE STROKE
        (u'Home', u'\u2196'),  # ↖ NORTH WEST ARROW
        (u'End', u'\u2198'),  # ↘ SOUTH EAST ARROW
        (u'Esc', u'\u238b'),  # ⎋ BROKEN CIRCLE WITH NORTHWEST ARROW
        (u'Escape', u'\u238b'),  # ⎋ BROKEN CIRCLE WITH NORTHWEST ARROW
        (u'Eject', u'\u23cf'),  # ⏏ EJECT SYMBOL
        (u'Space', u'\u2423'),  # ␣ OPEN BOX
    )
    return mreplacer(*key_values)(string)

class Kbd(Pattern):
    def __init__(self, pattern, config):
        super(Kbd, self).__init__(pattern)
        self.config = config

    def processLabel(self, label):
        if self.config['repl_mac']:
            ol = re.split(r"(?<!\\)(?:\\\\)*[\+\-]", label)
            nl = map(mreplace, ol)
            print(ol, nl)
            return u"\u2009".join(nl)

    def handleMatch(self, m):
        if m.group(3).strip():
            html_class = self.config['html_class']
            label = m.group(3).strip()
            label = self.processLabel(label)
            kbd = etree.Element('kbd')
            kbd.text = label
            if html_class:
                kbd.set('class', html_class)
        else:
            kbd = label
        return kbd

class KbdExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'repl_mac':   [True, "Replace macOS symbols"],
            'html_class': ['kbd', 'CSS hook. Leave blank for none.'],
        }

        super(KbdExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.md = md

        #WIKILINK_RE = r'\|\|([\w0-9_ -]+)\]\]'
        kbdPattern = Kbd(RE_KBD, self.getConfigs())
        kbdPattern.md = md
        md.inlinePatterns.add('kbd', kbdPattern, "<not_strong")

def makeExtension(*args, **kwargs):
    return KbdExtension(*args, **kwargs)
