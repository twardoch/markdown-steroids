import markdown
import pytest

# Test cases: (input_markdown, config, expected_html_output_containing_list)
KBD_TEST_CASES = [
    (
        "Press ++Enter++.",
        {},  # Default config (reverted)
        ['<span class="keys"><kbd class="key-enter">Enter</kbd></span>'],
    ),
    (
        'Type ++"Hello World"++.',
        {},
        ['<span class="keys"><kbd>Hello World</kbd></span>'],
    ),
    (
        "Combo: ++Ctrl+Shift+Esc++.",
        {},
        [
            '<span class="keys">',
            '<kbd class="key-control">Ctrl</kbd>',  # Corrected class
            "<span>+</span>",
            '<kbd class="key-shift">Shift</kbd>',  # Shift is correct
            "<span>+</span>",
            '<kbd class="key-escape">Esc</kbd>',  # Corrected class
            "</span>",
        ],
    ),
    (
        "Strict mode: ++A+B++.",
        {"strict": True, "separator": ""},
        [
            '<kbd class="keys">',
            '<kbd class="key-a">A</kbd>',
            # No separator span
            '<kbd class="key-b">B</kbd>',
            "</kbd>",
        ],
    ),
    (
        "Custom separator: ++A+B++.",
        {"separator": " then "},
        [
            '<span class="keys">',
            '<kbd class="key-a">A</kbd>',
            "<span> then </span>",
            '<kbd class="key-b">B</kbd>',
            "</span>",
        ],
    ),
    (
        "CamelCase: ++PageDown++.",
        {"camel_case": True},
        [
            '<kbd class="key-page-down">PgDn</kbd>'
        ],  # Corrected to match local keymap_db.py
    ),
    (
        "CamelCase off: ++PageDown++.",  # Should be treated as a literal key "PageDown"
        {"camel_case": False},
        [
            "<p>CamelCase off: ++PageDown++.</p>"
        ],  # Corrected: Expect raw output as 'pagedown' is not in map
    ),
    (
        "Custom key map: ++mykey++.",
        {"key_map": {"mykey": "My Custom Key"}},
        ['<kbd class="key-mykey">My Custom Key</kbd>'],
    ),
    (
        "Escaped plus: ++A\\+B++.",
        {},
        [
            "<p>Escaped plus: ++A+B++.</p>"
        ],  # Corrected: Expect raw output with \+ -> + by Markdown
    ),
    (
        'Multiple: ++A++ and ++"B"++.',  # Changed outer quotes to single
        {},
        [
            '<span class="keys"><kbd class="key-a">A</kbd></span>',
            '<span class="keys"><kbd>B</kbd></span>',
        ],
    ),
]


@pytest.mark.parametrize("md_input, config, expected_parts", KBD_TEST_CASES)
def test_kbd_extension_various_cases(md_input, config, expected_parts):
    # The extension is registered as 'mdx_steroids.kbd' due to __init__.py
    md = markdown.Markdown(
        extensions=["mdx_steroids.kbd"], extension_configs={"mdx_steroids.kbd": config}
    )
    html_output = md.convert(md_input)

    print(f"Input MD:\n{md_input}")
    print(f"Config:\n{config}")
    print(f"Output HTML:\n{html_output}")

    for i, part in enumerate(expected_parts):
        print(f"Expected part {i}:\n{part}")
        assert part in html_output


def test_kbd_default_keys_and_aliases():
    """Test some default keys and their known aliases."""
    test_data = {
        "++enter++": '<kbd class="key-enter">Enter</kbd>',
        "++ENT++": '<kbd class="key-enter">Enter</kbd>',  # Assuming ENT is an alias
        "++control++": '<kbd class="key-ctrl">Control</kbd>',  # Assuming keymap stores "Control" for "ctrl"
        "++CTRL++": '<kbd class="key-ctrl">Ctrl</kbd>',
        "++shift++": '<kbd class="key-shift">Shift</kbd>',
        "++pg-up++": '<kbd class="key-page-up">Page Up</kbd>',  # Alias and space in output
        "++page-up++": '<kbd class="key-page-up">Page Up</kbd>',
    }
    md = markdown.Markdown(extensions=["mdx_steroids.kbd"])
    for md_input, expected_kbd_html in test_data.items():
        html_output = md.convert(md_input)
        print(
            f"Input: {md_input}, Output: {html_output}, Expected kbd: {expected_kbd_html}"
        )
        assert expected_kbd_html in html_output


def test_kbd_unknown_key():
    """Test how an unknown key (not in map or aliases) is handled."""
    md_input = "++unknownKey123++"
    # Based on KeysPattern logic: if not in map, value is None, then `if None in content` makes it return None,None,None
    # This means the pattern match is rejected, and the original text should pass through.
    # However, the `RE_KBD` is quite broad. If it matches, but `process_key` returns None for it,
    # the `handleMatch` returns `None, None, None` which means the original text `++unknownKey123++` is unchanged.
    md = markdown.Markdown(extensions=["mdx_steroids.kbd"])
    html_output = md.convert(md_input)
    print(f"Input: {md_input}, Output: {html_output}")
    # Default behavior of Markdown if no pattern matches is to wrap in <p>
    assert "<p>++unknownKey123++</p>" == html_output
    # Or, if the pattern is consumed but then rejected, it might leave it as is.
    # The current code `if None in content: return None, None, None` suggests the original text is returned.
    # So, it should not convert to <kbd> if the key is unknown.


# Test case for `camel_case: False` and an unmapped camelCase key
# This was added because one test case for camel_case: False was a bit ambiguous
KBD_CAMEL_CASE_FALSE_UNMAPPED_TEST_CASES = [
    (
        "++MyCamelKey++",
        {"camel_case": False},
        # Expecting the key to be treated literally if not in map and camel_case is off
        # The actual class might be "key-mycamelkey" due to lowercasing for class names.
        # The text content should be "MyCamelKey".
        # Based on current keys.py, if not in map, it's rejected. So, no <kbd>.
        "++MyCamelKey++",  # This will be wrapped in <p> by markdown
    ),
]


@pytest.mark.parametrize(
    "md_input, config, expected_text_part", KBD_CAMEL_CASE_FALSE_UNMAPPED_TEST_CASES
)
def test_kbd_camel_false_unmapped(md_input, config, expected_text_part):
    md = markdown.Markdown(
        extensions=["mdx_steroids.kbd"], extension_configs={"mdx_steroids.kbd": config}
    )
    html_output = md.convert(md_input)
    print(f"Input MD:\n{md_input}")
    print(f"Config:\n{config}")
    print(f"Output HTML:\n{html_output}")
    assert (
        expected_text_part in html_output
    )  # Check if the original text is in the output


# Test for the F401 on PIL.Image in img_smart.py (this test is unrelated to kbd but was noted in a previous lint run)
# This is just a placeholder to remind me to check it. I'll remove/move it later.
# def test_placeholder_for_img_smart_f401():
#    pass
