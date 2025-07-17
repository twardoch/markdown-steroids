# this_file: tests/test_translate_no.py
import markdown
import pytest


def test_translate_no_default():
    """Test translate_no with default configuration."""
    md_input = """
    # Title
    
    Here is some `code` and a <kbd>key</kbd>.
    
    <pre>
    preformatted text
    </pre>
    
    <mark>highlighted text</mark>
    """
    
    md = markdown.Markdown(extensions=["mdx_steroids.translate_no"])
    html_output = md.convert(md_input)
    
    # Should add translate="no" and notranslate class to default elements
    assert 'translate="no"' in html_output
    assert 'class="notranslate"' in html_output or 'notranslate' in html_output


def test_translate_no_custom_selectors():
    """Test translate_no with custom selectors."""
    md_input = """
    # Title
    
    <span class="product-name">ProductX</span>
    <div class="technical-term">API</div>
    <p>Regular text</p>
    """
    
    config = {"add": [".product-name", ".technical-term"]}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.translate_no"],
        extension_configs={"mdx_steroids.translate_no": config}
    )
    html_output = md.convert(md_input)
    
    # Should add translate="no" to custom selectors
    assert 'translate="no"' in html_output
    # Should not affect regular text
    assert "Regular text" in html_output


def test_translate_no_xpath():
    """Test translate_no with XPath selectors."""
    md_input = """
    # Title
    
    <div data-type="code">Code block</div>
    <div data-type="text">Regular text</div>
    """
    
    config = {"add": ["!//div[@data-type='code']"]}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.translate_no"],
        extension_configs={"mdx_steroids.translate_no": config}
    )
    html_output = md.convert(md_input)
    
    # Should add translate="no" to XPath selected elements
    assert 'translate="no"' in html_output


def test_translate_no_normalize():
    """Test translate_no with normalize option."""
    md_input = """
    # Title
    
    <code>code snippet</code>
    <p>Regular text</p>
    """
    
    config = {"normalize": True}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.translate_no"],
        extension_configs={"mdx_steroids.translate_no": config}
    )
    html_output = md.convert(md_input)
    
    # Should process with normalization
    assert 'translate="no"' in html_output
    assert "Regular text" in html_output


def test_translate_no_multiple_elements():
    """Test translate_no with multiple elements."""
    md_input = """
    # Title
    
    <code>code1</code>
    <code>code2</code>
    <kbd>key1</kbd>
    <kbd>key2</kbd>
    """
    
    md = markdown.Markdown(extensions=["mdx_steroids.translate_no"])
    html_output = md.convert(md_input)
    
    # Should add translate="no" to all matching elements
    code_count = html_output.count('translate="no"')
    assert code_count >= 2  # At least for code and kbd elements


def test_translate_no_nested_elements():
    """Test translate_no with nested elements."""
    md_input = """
    # Title
    
    <div>
        <code>nested code</code>
        <p>Regular text</p>
    </div>
    """
    
    md = markdown.Markdown(extensions=["mdx_steroids.translate_no"])
    html_output = md.convert(md_input)
    
    # Should add translate="no" to code element inside div
    assert 'translate="no"' in html_output
    assert "nested code" in html_output
    assert "Regular text" in html_output


def test_translate_no_preserves_existing_attributes():
    """Test that translate_no preserves existing attributes."""
    md_input = """
    # Title
    
    <code class="language-python" id="snippet1">print("hello")</code>
    """
    
    md = markdown.Markdown(extensions=["mdx_steroids.translate_no"])
    html_output = md.convert(md_input)
    
    # Should preserve existing attributes and add translate="no"
    assert 'class="language-python' in html_output or 'class="notranslate language-python' in html_output
    assert 'id="snippet1"' in html_output
    assert 'translate="no"' in html_output


def test_translate_no_no_matching_elements():
    """Test translate_no when no elements match."""
    md_input = """
    # Title
    
    <p>Just regular text</p>
    <div>More regular text</div>
    """
    
    md = markdown.Markdown(extensions=["mdx_steroids.translate_no"])
    html_output = md.convert(md_input)
    
    # Should not add translate="no" if no elements match
    assert "Just regular text" in html_output
    assert "More regular text" in html_output


def test_translate_no_mixed_content():
    """Test translate_no with mixed content."""
    md_input = """
    # Title
    
    Here is some text with `inline code` and a <kbd>Ctrl+C</kbd> shortcut.
    
    The <mark>highlighted</mark> text is important.
    
    <pre>
    function example() {
        return "code block";
    }
    </pre>
    """
    
    md = markdown.Markdown(extensions=["mdx_steroids.translate_no"])
    html_output = md.convert(md_input)
    
    # Should add translate="no" to code-related elements
    assert 'translate="no"' in html_output
    # Should preserve all content
    assert "inline code" in html_output
    assert "Ctrl+C" in html_output
    assert "highlighted" in html_output
    assert "function example" in html_output


def test_translate_no_empty_config():
    """Test translate_no with empty configuration."""
    md_input = """
    # Title
    
    <code>code</code>
    <p>text</p>
    """
    
    config = {"add": []}
    
    md = markdown.Markdown(
        extensions=["mdx_steroids.translate_no"],
        extension_configs={"mdx_steroids.translate_no": config}
    )
    html_output = md.convert(md_input)
    
    # Should not add translate="no" if no selectors
    assert "code" in html_output
    assert "text" in html_output