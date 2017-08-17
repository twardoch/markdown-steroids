#!/usr/bin/env python
# -*- coding: utf-8 -*-

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
from bs4 import BeautifulSoup

class KillTagsPostprocessor(Postprocessor):
    def kill_tags(self, html, find_tags):
        soup = BeautifulSoup(html, "lxml")
        for find_tag in find_tags:
            for t in soup.find_all(find_tag):
                t.extract()
        for t in soup.find_all('p'):
            if not len(t.contents):
                t.extract()
            elif not unicode(t.contents[0]).rstrip():
                t.extract()
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