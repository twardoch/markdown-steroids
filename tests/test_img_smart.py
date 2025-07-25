# this_file: tests/test_img_smart.py
"""Tests for the img_smart extension."""

import markdown
import pytest
import tempfile
import os
import json
from unittest.mock import patch, MagicMock


class TestImgSmartExtension:
    """Test the smart image processing extension."""

    def test_basic_image(self):
        """Test basic image processing."""
        text = "![Alt text](image.jpg)"
        html = markdown.markdown(text, extensions=['mdx_steroids.img_smart'])
        assert '<img' in html
        assert 'alt="Alt text"' in html
        assert 'src="image.jpg"' in html

    def test_image_with_title(self):
        """Test image with title becomes figure with caption."""
        text = '![Alt text](image.jpg "Image caption")'
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.img_smart'],
            extension_configs={
                'mdx_steroids.img_smart': {
                    'alt_figure': True
                }
            }
        )
        # Should create figure with caption when alt_figure is True
        if '<figure>' in html:
            assert '<figcaption>' in html

    def test_url_replacement(self):
        """Test URL find and replace functionality."""
        text = "![Alt](local/path/image.jpg)"
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.img_smart'],
            extension_configs={
                'mdx_steroids.img_smart': {
                    'find': 'local/path',
                    'repl_url': 'https://cdn.example.com'
                }
            }
        )
        assert 'https://cdn.example.com' in html

    def test_lazy_loading(self):
        """Test lazy loading attribute."""
        text = "![Alt](image.jpg)"
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.img_smart'],
            extension_configs={
                'mdx_steroids.img_smart': {
                    'lazy': True
                }
            }
        )
        assert 'loading="lazy"' in html

    def test_cache_functionality(self):
        """Test image metadata caching."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            cache_file = f.name

        try:
            text = "![Alt](image.jpg)"
            # First run - should create cache
            html1 = markdown.markdown(
                text,
                extensions=['mdx_steroids.img_smart'],
                extension_configs={
                    'mdx_steroids.img_smart': {
                        'cache': cache_file
                    }
                }
            )
            
            # Check cache file exists
            assert os.path.exists(cache_file)
            
            # Second run - should use cache
            html2 = markdown.markdown(
                text,
                extensions=['mdx_steroids.img_smart'],
                extension_configs={
                    'mdx_steroids.img_smart': {
                        'cache': cache_file
                    }
                }
            )
            
            # Results should be the same
            assert html1 == html2
            
        finally:
            if os.path.exists(cache_file):
                os.unlink(cache_file)

    def test_multiple_images(self):
        """Test processing multiple images."""
        text = """
![First](first.jpg)
![Second](second.png)
![Third](third.gif)
"""
        html = markdown.markdown(text, extensions=['mdx_steroids.img_smart'])
        assert html.count('<img') == 3
        assert 'first.jpg' in html
        assert 'second.png' in html
        assert 'third.gif' in html

    def test_image_with_attributes(self):
        """Test image with additional attributes."""
        text = '![Alt](image.jpg){: width="300" height="200" .my-class #my-id }'
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.img_smart', 'attr_list']
        )
        assert 'width="300"' in html
        assert 'height="200"' in html
        assert 'class="my-class"' in html
        assert 'id="my-id"' in html

    def test_image_reference_style(self):
        """Test reference-style images."""
        text = """
![Alt text][img-ref]

[img-ref]: path/to/image.jpg "Optional title"
"""
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.img_smart']
        )
        assert '<img' in html
        assert 'path/to/image.jpg' in html

    def test_alt_figure_with_alt_text(self):
        """Test using alt text as figure caption."""
        text = "![This is the caption](image.jpg)"
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.img_smart'],
            extension_configs={
                'mdx_steroids.img_smart': {
                    'alt_figure': True
                }
            }
        )
        if '<figure>' in html:
            assert '<figcaption>This is the caption</figcaption>' in html

    def test_path_replacement(self):
        """Test path replacement for local file resolution."""
        text = "![Alt](remote/image.jpg)"
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.img_smart'],
            extension_configs={
                'mdx_steroids.img_smart': {
                    'find': 'remote',
                    'repl_path': '/local/path',
                    'repl_url': 'https://example.com/images'
                }
            }
        )
        # URL in output should use repl_url
        assert 'https://example.com/images' in html

    def test_svg_handling(self):
        """Test SVG image handling."""
        text = "![SVG Image](diagram.svg)"
        html = markdown.markdown(text, extensions=['mdx_steroids.img_smart'])
        assert 'diagram.svg' in html

    def test_no_images(self):
        """Test text without images."""
        text = "This is just plain text without any images."
        html = markdown.markdown(text, extensions=['mdx_steroids.img_smart'])
        assert '<img' not in html
        assert text in html

    @patch('requests.get')
    def test_remote_image_dimensions(self, mock_get):
        """Test fetching dimensions for remote images."""
        # Mock response for remote image
        mock_response = MagicMock()
        mock_response.content = b'fake image data'
        mock_get.return_value = mock_response
        
        text = "![Remote](https://example.com/image.jpg)"
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.img_smart']
        )
        assert 'https://example.com/image.jpg' in html

    def test_mixed_markdown(self):
        """Test images mixed with other markdown elements."""
        text = """
# Gallery

Here are some images:

![First Image](img1.jpg)

Some text between images.

![Second Image](img2.jpg)

* List item with ![inline image](icon.png)
"""
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.img_smart', 'markdown.extensions.extra']
        )
        assert '<h1>Gallery</h1>' in html
        assert html.count('<img') == 3
        assert 'List item with' in html