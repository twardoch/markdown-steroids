# this_file: tests/test_replimgsrc.py
import markdown
import pytest


TEST_CASES = [
    (
        "![alt text](http://old-domain.com/images/photo.jpg)",
        {"find": "http://old-domain.com/images/", "replace": "/assets/images/"},
        '<img alt="alt text" src="/assets/images/photo.jpg" />',
    ),
    (
        "![alt text](relative/path/image.png)",
        {"find": "relative/path/", "replace": "/static/"},
        '<img alt="alt text" src="/static/image.png" />',
    ),
    (
        "![alt text](image.jpg)",
        {"find": "image.jpg", "replace": "new-image.jpg"},
        '<img alt="alt text" src="new-image.jpg" />',
    ),
    (
        "![alt text](no-match.png)",
        {"find": "other.png", "replace": "replacement.png"},
        '<img alt="alt text" src="no-match.png" />',
    ),
    (
        "![alt text](path/image.png) and ![alt text](path/other.png)",
        {"find": "path/", "replace": "newpath/"},
        '<img alt="alt text" src="newpath/image.png" />',
    ),
    (
        "![alt text](image.png)",
        {"find": "", "replace": "prefix-"},
        '<img alt="alt text" src="prefix-image.png" />',
    ),
]


@pytest.mark.parametrize("md_input, config, expected_part", TEST_CASES)
def test_replimgsrc_extension(md_input, config, expected_part):
    """Test replimgsrc extension performs find/replace on image src."""
    md = markdown.Markdown(
        extensions=["mdx_steroids.replimgsrc"],
        extension_configs={"mdx_steroids.replimgsrc": config}
    )
    html_output = md.convert(md_input)
    assert expected_part in html_output


def test_replimgsrc_multiple_images():
    """Test replimgsrc with multiple images."""
    md_input = """
    ![Image 1](old/path/img1.jpg)
    ![Image 2](old/path/img2.png)
    ![Image 3](different/path/img3.gif)
    """
    config = {"find": "old/path/", "replace": "new/location/"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.replimgsrc"],
        extension_configs={"mdx_steroids.replimgsrc": config}
    )
    html_output = md.convert(md_input)
    
    # Should replace in matching images
    assert "new/location/img1.jpg" in html_output
    assert "new/location/img2.png" in html_output
    # Should not replace in non-matching images
    assert "different/path/img3.gif" in html_output


def test_replimgsrc_with_title():
    """Test replimgsrc preserves image title."""
    md_input = '![alt text](old/image.jpg "Image Title")'
    config = {"find": "old/", "replace": "new/"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.replimgsrc"],
        extension_configs={"mdx_steroids.replimgsrc": config}
    )
    html_output = md.convert(md_input)
    
    assert 'src="new/image.jpg"' in html_output
    assert 'title="Image Title"' in html_output


def test_replimgsrc_no_config():
    """Test replimgsrc behavior without configuration."""
    md_input = "![alt text](image.jpg)"
    
    # Should handle gracefully if no config provided
    md = markdown.Markdown(extensions=["mdx_steroids.replimgsrc"])
    html_output = md.convert(md_input)
    
    # Should not change anything if no find/replace specified
    assert 'src="image.jpg"' in html_output


def test_replimgsrc_empty_find():
    """Test replimgsrc with empty find string."""
    md_input = "![alt text](image.jpg)"
    config = {"find": "", "replace": "prefix-"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.replimgsrc"],
        extension_configs={"mdx_steroids.replimgsrc": config}
    )
    html_output = md.convert(md_input)
    
    # Empty find should match and prepend to all src attributes
    assert 'src="prefix-image.jpg"' in html_output


def test_replimgsrc_case_sensitive():
    """Test replimgsrc is case sensitive."""
    md_input = "![alt text](Image.JPG)"
    config = {"find": "image.jpg", "replace": "new.jpg"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.replimgsrc"],
        extension_configs={"mdx_steroids.replimgsrc": config}
    )
    html_output = md.convert(md_input)
    
    # Should not replace due to case mismatch
    assert 'src="Image.JPG"' in html_output


def test_replimgsrc_special_characters():
    """Test replimgsrc with special characters."""
    md_input = "![alt text](path/image (1).jpg)"
    config = {"find": "path/", "replace": "new-path/"}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.replimgsrc"],
        extension_configs={"mdx_steroids.replimgsrc": config}
    )
    html_output = md.convert(md_input)
    
    assert 'src="new-path/image (1).jpg"' in html_output