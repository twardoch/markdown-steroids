# this_file: tests/test_md_mako.py
"""Tests for the md_mako extension."""

import markdown
import pytest
import tempfile
import os


class TestMdMakoExtension:
    """Test the Mako templating extension."""

    def test_basic_variable_substitution(self):
        """Test basic Mako variable substitution."""
        text = "Hello ${name}!"
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.md_mako'],
            extension_configs={
                'mdx_steroids.md_mako': {
                    'meta': {'name': 'World'}
                }
            }
        )
        assert "Hello World!" in html

    def test_python_expression(self):
        """Test Python expressions in Mako."""
        text = "2 + 2 = ${2 + 2}"
        html = markdown.markdown(text, extensions=['mdx_steroids.md_mako'])
        assert "2 + 2 = 4" in html

    def test_for_loop(self):
        """Test Mako for loop."""
        text = """
% for item in items:
- ${item}
% endfor
"""
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.md_mako'],
            extension_configs={
                'mdx_steroids.md_mako': {
                    'meta': {'items': ['Apple', 'Banana', 'Cherry']}
                }
            }
        )
        assert 'Apple' in html
        assert 'Banana' in html
        assert 'Cherry' in html

    def test_conditional(self):
        """Test Mako conditional statements."""
        text = """
% if show_message:
This message is visible.
% else:
This message is hidden.
% endif
"""
        # Test with True
        html_true = markdown.markdown(
            text,
            extensions=['mdx_steroids.md_mako'],
            extension_configs={
                'mdx_steroids.md_mako': {
                    'meta': {'show_message': True}
                }
            }
        )
        assert "This message is visible." in html_true
        assert "This message is hidden." not in html_true

        # Test with False
        html_false = markdown.markdown(
            text,
            extensions=['mdx_steroids.md_mako'],
            extension_configs={
                'mdx_steroids.md_mako': {
                    'meta': {'show_message': False}
                }
            }
        )
        assert "This message is visible." not in html_false
        assert "This message is hidden." in html_false

    def test_python_block(self):
        """Test Python block functionality."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def double(x):
    return x * 2

def greet(name):
    return f"Hello, {name}!"
""")
            python_file = f.name

        try:
            text = """
The double of 5 is ${double(5)}.
${greet("Alice")}
"""
            html = markdown.markdown(
                text,
                extensions=['mdx_steroids.md_mako'],
                extension_configs={
                    'mdx_steroids.md_mako': {
                        'python_block': python_file
                    }
                }
            )
            assert "The double of 5 is 10" in html
            assert "Hello, Alice!" in html
        finally:
            os.unlink(python_file)

    def test_include_file(self):
        """Test file inclusion."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create include file
            include_file = os.path.join(tmpdir, 'header.md')
            with open(include_file, 'w') as f:
                f.write("## Included Header\n\nThis is included content.")

            text = """
# Main Document

<%include file="header.md"/>

Main content here.
"""
            html = markdown.markdown(
                text,
                extensions=['mdx_steroids.md_mako'],
                extension_configs={
                    'mdx_steroids.md_mako': {
                        'include_base': tmpdir
                    }
                }
            )
            assert "Included Header" in html
            assert "This is included content" in html
            assert "Main content here" in html

    def test_combined_with_meta_yaml(self):
        """Test md_mako working with meta_yaml extension."""
        text = """---
title: My Page
author: John Doe
---

# ${title}

Written by ${author}
"""
        md = markdown.Markdown(
            extensions=['mdx_steroids.meta_yaml', 'mdx_steroids.md_mako']
        )
        html = md.convert(text)
        assert "My Page" in html
        assert "John Doe" in html

    def test_undefined_variable(self):
        """Test handling of undefined variables."""
        text = "Hello ${undefined_var}!"
        # This should raise an error or handle gracefully
        with pytest.raises(Exception):
            markdown.markdown(text, extensions=['mdx_steroids.md_mako'])

    def test_escape_mako_syntax(self):
        """Test escaping Mako syntax."""
        text = "This is literal: ${'${variable}'}"
        html = markdown.markdown(text, extensions=['mdx_steroids.md_mako'])
        assert "${variable}" in html

    def test_complex_template(self):
        """Test complex Mako template with multiple features."""
        text = """
<%
    import datetime
    current_year = datetime.datetime.now().year
%>

# Report for ${current_year}

% for month in ['January', 'February', 'March']:
## ${month} ${current_year}

% if month == 'January':
Start of the year!
% endif

% endfor

Total items: ${len(items)}
"""
        html = markdown.markdown(
            text,
            extensions=['mdx_steroids.md_mako'],
            extension_configs={
                'mdx_steroids.md_mako': {
                    'meta': {'items': [1, 2, 3, 4, 5]}
                }
            }
        )
        import datetime
        current_year = datetime.datetime.now().year
        assert f"Report for {current_year}" in html
        assert "January" in html
        assert "Start of the year!" in html
        assert "Total items: 5" in html

    def test_auto_include(self):
        """Test automatic file inclusion."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create auto-include file
            auto_file = os.path.join(tmpdir, 'auto.mako')
            with open(auto_file, 'w') as f:
                f.write("<%\n    site_name = 'My Site'\n%>")

            text = "Welcome to ${site_name}!"
            html = markdown.markdown(
                text,
                extensions=['mdx_steroids.md_mako'],
                extension_configs={
                    'mdx_steroids.md_mako': {
                        'include_auto': auto_file
                    }
                }
            )
            assert "Welcome to My Site!" in html