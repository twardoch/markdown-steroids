import markdown
import pytest

# Basic test cases
# (input_markdown, base_url_config, expected_output_html_containing)

TEST_CASES = [
    (
        "![alt text](relative/image.png)",
        {"base_url": "https://example.com/images/"},
        '<img alt="alt text" src="https://example.com/images/relative/image.png" />',
    ),
    (
        'Some text with an image: ![alt text](another/image.jpg "title").',
        {"base_url": "https://cdn.test.com/assets/"},
        '<img alt="alt text" src="https://cdn.test.com/assets/another/image.jpg" title="title" />',
    ),
    (
        "![alt text](http://absolute.com/image.png)",  # Already absolute
        {"base_url": "https://example.com/images/"},
        '<img alt="alt text" src="http://absolute.com/image.png" />',  # Should remain unchanged
    ),
    (
        "![alt text](//protocol-relative.com/image.png)",  # Protocol-relative
        {"base_url": "https://example.com/images/"},
        '<img alt="alt text" src="//protocol-relative.com/image.png" />',  # Should remain unchanged based on current logic (is_relative checks for http)
    ),
    (
        "Image: ![alt text](image.gif)",  # No leading slash in image path
        {"base_url": "https://example.com/images"},  # base_url without trailing slash
        '<img alt="alt text" src="https://example.com/images/image.gif" />',  # urljoin should handle this
    ),
    (
        "Image: ![alt text](/image.gif)",  # Leading slash in image path
        {"base_url": "https://example.com/images/"},  # base_url with trailing slash
        '<img alt="alt text" src="https://example.com/image.gif" />',  # Corrected: urljoin behavior for absolute paths
    ),
    (
        "Image: ![alt text](image.gif)",
        {"base_url": "http://localhost:8000/my/folder/"},
        '<img alt="alt text" src="http://localhost:8000/my/folder/image.gif" />',
    ),
    (
        "<p>No image here.</p>",
        {"base_url": "https://example.com/images/"},
        "<p>No image here.</p>",  # Should not affect non-image elements
    ),
    (
        "![alt text](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)",  # Data URI
        {"base_url": "https://example.com/images/"},
        '<img alt="alt text" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" />',  # Should remain unchanged
    ),
]


@pytest.mark.parametrize("md_input, config, expected_html_part", TEST_CASES)
def test_absimgsrc_various_cases(md_input, config, expected_html_part):
    """Test absimgsrc extension with various inputs and configurations."""
    md = markdown.Markdown(
        extensions=["mdx_steroids.absimgsrc"],
        extension_configs={"mdx_steroids.absimgsrc": config},
    )
    html_output = md.convert(md_input)
    print(f"Input MD:\n{md_input}")
    print(f"Config:\n{config}")
    print(f"Output HTML:\n{html_output}")
    print(f"Expected part:\n{expected_html_part}")
    assert expected_html_part in html_output


def test_absimgsrc_no_base_url_config():
    """
    Test behavior when base_url is not provided.
    The extension code currently would raise a KeyError if base_url is not in getConfigs().
    Let's verify this or decide if it should fail gracefully or do nothing.
    For now, expecting it to not process if config is missing/empty.
    """
    md_input = "![alt text](relative/image.png)"
    # Option 1: Extension is not configured, so it shouldn't run.
    # md = markdown.Markdown(extensions=['mdx_steroids.absimgsrc'])
    # html_output = md.convert(md_input)
    # assert '<img alt="alt text" src="relative/image.png" />' in html_output

    # Option 2: Extension configured but base_url is None or empty (current code might error)
    # Based on current absimgsrc.py, self.config["base_url"] will be called.
    # If 'base_url' is not in the dict from getConfigs(), it's a KeyError.
    # If 'base_url' is [None, "..."], then self.config["base_url"] is None. urljoin(None, path) is an error.

    # Test case: base_url is explicitly None in config
    # This should cause urljoin to fail if not handled.
    # The current code MDXAbsoluteImagesTreeprocessor assumes self.config['base_url'] is a string.
    # A None value for base_url will likely cause a TypeError with urljoin.
    # Let's test that it doesn't transform if base_url is not a usable string.
    # The extension's default config is `base_url: [None, "..."]`. If not overridden, `getConfigs()['base_url']` will be None.

    md_config_none = markdown.Markdown(
        extensions=["mdx_steroids.absimgsrc"],
        extension_configs={"mdx_steroids.absimgsrc": {"base_url": None}},
    )
    html_output_none = md_config_none.convert(md_input)
    assert (
        '<img alt="alt text" src="relative/image.png" />' in html_output_none
    ), "Should not change if base_url is None"

    md_config_empty_string = markdown.Markdown(
        extensions=["mdx_steroids.absimgsrc"],
        extension_configs={"mdx_steroids.absimgsrc": {"base_url": ""}},
    )
    html_output_empty = md_config_empty_string.convert(md_input)
    # urljoin('', 'relative/image.png') -> 'relative/image.png'
    assert (
        '<img alt="alt text" src="relative/image.png" />' in html_output_empty
    ), "Should effectively not change if base_url is empty string"


def test_is_relative_logic():
    """Test the is_relative helper method logic directly if possible, or infer through behavior."""
    # This is harder to test directly without instantiating the Treeprocessor,
    # but test cases for various URL schemes (http, https, ftp, data, //) cover it.
    # The current `is_relative` checks `link.startswith('http')`.
    # So 'https' will be seen as relative. This needs fixing in the extension.
    # Let's add a test case for this in TEST_CASES and then fix the code.
    pass


# Add a specific test case for https to highlight the bug in current `is_relative`
HTTPS_FIX_CASES = [
    (
        "![alt text](https://absolute.com/image.png)",  # Already absolute with https
        {"base_url": "https://example.com/images/"},
        '<img alt="alt text" src="https://absolute.com/image.png" />',  # Should remain unchanged
    ),
]


@pytest.mark.parametrize("md_input, config, expected_html_part", HTTPS_FIX_CASES)
def test_absimgsrc_https_case(md_input, config, expected_html_part):
    md = markdown.Markdown(
        extensions=["mdx_steroids.absimgsrc"],
        extension_configs={"mdx_steroids.absimgsrc": config},
    )
    html_output = md.convert(md_input)
    assert expected_html_part in html_output


# Consider a test case if the image tag has other attributes
COMPLEX_IMG_TAG_CASE = [
    (
        '<img src="relative/image.png" id="myimage" class="test-img" style="width:100px;" />',
        {"base_url": "https://example.com/assets/"},
        # Corrected: Raw HTML img tags are not processed by this extension's treeprocessor
        '<img src="relative/image.png" id="myimage" class="test-img" style="width:100px;" />',
    )
]


@pytest.mark.parametrize("md_input, config, expected_html_part", COMPLEX_IMG_TAG_CASE)
def test_absimgsrc_complex_img_tag(md_input, config, expected_html_part):
    """Test that other attributes on the img tag are preserved."""
    md = markdown.Markdown(
        extensions=["mdx_steroids.absimgsrc"],
        extension_configs={"mdx_steroids.absimgsrc": config},
    )
    html_output = md.convert(md_input)
    print(f"Complex Input MD:\n{md_input}")
    print(f"Complex Config:\n{config}")
    print(f"Complex Output HTML:\n{html_output}")
    print(f"Complex Expected part:\n{expected_html_part}")
    assert expected_html_part in html_output
