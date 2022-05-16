#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based on https://github.com/glushchenko/micropress/

from __future__ import absolute_import
from __future__ import print_function
import re, json
from pathlib import Path

from markdown import Extension
from markdown.extensions import attr_list
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import PIL, PIL.Image
import imageio.v3 as iio
import filetype

# from urlparse import urlparse
from os.path import splitext, basename, exists, realpath
import requests, io


class MDXSmartImageProcessor(BlockProcessor):
    NOBRACKET = r"[^\]\[]*"
    BRK = (
        r"\[("
        + (NOBRACKET + r"(\[") * 6
        + (NOBRACKET + r"\])*") * 6
        + NOBRACKET
        + r")\]"
    )
    NOIMG = r"(?<!\!)"
    # [text](url) or [text](<url>) or [text](url "title")
    LINK_RE = (
        NOIMG
        + BRK
        + r"""\(\s*(<.*?>|((?:(?:\(.*?\))|[^\(\)]))*?)\s*((['"])(.*?)\12\s*)?\)"""
    )
    # ![alttxt](http://x.com/) or ![alttxt](<http://x.com/>)
    IMAGE_LINK_RE = r"\!" + BRK + r'\s*\(\s*(<.*?>|([^"\)\s]+\s*"[^"]*"|[^\)\s]*))\s*\)'
    # ![alt text][2]
    IMAGE_REFERENCE_RE = r"\!" + BRK + r"\s?\[([^\]]*)\]"

    FIGURES = [
        "^\s*" + IMAGE_LINK_RE + "(\{\:?([^\}]*)\})?" + "\s*$",
        "^\s*" + IMAGE_REFERENCE_RE + "\s*$",
    ]
    INLINE_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)(\{\:?([^\}]*)\})?")
    FIGURES_RE = re.compile("|".join(f for f in FIGURES))

    SVG_VIEWBOX_RE = re.compile(r'viewBox="(\d*?) (\d*?) (\d*?) (\d*?)"')

    def __init__(self, md, config):
        super(MDXSmartImageProcessor, self).__init__(md)
        self.config = config

    def test(self, parent, block):
        isImage = bool(self.FIGURES_RE.search(block))
        isOnlyOneLine = len(block.splitlines()) == 1
        return isImage and isOnlyOneLine

    def run(self, parent, blocks):
        cache_path = self.config.get("cache", "")
        cache = {}
        if cache_path and exists(cache_path):
            with open(cache_path) as f:
                cache = json.load(f)

        alt = url = attr = None

        raw_block = blocks.pop(0)
        mdImage = self.FIGURES_RE.search(raw_block).group(0)

        if rAlt := self.FIGURES_RE.search(raw_block):
            alt = rAlt.group(1)

        if rUrl := self.INLINE_LINK_RE.search(mdImage):
            url = rUrl.group(2)

        if rAttr := self.INLINE_LINK_RE.search(mdImage):
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

        if filepath in cache.keys():
            media = cache[filepath]["media"]
            width = cache[filepath]["width"]
            height = cache[filepath]["height"]
        else:
            width = height = 0
            imbytes = imbytesio = immeta = None
            if filepath.startswith("http"):
                try:
                    response = requests.get(filepath)
                    imbytesio = io.BytesIO(response.content)
                except:
                    pass
            elif exists(filepath):
                imbytesio = open(filepath, "rb")
            if imbytesio:
                imbytes = imbytesio.read()
                print(f"Analyzing image: {filepath} with size {len(imbytes)}")
                media = ""
                if b"</svg>" in imbytes and b"<svg" in imbytes:
                    svg = str(imbytes)
                    media = "svg"
                    rem = self.SVG_VIEWBOX_RE.search(svg)
                    if rem:
                        width = int(rem.group(3)) - int(rem.group(1))
                        height = int(rem.group(4)) - int(rem.group(2))
                elif b"</html>" in imbytes and b"<html" in imbytes:
                    media = "html"
                    print(f"WARNING: {filepath} is of type HTML, possibly 404")
                else:
                    guess = filetype.guess_mime(imbytes)
                    if guess:
                        media = guess.split("/")[0].replace('image', 'img')
                try:
                    imbytesio.seek(0)
                    if media in ('video'):
                        frames = iio.imread(imbytesio, plugin="pyav", index=None)
                        if frames.any():
                            width = frames.shape[1]
                            height = frames.shape[2]
                    elif media in ('img'):
                        immeta = iio.immeta(imbytesio)
                        if immeta:
                            width, height = immeta.get('shape', (None, None))
                except:
                    print(f"{filepath} is not a valid video, image or SVG")
                imbytesio.close()

        if width > 1920:
            height = int(height * 1920 / width)
            width = 1920
        if height > 1080:
            width = int(width * 1080 / height)
            height = 1080
        if width:
            cache[filepath] = {"media": media, "width": width, "height": height}
        if cache_path:
            with open(cache_path, "w") as f:
                json.dump(cache, f)

        scale = 2.0
        title = None

        img = etree.Element("img")

        image_size = {}
        if attr:
            image_size = self.assignExtra(img, attr)
            width = int(image_size.get("width", width))
            height = int(image_size.get("height", height))
            scale = float(image_size.get("scale", scale))
            title = image_size.get("title", title)


        htmlcls = img.get("class", "")
        if htmlcls:
            htmlcls += " image"
        else:
            htmlcls = "image"
        htmlwidth = None
        box = False
        if int(width / scale) > 1280:
            htmlwidth = int(width / scale)
            htmlcls += " imxl"
            box = True
        elif int(width / scale) > 500:
            htmlwidth = int(width / scale)
            htmlcls += " iml"
            box = True
        elif int(width / scale) > 32:
            htmlwidth = int(width / scale)
            htmlcls += " imm"
        elif width > 0:
            htmlwidth = width
            htmlcls += " ims"
        if htmlwidth:
            img.set("width", str(htmlwidth))
        if alt:
            img.set("alt", alt)
        if htmlcls:
            img.set("class", htmlcls)
        img.set("src", orig_url)
        if self.config.get("lazy", False):
            img.set("loading", "lazy")

        insel = img
        if box:
            a = etree.Element("a")
            a.set("data-fancybox", "help")
            a.set("class", "fancybox")
            if title:
                a.set("data-caption", title)
            elif alt:
                a.set("data-caption", alt)
            a.set("href", url)
            a.append(img)
            insel = a
        if alt and alt_figure:
            figure = etree.Element("figure")
            figure.append(insel)
            figcaption = etree.Element("figcaption")
            figcaption.text = alt
            figure.append(figcaption)
            insel = figure
        parent.append(insel)

    # ![By default](/i/ukrainian-keyboard-default.png){: width=400} assign width i.e. <img width="400"/>
    def assignExtra(self, img, attr):
        image_size = {}

        BASE_RE = r"\{\:?([^\}]*)\}"
        INLINE_RE = re.compile(r"^%s" % BASE_RE)
        NAME_RE = re.compile(
            r"[^A-Z_a-z\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u02ff"
            r"\u0370-\u037d\u037f-\u1fff\u200c-\u200d"
            r"\u2070-\u218f\u2c00-\u2fef\u3001-\ud7ff"
            r"\uf900-\ufdcf\ufdf0-\ufffd"
            r"\:\-\.0-9\u00b7\u0300-\u036f\u203f-\u2040]+"
        )

        m = INLINE_RE.match(attr)
        if m:
            attr = m.group(1)

            for k, v in attr_list.get_attrs(attr):
                if k == ".":
                    if v == "lores":
                        image_size["scale"] = 1.0
                    htmlcls = img.get("class")
                    if htmlcls:
                        img.set("class", "%s %s" % (htmlcls, v))
                    else:
                        img.set("class", v)
                else:
                    if k == "data-scale":
                        try:
                            image_size["scale"] = 1 / int(v.rstrip("%")) * 100
                        except ValueError:
                            pass
                    else:
                        key = NAME_RE.sub("_", k)
                        img.set(key, v)

                    if k == "width":
                        image_size["width"] = v

                    if k == "height":
                        image_size["height"] = v

        return image_size


class MDXSmartImageExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            "find": ["", "the string to find in the URL"],
            "repl_path": ["", "the string to replace for the local path"],
            "repl_url": ["", "the string to replace for the final URL"],
            "alt_figure": [False, "Build <figure> from ![alt]() text"],
            "cache": ["", "cache JSON file to speed up processing"],
            "lazy": [False, 'Add loading="lazy" attribute to images'],
        }
        super(MDXSmartImageExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        config = self.getConfigs()
        smartImage = MDXSmartImageProcessor(md.parser, self.getConfigs())
        md.parser.blockprocessors.add("smartImage", smartImage, "<ulist")


def makeExtension(*args, **kwargs):
    return MDXSmartImageExtension(*args, **kwargs)
