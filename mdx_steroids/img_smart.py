#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based on https://github.com/glushchenko/micropress/

import re

from markdown import Extension
from markdown.extensions import attr_list
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
from PIL import Image
from urlparse import urlparse
from os.path import splitext, basename, exists

class MDXSmartImageProcessor(BlockProcessor):
    NOBRACKET = r'[^\]\[]*'
    BRK = (
        r'\[(' +
        (NOBRACKET + r'(\[')*6 +
        (NOBRACKET + r'\])*')*6 +
        NOBRACKET + r')\]'
    )
    NOIMG = r'(?<!\!)'
    # [text](url) or [text](<url>) or [text](url "title")
    LINK_RE = NOIMG + BRK + \
        r'''\(\s*(<.*?>|((?:(?:\(.*?\))|[^\(\)]))*?)\s*((['"])(.*?)\12\s*)?\)'''
    # ![alttxt](http://x.com/) or ![alttxt](<http://x.com/>)
    IMAGE_LINK_RE = r'\!' + BRK + r'\s*\(\s*(<.*?>|([^"\)\s]+\s*"[^"]*"|[^\)\s]*))\s*\)'
    # ![alt text][2]
    IMAGE_REFERENCE_RE = r'\!' + BRK + r'\s?\[([^\]]*)\]'


    FIGURES = [u'^\s*'+IMAGE_LINK_RE+ u'(\{\:?([^\}]*)\})?' + u'\s*$', u'^\s*'+IMAGE_REFERENCE_RE+u'\s*$']
    INLINE_LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)(\{\:?([^\}]*)\})?')
    FIGURES_RE = re.compile(u'|'.join(f for f in FIGURES))

    def __init__(self, md, config):
        super(MDXSmartImageProcessor, self).__init__(md)
        self.config = config

    def test(self, parent, block):
        isImage = bool(self.FIGURES_RE.search(block))
        isOnlyOneLine = (len(block.splitlines()) == 1)
        if (isImage and isOnlyOneLine):
            return True
        else:
            return False

    def run(self, parent, blocks):
        alt = url = attr = None

        raw_block = blocks.pop(0)
        mdImage = self.FIGURES_RE.search(raw_block).group(0)

        rAlt = self.FIGURES_RE.search(raw_block)
        if (rAlt):
            alt = rAlt.group(1)

        rUrl = self.INLINE_LINK_RE.search(mdImage)
        if (rUrl):
            url = rUrl.group(2)

        rAttr = self.INLINE_LINK_RE.search(mdImage)
        if (rAttr):
            attr = self.INLINE_LINK_RE.search(mdImage).group(3)

        url_find = self.config.get("find", None)
        url_repl_path = self.config.get("repl_path", None)
        url_repl_url = self.config.get("repl_url", None)

        filepath = url
        orig_url = url
        if url_find and url_repl_path:
            filepath = filepath.replace(url_find, url_repl_path)
        if url_find and url_repl_url:
            url = url.replace(url_find, url_repl_url)

        width = height = 0
        img = etree.Element('img')

        if (attr):
            image_size = self.assignExtra(img, attr)
            width = image_size['width']
            height = image_size['height']

        if (width == 0 and height == 0):
            if exists(filepath):
                with Image.open(filepath) as im:
                    width, height = im.size

        cls = img.get('class', '')
        if cls:
            cls += " image"
        else:
            cls = "image"
        htmlwidth = None
        box = False
        if (width > 1280):
            htmlwidth = int(width/2)
            cls += ' imxl'
            box = True
        elif (width > 500):
            htmlwidth = int(width/2)
            cls += ' iml'
            box = True
        elif (width > 32):
            htmlwidth = int(width/2)
            cls += ' imm'
        elif (width > 0):
            htmlwidth = width
            cls += ' ims'
        if htmlwidth:
            img.set('width', str(htmlwidth))
        if (alt):
            img.set('alt', alt)
        if (cls):
            img.set('class', cls)
        img.set('src', orig_url)
        if box:
            a = etree.Element('a')
            a.set('data-fancybox', 'help')
            a.set('href', url)
            a.append(img)
            parent.append(a)
        else:
            parent.append(img)


    # ![By default](/i/ukrainian-keyboard-default.png){: width=400} assign width i.e. <img width="400"/>
    def assignExtra(self, img, attr):
        image_size = {'width': 0, 'height': 0}

        BASE_RE = r'\{\:?([^\}]*)\}'
        INLINE_RE = re.compile(r'^%s' % BASE_RE)
        NAME_RE = re.compile(r'[^A-Z_a-z\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u02ff'
                             r'\u0370-\u037d\u037f-\u1fff\u200c-\u200d'
                             r'\u2070-\u218f\u2c00-\u2fef\u3001-\ud7ff'
                             r'\uf900-\ufdcf\ufdf0-\ufffd'
                             r'\:\-\.0-9\u00b7\u0300-\u036f\u203f-\u2040]+')

        m = INLINE_RE.match(attr)
        if (m):
            attr = m.group(1)

            for k, v in attr_list.get_attrs(attr):
                if k == '.':
                    cls = img.get('class')
                    if cls:
                        img.set('class', '%s %s' % (cls, v))
                    else:
                        img.set('class', v)
                else:
                    key = NAME_RE.sub('_', k)
                    img.set(key, v)

                    if (k == 'width'):
                        image_size['width'] = v

                    if (k == 'height'):
                        image_size['height'] = v

        return image_size


class MDXSmartImageExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'find'   : ["", "the string to find in the URL"],
            'repl_path': ["", "the string to replace for the local path"],
            'repl_url': ["", "the string to replace for the final URL"],
        }
        super(MDXSmartImageExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        config = self.getConfigs()
        smartImage = MDXSmartImageProcessor(md.parser, self.getConfigs())
        md.parser.blockprocessors.add('smartImage', smartImage, '<ulist')

def makeExtension(*args, **kwargs):
    return MDXSmartImageExtension(*args, **kwargs)

