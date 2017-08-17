#!/usr/bin/env python
# -*- coding: utf-8 -*-

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
from bs4 import BeautifulSoup

class DelDelPostprocessor(Postprocessor):
    def remove_tag(html, tag):
        soup = BeautifulSoup(html, "html5lib")
        if soup.find_all(tag):
            for t in soup.find_all(tag):
                t.replace_with("")
        return soup.prettify()

    def run(self, html):
        return self.remove_tag(html, "del")

class DelDelExtension(Extension):
    """ Delete the <del> tags with contents. """

    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add('deldel', DelDelPostprocessor(md), '_end')


def makeExtension(configs={}):
    return DelDelExtension(configs=configs)
