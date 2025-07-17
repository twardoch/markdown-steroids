# this_file: tests/test_comments.py
import markdown
import pytest


TEST_CASES = [
    (
        "This is text with <!--- hidden comment --> and more text.",
        "<p>This is text with  and more text.</p>",
    ),
    (
        "Standard comment <!-- visible --> stays.",
        "<p>Standard comment <!-- visible --> stays.</p>",
    ),
    (
        "Multiple <!--- first --> comments <!--- second --> here.",
        "<p>Multiple  comments  here.</p>",
    ),
    (
        "Text\n<!--- multiline\ncomment -->\nmore text.",
        "<p>Text\n\nmore text.</p>",
    ),
    (
        "No comments here.",
        "<p>No comments here.</p>",
    ),
    (
        "<!--- comment at start --> text",
        "<p> text</p>",
    ),
    (
        "text <!--- comment at end -->",
        "<p>text </p>",
    ),
]


@pytest.mark.parametrize("md_input, expected_html", TEST_CASES)
def test_comments_extension(md_input, expected_html):
    """Test comments extension removes <!--- ... --> comments."""
    md = markdown.Markdown(extensions=["mdx_steroids.comments"])
    html_output = md.convert(md_input)
    assert html_output == expected_html


def test_comments_preserves_standard_comments():
    """Test that standard HTML comments are preserved."""
    md_input = "Text with <!-- standard comment --> here."
    expected = "<p>Text with <!-- standard comment --> here.</p>"
    
    md = markdown.Markdown(extensions=["mdx_steroids.comments"])
    html_output = md.convert(md_input)
    assert html_output == expected


def test_comments_mixed_types():
    """Test mixing standard and special comments."""
    md_input = "Text <!-- keep --> and <!--- remove --> here."
    expected = "<p>Text <!-- keep --> and  here.</p>"
    
    md = markdown.Markdown(extensions=["mdx_steroids.comments"])
    html_output = md.convert(md_input)
    assert html_output == expected


def test_comments_nested():
    """Test nested or malformed comments."""
    md_input = "Text <!--- outer <!-- inner --> outer --> here."
    
    md = markdown.Markdown(extensions=["mdx_steroids.comments"])
    html_output = md.convert(md_input)
    
    # Should remove the special comment
    assert "<!---" not in html_output
    assert "--->" not in html_output