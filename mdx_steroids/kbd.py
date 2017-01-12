#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mdx_steroids.kbd
================
Python Markdown extension.
Input:
    ||keyboard intput||
Output:
    <kbd>keyboard input</kbd>

Copyright (c) 2016 Adam Twardoch <adam+github@twardoch.com>
Based on original code
Copyright (c) 2014-2015 Isaac Muse <isaacmuse@gmail.com>
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import re

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree

__version__ = '0.4.1'

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


class MDXKbd(Pattern):
    def __init__(self, pattern, config):
        """
        Args:
            pattern ():
            config ():
        """
        super(MDXKbd, self).__init__(pattern)
        self.config = config

    def processLabel(self, label):
        """
        Args:
            label ():
        """
        if self.config['repl_mac']:
            ol = re.split(r"(?<!\\)(?:\\\\)*[\+\-]", label)
            nl = map(mreplace, ol)
            return u"\u2009".join(nl)

    def handleMatch(self, m):
        """
        Args:
            m ():
        """
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


class MDXKbdExtension(Extension):
    def __init__(self, *args, **kwargs):
        """
        Args:
            *args ():
            **kwargs ():
        """
        self.config = {
            'repl_mac'  : [True, "Replace macOS symbols"],
            'html_class': ['kbd', 'CSS hook. Leave blank for none.'],
        }

        super(MDXKbdExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.md = md

        # WIKILINK_RE = r'\|\|([\w0-9_ -]+)\]\]'
        kbdPattern = MDXKbd(RE_KBD, self.getConfigs())
        kbdPattern.md = md
        md.inlinePatterns.add(
            'kbd',
            kbdPattern,
            '<not_strong'
        )


def makeExtension(*args, **kwargs):
    return MDXKbdExtension(*args, **kwargs)
