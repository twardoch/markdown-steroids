# this_file: tests/test_keys.py
"""Tests for the keys extension."""

import markdown
import pytest


class TestKeysExtension:
    """Test the keys keyboard shortcut extension."""

    def test_basic_key_combination(self):
        """Test basic key combinations."""
        text = "Press ++Ctrl+S++ to save."
        html = markdown.markdown(text, extensions=['mdx_steroids.keys'])
        assert '<kbd' in html
        assert 'Ctrl' in html
        assert 'S' in html

    def test_string_input(self):
        """Test string input formatting."""
        text = 'Type ++"Hello World"++ exactly.'
        html = markdown.markdown(text, extensions=['mdx_steroids.keys'])
        assert '<kbd>Hello World</kbd>' in html

    def test_multiple_keys(self):
        """Test multiple key combinations."""
        text = "Use ++Ctrl+Shift+I++ for developer tools."
        html = markdown.markdown(text, extensions=['mdx_steroids.keys'])
        assert 'Ctrl' in html
        assert 'Shift' in html
        assert 'I' in html

    def test_special_keys(self):
        """Test special key names."""
        text = "Press ++Enter++ or ++Escape++ or ++Tab++."
        html = markdown.markdown(text, extensions=['mdx_steroids.keys'])
        assert 'Enter' in html
        assert 'Escape' in html
        assert 'Tab' in html

    def test_custom_separator(self):
        """Test custom separator configuration."""
        text = "Press ++Ctrl+Alt+Delete++."
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.keys'],
            extension_configs={
                'mdx_steroids.keys': {
                    'separator': ' - '
                }
            }
        )
        assert ' - ' in html

    def test_strict_mode(self):
        """Test strict HTML5 mode."""
        text = "Press ++Ctrl+S++."
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.keys'],
            extension_configs={
                'mdx_steroids.keys': {
                    'strict': True
                }
            }
        )
        # In strict mode, uses nested <kbd> elements
        assert html.count('<kbd') >= 2  # At least outer and inner kbd

    def test_non_strict_mode(self):
        """Test non-strict mode with span wrapper."""
        text = "Press ++Ctrl+S++."
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.keys'],
            extension_configs={
                'mdx_steroids.keys': {
                    'strict': False
                }
            }
        )
        assert '<span class="keys">' in html

    def test_camel_case(self):
        """Test CamelCase key names."""
        text = "Press ++PageUp++ or ++PageDown++."
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.keys'],
            extension_configs={
                'mdx_steroids.keys': {
                    'camel_case': True
                }
            }
        )
        assert 'Page Up' in html or 'PageUp' in html
        assert 'Page Down' in html or 'PageDown' in html

    def test_custom_css_class(self):
        """Test custom CSS class configuration."""
        text = "Press ++Enter++."
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.keys'],
            extension_configs={
                'mdx_steroids.keys': {
                    'class': 'keyboard-keys'
                }
            }
        )
        assert 'keyboard-keys' in html

    def test_mixed_content(self):
        """Test keys mixed with other markdown."""
        text = """
# Keyboard Shortcuts

Press ++Ctrl+S++ to **save** your work.

Common shortcuts:
- ++Ctrl+C++ - Copy
- ++Ctrl+V++ - Paste
- ++Ctrl+Z++ - Undo
"""
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.keys', 'markdown.extensions.extra']
        )
        assert '<h1>Keyboard Shortcuts</h1>' in html
        assert '<strong>save</strong>' in html
        assert '<kbd' in html

    def test_no_keys(self):
        """Test text without keyboard shortcuts."""
        text = "This is normal text without any keyboard shortcuts."
        html = markdown.markdown(text, extensions=['mdx_steroids.keys'])
        assert '<kbd' not in html
        assert text in html

    def test_incomplete_syntax(self):
        """Test incomplete key syntax."""
        text = "This ++is not complete"
        html = markdown.markdown(text, extensions=['mdx_steroids.keys'])
        # Should not process incomplete syntax
        assert '<kbd' not in html
        assert '++is not complete' in html

    def test_empty_keys(self):
        """Test empty key syntax."""
        text = "This ++++ is empty"
        html = markdown.markdown(text, extensions=['mdx_steroids.keys'])
        # Should not create empty kbd elements
        assert '<kbd></kbd>' not in html

    def test_function_keys(self):
        """Test function key formatting."""
        text = "Press ++F1++ for help or ++F12++ for developer tools."
        html = markdown.markdown(text, extensions=['mdx_steroids.keys'])
        assert 'F1' in html
        assert 'F12' in html

    def test_modifier_keys(self):
        """Test modifier key combinations."""
        text = "Use ++Cmd+Shift+4++ on Mac or ++Win+Shift+S++ on Windows."
        html = markdown.markdown(text, extensions=['mdx_steroids.keys'])
        assert 'Cmd' in html
        assert 'Win' in html
        assert 'Shift' in html

    def test_arrow_keys(self):
        """Test arrow key formatting."""
        text = "Navigate with ++Up++, ++Down++, ++Left++, and ++Right++."
        html = markdown.markdown(text, extensions=['mdx_steroids.keys'])
        for direction in ['Up', 'Down', 'Left', 'Right']:
            assert direction in html