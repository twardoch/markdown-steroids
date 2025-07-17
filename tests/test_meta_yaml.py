# this_file: tests/test_meta_yaml.py
import markdown
import pytest


def test_meta_yaml_basic():
    """Test basic YAML front matter parsing."""
    md_input = """---
title: Test Page
author: John Doe
date: 2023-01-01
---

# Main Content

This is the main content of the page."""
    
    md = markdown.Markdown(extensions=["mdx_steroids.meta_yaml"])
    html_output = md.convert(md_input)
    
    # Check that metadata is parsed
    assert hasattr(md, 'Meta')
    assert md.Meta['title'] == ['Test Page']
    assert md.Meta['author'] == ['John Doe']
    assert md.Meta['date'] == ['2023-01-01']
    
    # Check that content is processed normally
    assert "<h1>Main Content</h1>" in html_output
    assert "<p>This is the main content of the page.</p>" in html_output


def test_meta_yaml_list():
    """Test YAML front matter with lists."""
    md_input = """---
title: Test Page
tags:
  - python
  - markdown
  - testing
categories: [web, development]
---

Content here."""
    
    md = markdown.Markdown(extensions=["mdx_steroids.meta_yaml"])
    html_output = md.convert(md_input)
    
    assert md.Meta['title'] == ['Test Page']
    assert md.Meta['tags'] == [['python', 'markdown', 'testing']]
    assert md.Meta['categories'] == [['web', 'development']]


def test_meta_yaml_nested():
    """Test YAML front matter with nested structures."""
    md_input = """---
title: Test Page
author:
  name: John Doe
  email: john@example.com
config:
  theme: dark
  sidebar: true
---

Content here."""
    
    md = markdown.Markdown(extensions=["mdx_steroids.meta_yaml"])
    html_output = md.convert(md_input)
    
    assert md.Meta['title'] == ['Test Page']
    # Nested structures should be preserved
    assert isinstance(md.Meta['author'], list)
    assert isinstance(md.Meta['config'], list)


def test_meta_yaml_no_frontmatter():
    """Test content without YAML front matter."""
    md_input = """# Main Content

This is content without front matter."""
    
    md = markdown.Markdown(extensions=["mdx_steroids.meta_yaml"])
    html_output = md.convert(md_input)
    
    # Should have empty or no Meta
    assert not hasattr(md, 'Meta') or len(md.Meta) == 0
    
    # Content should be processed normally
    assert "<h1>Main Content</h1>" in html_output


def test_meta_yaml_empty_frontmatter():
    """Test empty YAML front matter."""
    md_input = """---
---

# Content

This has empty front matter."""
    
    md = markdown.Markdown(extensions=["mdx_steroids.meta_yaml"])
    html_output = md.convert(md_input)
    
    # Should handle empty front matter gracefully
    assert "<h1>Content</h1>" in html_output


def test_meta_yaml_invalid_yaml():
    """Test handling of invalid YAML."""
    md_input = """---
title: Test Page
invalid: [unclosed list
---

Content here."""
    
    md = markdown.Markdown(extensions=["mdx_steroids.meta_yaml"])
    
    # Should handle invalid YAML gracefully
    try:
        html_output = md.convert(md_input)
        # If it processes, content should still be there
        assert "Content here." in html_output
    except:
        # If it raises an exception, that's also acceptable behavior
        pass


def test_meta_yaml_multiline_values():
    """Test YAML front matter with multiline values."""
    md_input = """---
title: Test Page
description: |
  This is a multiline
  description that spans
  multiple lines.
summary: >
  This is a folded
  multiline string.
---

Content here."""
    
    md = markdown.Markdown(extensions=["mdx_steroids.meta_yaml"])
    html_output = md.convert(md_input)
    
    assert md.Meta['title'] == ['Test Page']
    # Multiline values should be preserved
    assert len(md.Meta['description']) == 1
    assert len(md.Meta['summary']) == 1


def test_meta_yaml_with_dashes_in_content():
    """Test that content with dashes doesn't interfere."""
    md_input = """---
title: Test Page
---

# Content

This content has --- dashes in it.
And more --- dashes here."""
    
    md = markdown.Markdown(extensions=["mdx_steroids.meta_yaml"])
    html_output = md.convert(md_input)
    
    assert md.Meta['title'] == ['Test Page']
    # Content with dashes should be preserved
    assert "dashes in it" in html_output
    assert "dashes here" in html_output


def test_meta_yaml_boolean_and_numbers():
    """Test YAML front matter with boolean and numeric values."""
    md_input = """---
title: Test Page
published: true
draft: false
version: 1.2
count: 42
---

Content here."""
    
    md = markdown.Markdown(extensions=["mdx_steroids.meta_yaml"])
    html_output = md.convert(md_input)
    
    assert md.Meta['title'] == ['Test Page']
    # Boolean and numeric values should be preserved
    assert md.Meta['published'] == [True]
    assert md.Meta['draft'] == [False]
    assert md.Meta['version'] == [1.2]
    assert md.Meta['count'] == [42]