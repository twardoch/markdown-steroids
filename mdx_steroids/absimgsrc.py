#!/usr/bin/env python
# this_file: mdx_steroids/absimgsrc.py
"""Absolute Image Source Extension for Python-Markdown.

This extension converts relative image URLs to absolute URLs by prepending
a configurable base URL. This is particularly useful when:

- Serving images from a CDN
- Building documentation that will be viewed from different path contexts
- Ensuring images load correctly regardless of the current page location

## Basic Usage

```python
import markdown

text = '![Alt text](images/photo.jpg)'
html = markdown.markdown(text, extensions=['mdx_steroids.absimgsrc'],
                        extension_configs={
                            'mdx_steroids.absimgsrc': {
                                'base_url': 'https://cdn.example.com/'
                            }
                        })
# Result: <img src="https://cdn.example.com/images/photo.jpg" alt="Alt text">
```

## Configuration Options

- `base_url` (str): The base URL to prepend to relative image paths.
  Default: None (no modification)

Copyright (c) 2016 Adam Twardoch <adam+github@twardoch.com>
License: [BSD 3-clause](https://opensource.org/licenses/BSD-3-Clause)
"""

__version__ = "0.4.4"

try:
    from urllib.parse import urljoin
except ImportError:
    from urllib.parse import urljoin

from markdown import Extension
from markdown.treeprocessors import Treeprocessor

# Known URL schemes that indicate absolute URLs
known_schemes = [
    'http://', 'https://', 'ftp://', 'ftps://', 
    'mailto:', 'news:', 'telnet://', 'file://',
    'data:', 'tel:', 'ssh://', 'sftp://'
]


class MDXAbsoluteImagesTreeprocessor(Treeprocessor):
    """Tree processor that converts relative image URLs to absolute URLs.
    
    This processor walks through the HTML element tree after Markdown
    conversion and updates the 'src' attribute of all img elements,
    converting relative paths to absolute URLs using the configured base URL.
    
    Attributes:
        config (dict): Configuration dictionary containing 'base_url'
    """
    
    def __init__(self, md, config):
        """Initialize the tree processor.
        
        Args:
            md: The Markdown instance
            config (dict): Configuration dictionary with 'base_url' key
        """
        super().__init__(md)
        self.config = config

    def run(self, root):
        """Process the element tree, converting relative image URLs to absolute.
        
        Args:
            root: The root element of the document tree
            
        Returns:
            The modified root element
        """
        imgs = root.iter("img")  # Modern ElementTree method
        for image in imgs:
            if "src" in image.attrib and self.is_relative(
                image.attrib["src"]
            ):  # Check if src exists
                image.set("src", self.make_external(image.attrib["src"]))

    def make_external(self, path):
        """Convert a relative path to an absolute URL.
        
        Args:
            path (str): The relative path to convert
            
        Returns:
            str: The absolute URL
            
        Examples:
            >>> processor.make_external('images/photo.jpg')
            'https://cdn.example.com/images/photo.jpg'
        """
        base_url = self.config["base_url"]
        if not base_url:
            return path
            
        # Ensure base_url ends with a slash if it's not empty and path isn't absolute
        if base_url and not base_url.endswith("/") and not path.startswith("/"):
            base_url += "/"
        return urljoin(base_url, path)

    def is_relative(self, link):
        """Check if a URL is relative.
        
        Args:
            link (str): The URL to check
            
        Returns:
            bool: True if the URL is relative, False if absolute
            
        Examples:
            >>> processor.is_relative('images/photo.jpg')
            True
            >>> processor.is_relative('https://example.com/photo.jpg')
            False
            >>> processor.is_relative('mailto:user@example.com')
            False
        """
        if link.startswith("http"):
            return False
        for scheme in known_schemes:
            if link.startswith(scheme):
                return False
        return True


class MDXAbsoluteImagesExtension(Extension):
    """Extension class for absolute image URLs.
    
    This extension adds a tree processor to convert relative image URLs
    to absolute URLs based on a configured base URL.
    
    Configuration:
        base_url (str): The base URL to prepend to relative image paths.
                       If None or empty, no modification is performed.
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize the extension with configuration options."""
        self.config = {
            "base_url": [
                None,
                "The base URL to which the relative paths will be appended",
            ],
        }

        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Register the extension with the Markdown parser.
        
        Args:
            md: The Markdown instance
        """
        absoluteImages = MDXAbsoluteImagesTreeprocessor(md, self.getConfigs())
        md.treeprocessors.add("absoluteImages", absoluteImages, "_end")
        md.registerExtension(self)


def makeExtension(*args, **kwargs):
    """Create and return an instance of the extension.
    
    This is the entry point for Markdown to create the extension.
    
    Args:
        *args: Positional arguments for the extension
        **kwargs: Keyword arguments for the extension configuration
        
    Returns:
        MDXAbsoluteImagesExtension: An instance of the extension
    """
    return MDXAbsoluteImagesExtension(*args, **kwargs)
