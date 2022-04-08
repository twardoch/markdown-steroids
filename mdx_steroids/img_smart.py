#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based on https://github.com/glushchenko/micropress/

from __future__ import absolute_import
from __future__ import print_function
import re

from markdown import Extension
from markdown.extensions import attr_list
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import PIL, PIL.Image
#from urlparse import urlparse
from os.path import splitext, basename, exists
import requests, io

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
        alt_figure = self.config.get("alt_figure", False)

        filepath = url
        orig_url = url
        if url_find and url_repl_path:
            filepath = filepath.replace(url_find, url_repl_path)
        if url_find and url_repl_url:
            url = url.replace(url_find, url_repl_url)

        width = height = 0
        img = etree.Element('img')
        scale = 2.0
        title = None

        if (attr):
            image_size = self.assignExtra(img, attr)
            width = int(image_size.get('width', 0))
            height = int(image_size.get('height', 0))
            scale = float(image_size.get('scale', 2))
            title = image_size.get('title', None)

        if (width == 0 and height == 0):
            imb = None
            if filepath.startswith('http'):
                try:
                    response = requests.get(filepath)
                    imb = io.BytesIO(response.content)
                except:
                    pass
            elif exists(filepath):
                imb = open(filepath, "rb")
            if imb:
                try:
                    im = PIL.Image.open(imb)
                    width, height = im.size
                    imb.close()
                except PIL.UnidentifiedImageError:
                    print(f"{filepath} is not an image")

        htmlcls = img.get('class', '')
        if htmlcls:
            htmlcls += " image"
        else:
            htmlcls = "image"
        htmlwidth = None
        box = False
        if (int(width/scale) > 1280):
            htmlwidth = int(width/scale)
            htmlcls += ' imxl'
            box = True
        elif (int(width/scale) > 500):
            htmlwidth = int(width/scale)
            htmlcls += ' iml'
            box = True
        elif (int(width/scale) > 32):
            htmlwidth = int(width/scale)
            htmlcls += ' imm'
        elif (width > 0):
            htmlwidth = width
            htmlcls += ' ims'
        if htmlwidth:
            img.set('width', str(htmlwidth))
        if (alt):
            img.set('alt', alt)
        if (htmlcls):
            img.set('class', htmlcls)
        img.set('src', orig_url)

        insel = img
        if box:
            a = etree.Element('a')
            a.set('data-fancybox', 'help')
            a.set('class', 'fancybox')
            if title:
                a.set('data-caption', title)
            elif alt:
                a.set('data-caption', alt)
            a.set('href', url)
            a.append(img)
            insel = a
        if (alt and alt_figure):
            figure = etree.Element('figure')
            figure.append(insel)
            figcaption = etree.Element('figcaption')
            figcaption.text = alt
            figure.append(figcaption)
            insel = figure
        parent.append(insel)

    # ![By default](/i/ukrainian-keyboard-default.png){: width=400} assign width i.e. <img width="400"/>
    def assignExtra(self, img, attr):
        image_size = {'width': 0, 'height': 0, 'scale': 2.0}

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
                    if v == 'lores':
                        image_size['scale'] = 1.0
                    htmlcls = img.get('class')
                    if htmlcls:
                        img.set('class', '%s %s' % (htmlcls, v))
                    else:
                        img.set('class', v)
                else:
                    if (k == 'data-scale'):
                        try:
                            image_size['scale'] = 1/int(v.rstrip("%"))*100
                        except ValueError:
                            pass
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
            'alt_figure': [False, "Build <figure> from ![alt]() text"],
        }
        super(MDXSmartImageExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        config = self.getConfigs()
        smartImage = MDXSmartImageProcessor(md.parser, self.getConfigs())
        md.parser.blockprocessors.add('smartImage', smartImage, '<ulist')

def makeExtension(*args, **kwargs):
    return MDXSmartImageExtension(*args, **kwargs)
