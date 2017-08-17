#!/usr/bin/env python
# -*- coding: utf-8 -*-

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
from bs4 import BeautifulSoup

class KillTagsPostprocessor(Postprocessor):
    def kill_tags(self, html, tags):
        soup = BeautifulSoup(html, "lxml")
        for tag in tags:
            if soup.find_all(tag):
                for t in soup.find_all(tag):
                    t.replace_with("")
        return unicode(soup)

    def run(self, html):
        tags = self.config.get('tags', [])
        return self.kill_tags(html, tags)

class KillTagsExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'tags': [[], 'HTML element tags to be removed (with contents)'],
        }
        super(KillTagsExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        processor = KillTagsPostprocessor(md)
        processor.config = self.getConfigs()
        md.postprocessors.add('kill_tags', processor, '_end')
        md.registerExtension(self)

def makeExtension(*args, **kwargs):
    return KillTagsExtension(*args, **kwargs)