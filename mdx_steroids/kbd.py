#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""KBD."""
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import Pattern
from pymdownx import util
import re

RE_KBD = r'\+{2}((?:[A-Za-z\d_]+\+)*?[A-Za-z\d_]+)\+{2}'
RE_NORMALIZE = re.compile(r'((?<=[a-z\d])[A-Z])')
KBD = '<kbd class="%(class)s key-%(key)s">%(name)s</kbd>'
WRAPPED_KBD = '<kbd class="%(class)s">' + KBD + '</kbd>'

KEY_MAP = {

    # Digits
    "0"                : "0",
    "1"                : "1",
    "2"                : "2",
    "3"                : "3",
    "4"                : "4",
    "5"                : "5",
    "6"                : "6",
    "7"                : "7",
    "8"                : "8",
    "9"                : "9",

    # Letters
    "a"                : "A",
    "b"                : "B",
    "c"                : "C",
    "d"                : "D",
    "e"                : "E",
    "f"                : "F",
    "g"                : "G",
    "h"                : "H",
    "i"                : "I",
    "j"                : "J",
    "k"                : "K",
    "l"                : "L",
    "m"                : "M",
    "n"                : "N",
    "o"                : "O",
    "p"                : "P",
    "q"                : "Q",
    "r"                : "R",
    "s"                : "S",
    "t"                : "T",
    "u"                : "U",
    "v"                : "V",
    "w"                : "W",
    "x"                : "X",
    "y"                : "Y",
    "z"                : "Z",

    # Space
    "space"            : "Space",

    # Punctuation
    "backslash"        : "\\",
    "bar"              : "|",
    "brace-left"       : "{",
    "brace-right"      : "}",
    "bracket-left"     : "[",
    "bracket-right"    : "]",
    "colon"            : ":",
    "comma"            : ",",
    "double-quote"     : "\"",
    "equal"            : "=",
    "exclam"           : "!",
    "grave"            : "`",
    "greater"          : ">",
    "less"             : "<",
    "less-greater"     : "<>",
    "minus"            : "-",
    "period"           : ".",
    "plus"             : "+",
    "question"         : "?",
    "section"          : "§",
    "semicolon"        : ";",
    "single-quote"     : "'",
    "slash"            : "/",
    "tilde"            : "~",
    "underscore"       : "_",

    # Navigation keys
    "arrow-up"         : "Up",
    "arrow-down"       : "Down",
    "arrow-left"       : "Left",
    "arrow-right"      : "Right",
    "page-up"          : "Page Up",
    "page-down"        : "Page Down",
    "home"             : "Home",
    "end"              : "End",
    "backspace"        : "Backspace",
    "delete"           : "Del",
    "insert"           : "Ins",
    "tab"              : "Tab",

    # Action keys
    "break"            : "Break",
    "caps-lock"        : "Caps Lock",
    "clear"            : "Clear",
    "escape"           : "Esc",
    "help"             : "Help",
    "print-screen"     : "Print Screen",
    "scroll-lock"      : "Scroll Lock",

    # Numeric keypad
    "num-0"            : "Num 0",
    "num-1"            : "Num 1",
    "num-2"            : "Num 2",
    "num-3"            : "Num 3",
    "num-4"            : "Num 4",
    "num-5"            : "Num 5",
    "num-6"            : "Num 6",
    "num-7"            : "Num 7",
    "num-8"            : "Num 8",
    "num-9"            : "Num 9",
    "num-asterisk"     : "Num *",
    "num-clear"        : "Num Clear",
    "num-delete"       : "Num Del",
    "num-equal"        : "Num =",
    "num-lock"         : "Num Lock",
    "num-minus"        : "Num -",
    "num-plus"         : "Num +",
    "num-separator"    : "Num ,",
    "num-slash"        : "Num /",
    "num-enter"        : "Num Enter",

    # Modifier keys
    "alt"              : "Alt",
    "command"          : "Cmd",
    "control"          : "Ctrl",
    "function"         : "Fn",
    "left-alt"         : "Left Alt",
    "left-control"     : "Left Ctrl",
    "left-shift"       : "Left Shift",
    "left-windows"     : "Left Win",
    "meta"             : "Meta",
    "right-alt"        : "Right Alt",
    "right-control"    : "Right Ctrl",
    "right-shift"      : "Right Shift",
    "right-windows"    : "Right Win",
    "shift"            : "Shift",
    "windows"          : "Win",

    # Function keys
    "f1"               : "F1",
    "f2"               : "F2",
    "f3"               : "F3",
    "f4"               : "F4",
    "f5"               : "F5",
    "f6"               : "F6",
    "f7"               : "F7",
    "f8"               : "F8",
    "f9"               : "F9",
    "f10"              : "F10",
    "f11"              : "F11",
    "f12"              : "F12",
    "f13"              : "F13",
    "f14"              : "F14",
    "f15"              : "F15",
    "f16"              : "F16",
    "f17"              : "F17",
    "f18"              : "F18",
    "f19"              : "F19",
    "f20"              : "F20",
    "f21"              : "F21",
    "f22"              : "F22",
    "f23"              : "F23",
    "f24"              : "F24",

    # Extra keys
    "abnt-c1"          : "Abnt C1",
    "abnt-c2"          : "Abnt C2",
    "accept"           : "Accept",
    "app1"             : "App 1",
    "app2"             : "App 2",
    "attn"             : "Attn",
    "auto"             : "Auto",
    "ax"               : "Ax",
    "backtab"          : "Back Tab",
    "browser-back"     : "Browser Back",
    "browser-favorites": "Browser Favorites",
    "browser-forward"  : "Browser Forward",
    "browser-home"     : "Browser Home",
    "browser-refresh"  : "Browser Refresh",
    "browser-search"   : "Browser Search",
    "browser-stop"     : "Browser Stop",
    "context-menu"     : "Context Menu",
    "copy"             : "Copy",
    "cr-sel"           : "Cr Sel",
    "cu-sel"           : "Cu Sel",
    "enlw"             : "Enlw",
    "er-eof"           : "Er Eof",
    "ex-sel"           : "Ex Sel",
    "execute"          : "Execute",
    "final"            : "Final",
    "finish"           : "Finish",
    "ico-00"           : "Ico 00",
    "ico-clear"        : "Ico Clr",
    "ico-help"         : "Ico Hlp",
    "jump"             : "Jump",
    "left-button"      : "Left Button",
    "mail"             : "Mail",
    "media"            : "Media",
    "media-next-track" : "Next Track",
    "media-pause"      : "Pause",
    "media-play"       : "Play",
    "media-play-pause" : "Play/Pause",
    "media-prev-track" : "Previous Track",
    "media-stop"       : "Stop",
    "middle-button"    : "Middle Button",
    "no-name"          : "No Name",
    "pa1"              : "Pa1",
    "pa2"              : "Pa2",
    "pa3"              : "Pa3",
    "packet"           : "Packet",
    "print"            : "Print",
    "process"          : "Process",
    "reset"            : "Reset",
    "right-button"     : "Right Button",
    "select"           : "Select",
    "sleep"            : "Sleep",
    "volume-down"      : "Volume Down",
    "volume-mute"      : "Mute",
    "volume-up"        : "Volume Up",
    "ws-ctrl"          : "Ws Ctrl",
    "x-button1"        : "X Button 1",
    "x-button2"        : "X Button 2",
    "zoom"             : "Zoom",

    # Japanese
    "jp-convert"       : "Convert",
    "jp-jisho"         : "Jisho",
    "jp-loya"          : "Loya",
    "jp-masshou"       : "Mashu",
    "jp-mode-change"   : "Mode Change",
    "jp-roya"          : "Roya",
    "jp-touroku"       : "Touroku",
    "jp-junja"         : "Junja",
    "jp-kana"          : "Kana",
    "jp-kanji"         : "Kanji",
    "jp-non-convert"   : "Non Convert",

}

KEY_ALIAS = {
    "add"              : "num-plus",
    "apps"             : "context-menu",
    "back"             : "backspace",
    "bksp"             : "backspace",
    "bktab"            : "backtab",
    "cancel"           : "break",
    "capital"          : "caps-lock",
    "close-brace"      : "brace-right",
    "close-bracket"    : "bracket-right",
    "clr"              : "clear",
    "cmd"              : "command",
    "convert"          : "jp-convert",
    "cplk"             : "caps-lock",
    "crsel"            : "cr-sel",
    "ctrl"             : "control",
    "cusel"            : "cu-sel",
    "dblquote"         : "double-quote",
    "decimal"          : "num-separator",
    "del"              : "delete",
    "divide"           : "num-slash",
    "dn"               : "arrow-down",
    "down"             : "arrow-down",
    "end"              : "end",
    "ereof"            : "er-eof",
    "esc"              : "escape",
    "exclamation"      : "exclam",
    "exsel"            : "ex-sel",
    "favorites"        : "browser-favorites",
    "fn"               : "function",
    "forward"          : "browser-forward",
    "grave-accent"     : "grave",
    "greater-than"     : "greater",
    "gt"               : "greater",
    "hyphen"           : "minus",
    "ico00"            : "ico-00",
    "icoclear"         : "ico-clear",
    "icohelp"          : "ico-help",
    "ins"              : "insert",
    "jisho"            : "jp-jisho",
    "junja"            : "jp-junja",
    "kana"             : "jp-kana",
    "kanji"            : "jp-kanji",
    "lalt"             : "left-alt",
    "launch-app1"      : "app1",
    "launch-app2"      : "app2",
    "launch-mail"      : "mail",
    "launch-media"     : "media",
    "lbutton"          : "left-button",
    "lcontrol"         : "left-control",
    "lctrl"            : "left-control",
    "left"             : "arrow-left",
    "left-ctrl"        : "left-control",
    "left-menu"        : "left-alt",
    "left-win"         : "left-windows",
    "less-greater-than": "less-greater",
    "less-than"        : "less",
    "lmenu"            : "left-alt",
    "loya"             : "jp-loya",
    "lshift"           : "left-shift",
    "lt"               : "less",
    "lt-gt"            : "less-greater",
    "lwin"             : "left-windows",
    "masshou"          : "jp-masshou",
    "mbutton"          : "middle-button",
    "menu"             : "alt",
    "mode-change"      : "jp-mode-change",
    "modechange"       : "jp-mode-change",
    "multiply"         : "num-asterisk",
    "mute"             : "volume-mute",
    "next"             : "page-down",
    "next-track"       : "media-next-track",
    "non-convert"      : "jp-non-convert",
    "noname"           : "no-name",
    "num-del"          : "num-delete",
    "num-equalsign"    : "num-equal",
    "num0"             : "num-0",
    "num1"             : "num-1",
    "num2"             : "num-2",
    "num3"             : "num-3",
    "num4"             : "num-4",
    "num5"             : "num-5",
    "num6"             : "num-6",
    "num7"             : "num-7",
    "num8"             : "num-8",
    "num9"             : "num-9",
    "numlk"            : "num-lock",
    "numlock"          : "num-lock",
    "open-brace"       : "brace-left",
    "open-bracket"     : "bracket-left",
    "page-dn"          : "page-down",
    "page-up"          : "page-up",
    "pause"            : "media-pause",
    "pgdn"             : "page-down",
    "pgup"             : "page-up",
    "play"             : "media-play",
    "play-pause"       : "media-play-pause",
    "prev-track"       : "media-prev-track",
    "printscreen"      : "print-screen",
    "prior"            : "page-up",
    "prtsc"            : "print-screen",
    "question-mark"    : "question",
    "ralt"             : "right-alt",
    "rbutton"          : "right-button",
    "rcontrol"         : "right-control",
    "rctrl"            : "right-control",
    "refresh"          : "browser-refresh",
    "return"           : "num-enter",
    "right"            : "arrow-right",
    "right-ctrl"       : "right-control",
    "right-menu"       : "right-alt",
    "right-win"        : "right-windows",
    "rmenu"            : "right-alt",
    "roya"             : "jp-roya",
    "rshift"           : "right-shift",
    "rwin"             : "right-windows",
    "scroll"           : "scroll-lock",
    "search"           : "browser-search",
    "separator"        : "num-separator",
    "spc"              : "space",
    "stop"             : "media-stop",
    "subtract"         : "num-minus",
    "tabulator"        : "tab",
    "touroku"          : "jp-touroku",
    "up"               : "arrow-up",
    "vol-down"         : "volume-down",
    "vol-mute"         : "volume-mute",
    "vol-up"           : "volume-up",
    "win"              : "windows",
    "wsctrl"           : "ws-ctrl",
    "xbutton1"         : "x-button1",
    "xbutton2"         : "x-button2",
    "zoom"             : "zoom",
}


class KbdPattern(Pattern):
    """Return kbd tag."""

    def __init__(self, pattern, config, md):
        """Initialize."""

        self.markdown = md
        self.wrap_kbd = config['wrap_kbd']
        self.separator = config['separator']
        self.classes = config['classes']
        Pattern.__init__(self, pattern)

    def process_key(self, key):
        """Process key."""

        norm_key = RE_NORMALIZE.sub(r'-\1', key).replace('_', '-').lower()
        canonical_key = KEY_ALIAS.get(norm_key, norm_key)
        name = KEY_MAP.get(canonical_key, None)
        return (canonical_key, name) if name else None

    def handleMatch(self, m):
        """Handle kbd pattern matches."""

        keys = [self.process_key(key) for key in m.group(2).split('+')]

        if None in keys:
            return

        html = []
        for key_class, key_name in keys:
            html.append(
                (WRAPPED_KBD if self.wrap_kbd else KBD) % {
                    'class': self.classes,
                    'key': key_class,
                    'name': key_name
                }
            )

        return self.markdown.htmlStash.store(self.separator.join(html), safe=True)


class KbdExtension(Extension):
    """Add KBD extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'separator': ['+', "Provide a separator - Default: \"+\""],
            'wrap_kbd': [False, "Wrap kbds in another kbd according to HTML5 spec - Default: False"],
            'classes': ['kbd', "Provide classes for the kbd elements - Default: kbd"]
        }
        super(KbdExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add support for kbd."""

        util.escape_chars(md, ['+'])

        md.inlinePatterns.add(
            "kbd",
            KbdPattern(RE_KBD, self.getConfigs(), md),
            "<not_strong"
        )


###################
# Make Available
###################
def makeExtension(*args, **kwargs):
    """Return extension."""

    return KbdExtension(*args, **kwargs)
