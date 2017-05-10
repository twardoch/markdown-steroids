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

__version__ = '0.0.1'

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from mako.template import Template
from mako.lookup import TemplateLookup

class MarkdownMako(Extension):
    def __init__(self, configs={}):
        init_config = {
            'base_path': ['.', 'Default location from which to evaluate ' \
                               'relative paths for the include statement.'],
            'encoding' : ['utf-8', 'Encoding of the files used by the include ' \
                                   'statement.']
        }
        self.config = dict(init_config, **configs)
        #for key, value in configs.items():
        #    self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add(
            'md_mako', MakoPreprocessor(md, self.getConfigs()), '_begin'
        )

class MakoPreprocessor(Preprocessor):

    def __init__(self, md, config):
        super(MakoPreprocessor, self).__init__(md)
        self.config = config
        self.base_path = config['base_path']
        self.encoding = config['encoding']

    def run(self, lines):
        md = u"\n".join(lines)
        mako_lookup = TemplateLookup(directories=[self.base_path])
        mako_tpl = Template(md, input_encoding=self.encoding, lookup=mako_lookup)
        mako_result = mako_tpl.render(**self.config)
        lines = mako_result.splitlines()
        return lines

def makeExtension(*args, **kwargs):
    return MarkdownMako(kwargs)