# this_file: tests/test_wikilink.py
import markdown
import pytest


TEST_CASES = [
    (
        "This is a [[Simple Link]].",
        {"base_url": "/wiki/", "end_url": "/"},
        "[Simple Link](/wiki/simple-link/)",
    ),
    (
        "Multiple [[First Link]] and [[Second Link]] here.",
        {"base_url": "/docs/", "end_url": ".html"},
        "[First Link](/docs/first-link.html)",
    ),
    (
        "Link with [[Special Characters & Symbols]].",
        {"base_url": "/", "end_url": "/"},
        "[Special Characters & Symbols](/special-characters-symbols/)",
    ),
    (
        "[[Link with Numbers 123]]",
        {"base_url": "/kb/", "end_url": ""},
        "[Link with Numbers 123](/kb/link-with-numbers-123)",
    ),
    (
        "No wiki links here.",
        {"base_url": "/wiki/", "end_url": "/"},
        "No wiki links here.",
    ),
    (
        "[[Single Word]]",
        {"base_url": "", "end_url": ""},
        "[Single Word](single-word)",
    ),
]


@pytest.mark.parametrize("md_input, config, expected_part", TEST_CASES)
def test_wikilink_extension(md_input, config, expected_part):
    """Test wikilink extension converts [[Link]] to [Link](url)."""
    md = markdown.Markdown(
        extensions=["mdx_steroids.wikilink"],
        extension_configs={"mdx_steroids.wikilink": config}
    )
    html_output = md.convert(md_input)
    
    # Since wikilink is a preprocessor, it converts to standard markdown
    # which then gets processed normally
    assert expected_part in html_output or expected_part in md.convert(md_input)


def test_wikilink_default_config():
    """Test wikilink with default configuration."""
    md_input = "See [[Main Page]] for details."
    
    md = markdown.Markdown(extensions=["mdx_steroids.wikilink"])
    
    # The preprocessor should convert to standard markdown
    # We need to check what the actual default values are
    html_output = md.convert(md_input)
    
    # Should contain a link to main-page
    assert "main-page" in html_output.lower()


def test_wikilink_space_separator():
    """Test different space separator."""
    md_input = "Link to [[My Page Name]]."
    config = {"space_sep": "_"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.wikilink"],
        extension_configs={"mdx_steroids.wikilink": config}
    )
    html_output = md.convert(md_input)
    
    # Should use underscore instead of dash
    assert "my_page_name" in html_output.lower()


def test_wikilink_multiple_words():
    """Test wikilink with multiple words."""
    md_input = "See [[Getting Started Guide]] and [[Advanced Topics]]."
    config = {"base_url": "/docs/", "end_url": ".html", "space_sep": "-"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.wikilink"],
        extension_configs={"mdx_steroids.wikilink": config}
    )
    html_output = md.convert(md_input)
    
    # Should convert both links
    assert "getting-started-guide" in html_output.lower()
    assert "advanced-topics" in html_output.lower()


def test_wikilink_empty_link():
    """Test wikilink with empty or whitespace-only content."""
    md_input = "Empty [[]] and whitespace [[   ]] links."
    
    md = markdown.Markdown(extensions=["mdx_steroids.wikilink"])
    html_output = md.convert(md_input)
    
    # Should handle gracefully - exact behavior depends on implementation
    assert "[[]]" in html_output or "[]" in html_output


def test_wikilink_special_characters():
    """Test wikilink with special characters in page name."""
    md_input = "Link to [[Page with (parentheses) & symbols!]]."
    config = {"base_url": "/", "end_url": "/"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.wikilink"],
        extension_configs={"mdx_steroids.wikilink": config}
    )
    html_output = md.convert(md_input)
    
    # Should handle special characters appropriately
    assert "page-with" in html_output.lower()


def test_wikilink_case_sensitivity():
    """Test wikilink case handling."""
    md_input = "Links: [[UPPERCASE]], [[lowercase]], [[MixedCase]]."
    
    md = markdown.Markdown(extensions=["mdx_steroids.wikilink"])
    html_output = md.convert(md_input)
    
    # Should preserve case in link text but normalize URLs
    assert "UPPERCASE" in html_output
    assert "lowercase" in html_output
    assert "MixedCase" in html_output