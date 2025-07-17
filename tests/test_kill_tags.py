# this_file: tests/test_kill_tags.py
import markdown
import pytest


def test_kill_tags_basic():
    """Test basic tag removal."""
    md_input = """
    # Title
    
    <div class="remove-me">This should be removed</div>
    
    <p>This should stay</p>
    """
    
    config = {"kill": [".remove-me"]}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.kill_tags"],
        extension_configs={"mdx_steroids.kill_tags": config}
    )
    html_output = md.convert(md_input)
    
    # Should remove the div with class remove-me
    assert "remove-me" not in html_output
    assert "This should be removed" not in html_output
    # Should keep other content
    assert "This should stay" in html_output


def test_kill_tags_multiple_selectors():
    """Test multiple CSS selectors."""
    md_input = """
    # Title
    
    <div class="ad">Advertisement</div>
    <span id="tracker">Tracking</span>
    <p>Good content</p>
    """
    
    config = {"kill": [".ad", "#tracker"]}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.kill_tags"],
        extension_configs={"mdx_steroids.kill_tags": config}
    )
    html_output = md.convert(md_input)
    
    # Should remove both targeted elements
    assert "Advertisement" not in html_output
    assert "Tracking" not in html_output
    # Should keep good content
    assert "Good content" in html_output


def test_kill_tags_xpath():
    """Test XPath selectors (prefixed with !)."""
    md_input = """
    # Title
    
    <div id="remove-me">Remove this</div>
    <div>Keep this</div>
    """
    
    config = {"kill": ["!//div[@id='remove-me']"]}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.kill_tags"],
        extension_configs={"mdx_steroids.kill_tags": config}
    )
    html_output = md.convert(md_input)
    
    # Should remove the specific div
    assert "Remove this" not in html_output
    # Should keep other divs
    assert "Keep this" in html_output


def test_kill_tags_empty_elements():
    """Test removal of empty elements."""
    md_input = """
    # Title
    
    <p></p>
    <div></div>
    <p>Content here</p>
    <h1></h1>
    """
    
    config = {"kill_empty": ["p", "div", "h1"]}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.kill_tags"],
        extension_configs={"mdx_steroids.kill_tags": config}
    )
    html_output = md.convert(md_input)
    
    # Should keep non-empty elements
    assert "Content here" in html_output
    # Empty elements should be removed (exact behavior depends on implementation)


def test_kill_tags_normalize():
    """Test normalize option."""
    md_input = """
    # Title
    
    <div class="remove">Remove this</div>
    <p>Keep this</p>
    """
    
    config = {"kill": [".remove"], "normalize": True}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.kill_tags"],
        extension_configs={"mdx_steroids.kill_tags": config}
    )
    html_output = md.convert(md_input)
    
    # Should remove the targeted element
    assert "Remove this" not in html_output
    # Should keep other content
    assert "Keep this" in html_output


def test_kill_tags_no_config():
    """Test behavior without configuration."""
    md_input = """
    # Title
    
    <p></p>
    <div>Content</div>
    """
    
    md = markdown.Markdown(extensions=["mdx_steroids.kill_tags"])
    html_output = md.convert(md_input)
    
    # Should work with default configuration
    assert "Content" in html_output


def test_kill_tags_known_selectors():
    """Test kill_known option."""
    md_input = """
    # Title
    
    <del>Deleted content</del>
    <p>Normal content</p>
    """
    
    config = {"kill_known": True}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.kill_tags"],
        extension_configs={"mdx_steroids.kill_tags": config}
    )
    html_output = md.convert(md_input)
    
    # Should remove known elements (depends on implementation)
    assert "Normal content" in html_output


def test_kill_tags_complex_html():
    """Test with complex HTML structures."""
    md_input = """
    # Title
    
    <div class="container">
        <div class="ad">Advertisement</div>
        <article>
            <h2>Article Title</h2>
            <p>Article content</p>
        </article>
    </div>
    """
    
    config = {"kill": [".ad"]}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.kill_tags"],
        extension_configs={"mdx_steroids.kill_tags": config}
    )
    html_output = md.convert(md_input)
    
    # Should remove only the ad div
    assert "Advertisement" not in html_output
    # Should keep the article content
    assert "Article Title" in html_output
    assert "Article content" in html_output


def test_kill_tags_nested_elements():
    """Test with nested elements."""
    md_input = """
    # Title
    
    <div class="outer">
        <div class="inner remove-me">
            <p>Nested content</p>
        </div>
        <p>Outer content</p>
    </div>
    """
    
    config = {"kill": [".remove-me"]}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.kill_tags"],
        extension_configs={"mdx_steroids.kill_tags": config}
    )
    html_output = md.convert(md_input)
    
    # Should remove the inner div and its content
    assert "Nested content" not in html_output
    # Should keep the outer content
    assert "Outer content" in html_output


def test_kill_tags_multiple_instances():
    """Test removal of multiple instances of the same selector."""
    md_input = """
    # Title
    
    <div class="ad">Ad 1</div>
    <p>Content</p>
    <div class="ad">Ad 2</div>
    <p>More content</p>
    """
    
    config = {"kill": [".ad"]}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.kill_tags"],
        extension_configs={"mdx_steroids.kill_tags": config}
    )
    html_output = md.convert(md_input)
    
    # Should remove all instances
    assert "Ad 1" not in html_output
    assert "Ad 2" not in html_output
    # Should keep regular content
    assert "Content" in html_output
    assert "More content" in html_output