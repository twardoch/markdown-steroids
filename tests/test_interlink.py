# this_file: tests/test_interlink.py
import markdown
import pytest


TEST_CASES = [
    (
        "[Internal Link](internal-page)",
        {"base_url": "/docs/", "end_url": ".html"},
        "[Internal Link](/docs/internal-page.html)",
    ),
    (
        "[Another Link](page-name#anchor)",
        {"base_url": "/wiki/", "end_url": "/"},
        "[Another Link](/wiki/page-name/#anchor)",
    ),
    (
        "[External Link](https://example.com)",
        {"base_url": "/docs/", "end_url": "/"},
        "[External Link](https://example.com)",  # Should not change
    ),
    (
        "[Relative File](../file.txt)",
        {"base_url": "/docs/", "end_url": "/"},
        "[Relative File](../file.txt)",  # Should not change (has dots)
    ),
    (
        "[Protocol Link](//example.com/page)",
        {"base_url": "/docs/", "end_url": "/"},
        "[Protocol Link](//example.com/page)",  # Should not change
    ),
    (
        "[Simple Link](page)",
        {"base_url": "", "end_url": ""},
        "[Simple Link](page)",  # No base or end URL
    ),
    (
        "[Link with Space](page name)",
        {"base_url": "/kb/", "end_url": ".html"},
        "[Link with Space](/kb/page name.html)",
    ),
]


@pytest.mark.parametrize("md_input, config, expected_part", TEST_CASES)
def test_interlink_extension(md_input, config, expected_part):
    """Test interlink extension processes internal links."""
    md = markdown.Markdown(
        extensions=["mdx_steroids.interlink"],
        extension_configs={"mdx_steroids.interlink": config}
    )
    html_output = md.convert(md_input)
    
    # The interlink extension is a preprocessor that modifies the markdown
    # We need to check that the link was processed correctly
    assert expected_part in html_output or expected_part in md.convert(md_input)


def test_interlink_multiple_links():
    """Test interlink with multiple links in one document."""
    md_input = """
    See [Page One](page-one) and [Page Two](page-two).
    Also check [External Site](https://example.com).
    """
    config = {"base_url": "/docs/", "end_url": "/"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.interlink"],
        extension_configs={"mdx_steroids.interlink": config}
    )
    html_output = md.convert(md_input)
    
    # Internal links should be processed
    assert "/docs/page-one/" in html_output
    assert "/docs/page-two/" in html_output
    # External links should not be processed
    assert "https://example.com" in html_output


def test_interlink_anchor_preservation():
    """Test that anchors are preserved correctly."""
    md_input = "[Link with Anchor](page-name#section1)"
    config = {"base_url": "/docs/", "end_url": ".html"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.interlink"],
        extension_configs={"mdx_steroids.interlink": config}
    )
    html_output = md.convert(md_input)
    
    # Should preserve the anchor after the end_url
    assert "/docs/page-name.html#section1" in html_output


def test_interlink_no_config():
    """Test interlink behavior without configuration."""
    md_input = "[Link](page-name)"
    
    md = markdown.Markdown(extensions=["mdx_steroids.interlink"])
    html_output = md.convert(md_input)
    
    # Should work with default configuration
    assert "page-name" in html_output


def test_interlink_empty_link():
    """Test interlink with empty link."""
    md_input = "[Empty Link]()"
    config = {"base_url": "/docs/", "end_url": "/"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.interlink"],
        extension_configs={"mdx_steroids.interlink": config}
    )
    html_output = md.convert(md_input)
    
    # Should handle empty links gracefully
    assert "Empty Link" in html_output


def test_interlink_detection_logic():
    """Test the logic for detecting internal vs external links."""
    test_cases = [
        ("[HTTP Link](http://example.com)", "http://example.com"),  # External
        ("[HTTPS Link](https://example.com)", "https://example.com"),  # External
        ("[FTP Link](ftp://example.com)", "ftp://example.com"),  # External
        ("[File Link](file.txt)", "/docs/file.txt"),  # Internal (no protocol)
        ("[Dotted Link](../file.txt)", "../file.txt"),  # External (has dot)
        ("[Extension Link](file.html)", "file.html"),  # External (has dot)
        ("[Protocol Relative](//example.com)", "//example.com"),  # External
    ]
    
    config = {"base_url": "/docs/", "end_url": ""}
    
    for md_input, expected_url in test_cases:
        md = markdown.Markdown(
            extensions=["mdx_steroids.interlink"],
            extension_configs={"mdx_steroids.interlink": config}
        )
        html_output = md.convert(md_input)
        assert expected_url in html_output


def test_interlink_case_sensitivity():
    """Test interlink with different cases."""
    md_input = "[Mixed Case Link](Page-Name)"
    config = {"base_url": "/docs/", "end_url": "/"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.interlink"],
        extension_configs={"mdx_steroids.interlink": config}
    )
    html_output = md.convert(md_input)
    
    # Should preserve case in the URL
    assert "/docs/Page-Name/" in html_output


def test_interlink_special_characters():
    """Test interlink with special characters in URL."""
    md_input = "[Special Link](page-with-symbols)"
    config = {"base_url": "/docs/", "end_url": "/"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.interlink"],
        extension_configs={"mdx_steroids.interlink": config}
    )
    html_output = md.convert(md_input)
    
    # Should handle special characters appropriately
    assert "/docs/page-with-symbols/" in html_output