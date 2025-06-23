r"""
Figure Caption Extension for Python-Markdown
==================================

Converts \![alttext](http://example.com/image.png "caption")
to the image with a caption.
Its syntax is same as embedding images.

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

"""

# import re  # F401: Unused
import xml.etree.ElementTree as etree  # Standard ElementTree import
from markdown import Extension
from markdown.inlinepatterns import InlineProcessor  # Changed from ImagePattern

# Regex to capture ![%alt%](%link% "%title%") or ![%alt%](%link% '%title%')
# Group 1: Alt text
# Group 2: Link
# Group 3: Title with double quotes (optional)  # E261
# Group 4: Title with single quotes (optional)  # E261
FIGURECAPTION_RE = r'\!\[(.*?)\]\((.*?)(?:\s+(?:"(.*?)"|\'(.*?)\'))?\s*\)'


class FigureCaptionPattern(InlineProcessor):  # Changed base class
    def __init__(self, pattern, md=None):
        super().__init__(pattern, md)
        self.md = md  # Ensure md instance is stored

    def handleMatch(self, m, data):  # Added data param, returns el, start, end
        alt_text = m.group(1)
        src = m.group(2)
        # Title could be in group 3 (double quotes) or 4 (single quotes)  # E261
        title = m.group(3) if m.group(3) is not None else m.group(4)

        img = etree.Element("img")
        img.set("alt", alt_text)
        img.set("src", src)

        if title:
            # Keep title on img as well for consistency or if user expects it (E501)
            img.set("title", title)
            figure = etree.Element("figure")
            figure.append(img)
            figcaption = etree.SubElement(figure, "figcaption")
            figcaption.text = title
            return figure, m.start(0), m.end(0)
        else:
            return img, m.start(0), m.end(0)


class FigureCaptionExtension(Extension):
    def extendMarkdown(self, md):  # md_globals removed
        # Register new pattern with a priority
        # (e.g., > default image pattern priority of 150)
        md.inlinePatterns.register(
            FigureCaptionPattern(FIGURECAPTION_RE, md), "figurecaption", 155
        )
        # It's important that this runs *before* the standard image pattern
        # if it's to "steal" images with titles.
        # Or, it runs after and potentially wraps/modifies an existing img tag
        # if the standard one already ran.
        # Given it creates a new element structure (figure), running before
        # and consuming the match is cleaner.
        # However, this means it must fully handle the image link itself.
        # If we want it to modify an existing <img> tag created by the default
        # image handler, it would need to be a TreeProcessor or a very late
        # InlineProcessor that looks for specific <img>.
        # The current approach of replacing the image pattern for titled images
        # is more direct.


def makeExtension(*args, **kwargs):
    return FigureCaptionExtension(*args, **kwargs)
