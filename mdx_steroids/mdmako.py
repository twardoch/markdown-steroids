#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
## steroids.mako

The `steroids.mako` feeds Markdown through the Mako templating system.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids/

Copyright (c) 2017 Adam Twardoch <adam+github@twardoch.com>
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""

__version__ = '0.5.0'

import os.path
import io
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from mako.template import Template
from mako.lookup import TemplateLookup


class MakoPreprocessor(Preprocessor):
    def __init__(self, config, md):
        super(MakoPreprocessor, self).__init__(md)
        self.mako_args = config.get('mako_args')
        self.mako_include_base = config.get('mako_include_base')
        self.mako_include_encoding = config.get('mako_include_encoding')
        self.mako_include_auto = config.get('mako_include_auto')
        self.mako_python_block = config.get('mako_python_block')
        if type(self.mako_include_base) is list:
            self.mako_base_dirs = self.mako_include_base
        else:
            self.mako_base_dirs = [self.mako_include_base]

    def run(self, lines):
        if self.mako_python_block:
            path_python_block = None
            if os.path.exists(self.mako_python_block):
                path_python_block = self.mako_python_block
            elif os.path.exists(os.path.join(self.mako_include_base[0], self.mako_python_block)):
                path_python_block = os.path.join(self.mako_include_base[0], self.mako_python_block)
            if path_python_block:
                with io.open(path_python_block, 'r', encoding='utf8') as f:
                    python_block = f.read().splitlines()
                lines = [u'<%!'] + python_block + [u'%>'] + lines
        else:
            lines = [u''] + lines
        if self.mako_include_auto:
            line_include_auto = u'<%include file="{}"/>'.format(self.mako_include_auto)
            lines = [line_include_auto] + lines
        md = u"\n".join(lines)
        mako_lookup = TemplateLookup(directories=self.mako_base_dirs)
        mako_tpl = Template(md, input_encoding=self.mako_include_encoding, lookup=mako_lookup)
        mako_result = mako_tpl.render(**self.mako_args)
        lines = mako_result.splitlines()[1:]
        print(lines)
        return lines


class MarkdownMakoExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'mako_include_base'    : [u'.', 'Default location from which to evaluate ' \
                                           'relative paths for the include statement.'],
            'mako_include_encoding': ['utf-8', 'Encoding of the files used by the include ' \
                                               'statement.'],
            'mako_include_auto'    : [u'', 'Path to Mako file to be automatically' \
                                            'included at the beginning.'],
            'mako_python_block'    : [u'', 'Path to Python file to be automatically' \
                                            'included at the beginning as a module block.'],
            'mako_args'            : [{}, 'Dict of args passed to mako.Template().render()'],
        }
        super(MarkdownMakoExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.md = md
        md.registerExtension(self)
        config = self.getConfigs()
        md_mako = MakoPreprocessor(config, md)
        md.preprocessors.add('md_mako', md_mako, "_begin")
        print(md.preprocessors)

def makeExtension(*args, **kwargs):
    return MarkdownMakoExtension(kwargs)
