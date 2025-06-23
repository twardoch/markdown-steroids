import markdown
import pytest

# Test cases: (input_markdown, expected_html_output_containing_list)
FIGCAP_TEST_CASES = [
    (
        '![alt text](image.png "This is the caption")',
        [
            "<figure>",
            '<img alt="alt text" src="image.png" title="This is the caption" />',  # Original title should be preserved on img if needed, or removed if only for figcaption
            "<figcaption>This is the caption</figcaption>",
            "</figure>",
        ],
    ),
    (
        "![alt text](image.png)",  # No title
        ['<img alt="alt text" src="image.png" />'],  # Should be a normal image
    ),
    (
        'An image ![alt text](image.png "Caption here") and text.',
        [
            "<figure>",
            '<img alt="alt text" src="image.png" title="Caption here" />',
            "<figcaption>Caption here</figcaption>",
            "</figure>",
        ],
    ),
    (
        "No title here: ![alt text](no_title.jpg).",
        ['<img alt="alt text" src="no_title.jpg" />'],
    ),
    (  # Ensure other attributes on image are handled if possible (though Markdown only specifies alt, src, title)
        # Standard markdown ![]() doesn't support classes directly on the image from markdown text.
        # This test is more about ensuring the figcaption logic works cleanly.
        '![alt with "quotes" and spaces](url/to/image.jpeg "Caption with & ampersand and < > symbols")',
        [
            "<figure>",
            '<img alt="alt with &quot;quotes&quot; and spaces" src="url/to/image.jpeg" title="Caption with &amp; ampersand and &lt; &gt; symbols" />',
            "<figcaption>Caption with &amp; ampersand and &lt; &gt; symbols</figcaption>",
            "</figure>",
        ],
    ),
]


@pytest.mark.parametrize("md_input, expected_parts", FIGCAP_TEST_CASES)
def test_figcap_extension(md_input, expected_parts):
    md = markdown.Markdown(extensions=["mdx_steroids.figcap"])
    html_output = md.convert(md_input)
    print(f"Input MD:\n{md_input}")
    print(f"Output HTML:\n{html_output}")
    for part in expected_parts:
        print(f"Expected part:\n{part}")
        assert part in html_output

    # Also check that if a figure is created, a plain img tag is not also there for the same image
    if (
        "<figure>" in html_output and expected_parts[0] == "<figure>"
    ):  # Test cases where figure is expected
        img_tag_inside_figure = expected_parts[1]
        # Count occurrences of the img tag. It should only be once (inside the figure).
        assert (
            html_output.count(img_tag_inside_figure) == 1
        ), "Image tag should only appear once, inside the figure."
    elif expected_parts[0].startswith("<img"):  # Test cases where only img is expected
        assert "<figure>" not in html_output
        assert "<figcaption>" not in html_output
        assert html_output.count(expected_parts[0]) == 1


# Test to ensure it doesn't break standard image links if title is absent
def test_figcap_no_title_no_figure():
    md_input = "![alt text](image.png)"
    md = markdown.Markdown(extensions=["mdx_steroids.figcap"])
    html_output = md.convert(md_input)
    expected_html = '<p><img alt="alt text" src="image.png" /></p>'
    assert html_output == expected_html
    assert "<figure>" not in html_output
    assert "<figcaption>" not in html_output


def test_figcap_with_title_creates_figure():
    md_input = '![alt text](image.png "My Caption")'
    md = markdown.Markdown(extensions=["mdx_steroids.figcap"])
    html_output = md.convert(md_input)

    assert "<figure>" in html_output
    assert '<img alt="alt text" src="image.png" title="My Caption" />' in html_output
    assert "<figcaption>My Caption</figcaption>" in html_output
    # Ensure the original title on <img> is either preserved or removed.
    # The current figcap.py code seems to leave the title attribute on the <img>.
    # This is acceptable, browsers usually ignore title on img if it's in a figure with figcaption.
    # Let's assert it's there, as per current code.
    assert 'title="My Caption"' in html_output

    # Check that the plain image tag is not duplicated outside the figure
    # This is tricky because the img tag is *part* of the figure.
    # The parametrize test has a check for count.
    # A simpler check: count how many times "src="image.png"" appears.
    assert html_output.count('src="image.png"') == 1
