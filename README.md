```markdown
# mdx-steroids

**mdx-steroids** is a versatile collection of Python Markdown extensions designed to supercharge your Markdown processing workflow. It provides a suite of enhancements for fine-grained control over HTML output, enabling features like absolute image paths, figure captions, dynamic content with Mako, keyboard key styling, wikilinks, and much more, directly within your Markdown files.

This library is ideal for developers, technical writers, and content creators using Python-based Markdown rendering pipelines, especially with static site generators like MkDocs or custom Python scripts.

## Key Features

*   **Extensible:** Adds a rich set of features not available in standard Markdown.
*   **Customizable:** Most extensions offer configuration options to tailor their behavior to your specific needs.
*   **Seamless Integration:** Designed to work smoothly with the core `Python-Markdown` library and tools like MkDocs.
*   **Wide Range of Functionality:**
    *   Image handling: absolute paths, responsive attributes, figure captions, URL replacement.
    *   Content generation: Mako templating for dynamic content, YAML front matter parsing.
    *   Utility: Tag removal, comment stripping, non-translatable content marking.
    *   Formatting: Keyboard key styling, wikilinks.

## Installation

Install `mdx-steroids` directly from GitHub using pip:

```bash
pip install git+https://github.com/twardoch/markdown-steroids.git
```

**Requirements:**

*   Python >= 3.8
*   Core dependencies (automatically installed):
    *   `markdown>=3.5.0`
    *   `mako>=1.0.7`
    *   `pymdown-extensions>=9.0`
    *   `cssselect>=1.0.1`
    *   `lxml>=3.8.0`
    *   `beautifulsoup4>=4.6.0`
*   Some extensions may require additional dependencies (e.g., `filetype`, `imageio` for `img_smart`). For a full development setup, you might want to consult `py-requirements.txt`.

## General Usage

`mdx-steroids` extensions can be used with `Python-Markdown` directly or configured within tools like MkDocs.

### With Python-Markdown

You can use `mdx-steroids` extensions programmatically in your Python scripts:

```python
import markdown

markdown_text = """
This is a [[Sample Wikilink]].
Press ++Ctrl+S++ to save.
<!--- This comment will be stripped. -->
![An image](image.png "A nice caption for the image.")
"""

# Basic usage
html_output = markdown.markdown(
    markdown_text,
    extensions=[
        'mdx_steroids.wikilink',
        'mdx_steroids.keys',
        'mdx_steroids.comments',
        'mdx_steroids.figcap'
    ]
)
print(html_output)

# Usage with configuration
html_configured_output = markdown.markdown(
    markdown_text,
    extensions=['mdx_steroids.wikilink', 'mdx_steroids.keys'],
    extension_configs={
        'mdx_steroids.wikilink': {
            'base_url': '/wiki/',
            'end_url': '.html'
        },
        'mdx_steroids.keys': {
            'separator': ' + '
        }
    }
)
print(html_configured_output)
```

### With Python-Markdown CLI

You can use `Python-Markdown`'s CLI to process files with `mdx-steroids` extensions. First, create a configuration file (e.g., `config.yml`):

```yaml
# config.yml
mdx_steroids.wikilink:
  base_url: '/wiki/'
  end_url: '/'
mdx_steroids.keys:
  strict: true
```

Then run the command:

```bash
python -m markdown -x mdx_steroids.wikilink -x mdx_steroids.keys -c config.yml input.md -f output.html
```

### With MkDocs

Integrate `mdx-steroids` into your MkDocs project by adding the extensions to your `mkdocs.yml`:

```yaml
# mkdocs.yml
site_name: My Awesome Documentation

markdown_extensions:
  - mdx_steroids.absimgsrc:
      base_url: 'https://cdn.example.com/images/'
  - mdx_steroids.figcap
  - mdx_steroids.keys:
      camel_case: true
      separator: ' '
  - mdx_steroids.wikilink:
      base_url: '/docs/'
      end_url: '/'
  - mdx_steroids.comments
  # Add other extensions and their configurations as needed
```

## Available Extensions

Below is a list of available extensions, their purpose, and configuration options.

---

### 1. `mdx_steroids.absimgsrc`

*   **Description:** Replaces relative image URLs with absolute ones by prepending a `base_url`. Useful for ensuring images load correctly regardless of the page's location or when hosting assets on a CDN.
*   **Markdown Syntax:** Standard `![alt text](relative/path/image.png)`
*   **Configuration:**
    *   `base_url` (str): The base URL to prepend. Default: `None`.
*   **MkDocs Example:**
    ```yaml
    markdown_extensions:
      - mdx_steroids.absimgsrc:
          base_url: 'https://your-cdn.com/assets/images/'
    ```

---

### 2. `mdx_steroids.comments`

*   **Description:** Removes special HTML-like comments `<!--- ... -->` from the output. Standard HTML comments `<!-- ... -->` are preserved. This helps in leaving notes in Markdown that won't make it to the final HTML.
*   **Markdown Syntax:** `<!--- This is a strippable comment. -->`
*   **Configuration:** None.
*   **MkDocs Example:**
    ```yaml
    markdown_extensions:
      - mdx_steroids.comments
    ```

---

### 3. `mdx_steroids.figcap`
*   **Author:** mszk (forked)
*   **Description:** Converts Markdown images with a title attribute (e.g., `![alt text](image.png "Caption text")`) into an HTML5 `<figure>` element containing the `<img>` and a `<figcaption>` with the caption text.
*   **Markdown Syntax:** `![Alternative text for image](path/to/image.png "This text becomes the figcaption")`
*   **Configuration:** None.
*   **MkDocs Example:**
    ```yaml
    markdown_extensions:
      - mdx_steroids.figcap
    ```
*   **Note:** The original documentation mentions this extension might be broken with Python 3. Please test thoroughly.

---

### 4. `mdx_steroids.img_smart`

*   **Description:** Provides advanced image processing capabilities. It can automatically determine image dimensions, replace parts of image URLs, add `loading="lazy"` attributes, wrap images in links (e.g., for lightboxes like Fancybox), and generate `<figure>`/`<figcaption>` from alt text. It supports caching image metadata to speed up processing on subsequent builds.
*   **Markdown Syntax:** Standard image syntax `![alt text](path/image.png){: width=300 .css-class }`. Attributes can be added using the `attr_list` syntax.
*   **Configuration:**
    *   `find` (str): A string to find in the image URL. Default: `""`.
    *   `repl_path` (str): A string to replace the found part for local path resolution. Default: `""`.
    *   `repl_url` (str): A string to replace the found part for the final `src` URL. Default: `""`.
    *   `alt_figure` (bool): If `True`, uses the image `alt` text to create a `<figcaption>`. Default: `False`.
    *   `cache` (str): Path to a JSON file for caching image metadata (e.g., `.img_cache.json`). Default: `""`.
    *   `lazy` (bool): If `True`, adds `loading="lazy"` attribute to `<img>` tags. Default: `False`.
*   **MkDocs Example:**
    ```yaml
    markdown_extensions:
      - mdx_steroids.img_smart:
          find: '/src/images'
          repl_url: '/assets/img'
          alt_figure: true
          cache: '.img_metadata_cache.json'
          lazy: true
    ```

---

### 5. `mdx_steroids.interlink`

*   **Description:** Preprocesses internal Markdown links `[text](some-link#anchor)`. If a link does not contain a protocol (`://`) or a period (`.`), it can automatically prepend a `base_url` and append an `end_url`. This is useful for managing internal links within a site structure.
*   **Markdown Syntax:** `[Link Text](internal-page-slug)`
*   **Configuration:**
    *   `base_url` (str): String to prepend to relative link URLs. Default: `""`.
    *   `end_url` (str): String to append to relative link URLs (before any `#anchor`). Default: `""`.
*   **MkDocs Example:**
    ```yaml
    markdown_extensions:
      - mdx_steroids.interlink:
          base_url: '/documentation/'
          end_url: '/' # Turns 'my-page' into '/documentation/my-page/'
    ```

---

### 6. `mdx_steroids.keys` (and `mdx_steroids.kbd`)

*   **Original Idea:** Adam Twardoch
*   **Original Code:** Isaac Muse (for `pymdownx.keys`, forked)
*   **Description:** Formats textual representations of keyboard shortcuts (e.g., `++Ctrl+S++` or `++"type this phrase"++`) into stylable HTML `<kbd>` elements. It uses a keymap for consistent rendering and supports aliases. `mdx_steroids.kbd` is an alias for this extension.
*   **Markdown Syntax:** `++Key1+Key2++` for key combinations, or `++"Literal string"++` for typed text.
*   **Configuration:**
    *   `separator` (str): Character(s) to display between key names in the output. Default: `'+'`.
    *   `strict` (bool): If `True`, wraps individual keys in `<kbd>` tags within an outer `<kbd>` tag (HTML5 spec). If `False` (default), uses a `<span>` as the outer wrapper for better styling flexibility in some contexts.
    *   `class` (str): CSS class(es) for the main wrapper element. Default: `"keys"`.
    *   `camel_case` (bool): If `True`, allows `++CamelCaseKey++` to be interpreted as `++camel-case-key++`. Default: `False`.
    *   `key_map` (dict): A custom dictionary to extend or override the default key map definitions. Default: `{}`.
*   **MkDocs Example:**
    ```yaml
    markdown_extensions:
      - mdx_steroids.keys:
          camel_case: true
          strict: false # Uses <span> wrapper
          separator: ' + ' # e.g., Shift + Alt + K
    ```

---

### 7. `mdx_steroids.kill_tags`

*   **Description:** Removes specified HTML elements from the final rendered HTML using CSS or XPath selectors. It can also remove tags that are empty (contain no text or other elements). Useful for cleaning up generated HTML or removing unwanted content.
*   **Markdown Syntax:** No specific Markdown syntax; operates on the generated HTML output.
*   **Configuration:**
    *   `normalize` (bool): If `True`, normalizes the HTML using BeautifulSoup before and after processing. Default: `False`.
    *   `kill` (list): A list of CSS selectors. Elements matching these selectors will be completely removed. Prefix with `!` for XPath selectors (e.g., `"!//div[@id='remove-me']"`). Default: `[]`.
    *   `kill_known` (bool): If `True`, also removes some predefined "known" selectors (e.g., for `<del>` tags or specific code block classes used for deletion). Default: `False`.
    *   `kill_empty` (list): A list of simple HTML tag names (e.g., `p`, `div`) that will be removed if they are empty (no text content and no child elements with content or attributes). Default: `["p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "pre"]`.
*   **MkDocs Example:**
    ```yaml
    markdown_extensions:
      - mdx_steroids.kill_tags:
          kill:
            - '.advertisement-banner' # CSS selector
            - '!//figure[not(img)]'   # XPath selector
          kill_empty: ['span', 'p', 'div']
          normalize: true # Recommended if complex HTML is involved
    ```

---

### 8. `mdx_steroids.md_mako`

*   **Description:** Processes the Markdown content through the Mako templating engine before standard Markdown parsing. This allows embedding dynamic content, variables, loops, and includes using Mako syntax and Python logic.
*   **Markdown Syntax:** Utilizes Mako template syntax (e.g., `${variable}`, `<% ... %>`, `% for item in items: ... % endfor`).
*   **Configuration:**
    *   `include_base` (str or list): Base directory or list of directories for Mako's `<%include file="..."/>` statement. Default: `'.'`.
    *   `include_encoding` (str): Encoding for files included via Mako. Default: `'utf-8'`.
    *   `include_auto` (str): Path to a Mako template file to be automatically included at the beginning of every Markdown file processed. Default: `""`.
    *   `python_block` (str): Path to a Python file whose content will be automatically included as a Mako module-level block (`<%! ... %>`). Useful for defining global helper functions and imports accessible to Mako templates. Default: `""`.
    *   `meta` (dict): A dictionary of arguments passed to `mako.Template().render()`. These can be accessed as variables in Mako templates. Values here can be overridden by Markdown YAML front matter if `mdx_steroids.meta_yaml` (or a similar meta extension) is also used. Default: `{}`.
*   **MkDocs Example:**
    ```yaml
    # mkdocs.yml
    markdown_extensions:
      - mdx_steroids.meta_yaml # Often used with md_mako
      - mdx_steroids.md_mako:
          include_base: 'docs/_includes/' # For Mako <%include ...%>
          python_block: 'docs/_helpers/macros.py' # For global Mako functions
          meta:
            site_version: '2.0.1'
            current_year: 2024
    ```
    ```python
    # docs/_helpers/macros.py
    import datetime

    def get_current_year():
        return datetime.date.today().year
    ```
    ```markdown
    # In your Markdown file:
    ---
    author: Jane Doe
    ---
    Page author: ${author}
    Site version: ${site_version}
    Current year: ${get_current_year()}

    <%include file="notice.md"/>
    ```

---

### 9. `mdx_steroids.meta_yaml`

*   **Author:** Bernhard Fisseni (forked)
*   **Description:** Parses YAML front matter (metadata) at the beginning of a Markdown document. The parsed metadata is stored in the `markdown.Markdown` instance's `Meta` attribute (e.g., `md.Meta`). This is commonly used by static site generators and other tools to pass page-specific data.
*   **Markdown Syntax:** A block of YAML enclosed by `---` at the start and `---` or `...` at the end of the block, placed at the very beginning of the file.
    ```markdown
    ---
    title: My Awesome Page
    author: Alex Doe
    tags: [python, markdown, example]
    custom_data:
      key: value
    ---

    This is the main content of the page.
    ```
*   **Configuration:** None.
*   **MkDocs Example:**
    ```yaml
    markdown_extensions:
      - mdx_steroids.meta_yaml
    ```
*   **Note:** The original documentation mentions this extension might be broken with Python 3. Please test thoroughly.

---

### 10. `mdx_steroids.replimgsrc`

*   **Description:** Performs a simple find-and-replace operation on the `src` attribute of `<img>` tags. This is a straightforward way to batch-update image paths.
*   **Markdown Syntax:** Standard image syntax. Operates on the `src` attribute of the generated `<img>` tag.
*   **Configuration:**
    *   `find` (str): The string to search for in image `src` attributes.
    *   `replace` (str): The string to replace the found occurrences with.
*   **MkDocs Example:**
    ```yaml
    markdown_extensions:
      - mdx_steroids.replimgsrc:
          find: 'http://old-domain.com/images/'
          replace: '/assets/migrated-images/'
    ```

---

### 11. `mdx_steroids.translate_no`

*   **Description:** Adds the `translate="no"` attribute and a `notranslate` CSS class to specified HTML elements. This signals to browser translation tools (like Google Translate) that the content of these elements should not be translated.
*   **Markdown Syntax:** No specific Markdown syntax; operates on the generated HTML.
*   **Configuration:**
    *   `normalize` (bool): If `True`, normalizes the HTML using BeautifulSoup before and after processing. Default: `False`.
    *   `add` (list): A list of CSS selectors. Elements matching these selectors will get `translate="no"` and class `notranslate`. Prefix with `!` for XPath selectors. Default: `["code", "mark", "pre", "kbd"]`.
*   **MkDocs Example:**
    ```yaml
    markdown_extensions:
      - mdx_steroids.translate_no:
          add: ['code', 'pre', 'kbd', '.product-name', '.technical-term']
    ```

---

### 12. `mdx_steroids.wikilink`

*   **Description:** Converts Gollum/GitHub-style wiki links (e.g., `[[Page Name]]`) into standard Markdown links. It can automatically generate URLs by slugifying the page name and prepending/appending specified URL parts.
*   **Markdown Syntax:** `[[My Wiki Page]]` or `[[Another Page | Link Text]]` (though the latter form's pipe behavior might depend on interaction with other link processors; primarily `[[Page Name]]` is supported by this extension directly for URL generation).
*   **Configuration:**
    *   `base_url` (str): String to prepend to the generated link URL slug. Default: `'/'`.
    *   `end_url` (str): String to append to the generated link URL slug. Default: `'/'`.
    *   `html_class` (str): CSS class to attempt to add to the generated `<a>` tag. Note: As this is a preprocessor, the final HTML generation is handled by Markdown's link patterns, so class application might not be direct. Default: `'wikilink'`.
    *   `space_sep` (str): Character used to replace spaces in page names when generating the URL slug. Default: `'-'`.
*   **MkDocs Example:**
    ```yaml
    markdown_extensions:
      - mdx_steroids.wikilink:
          base_url: '/wiki/'       # Results in /wiki/Page-Name/
          end_url: '/'
          space_sep: '-'
    ```
    ```yaml
    markdown_extensions:
      - mdx_steroids.wikilink:
          base_url: '/kb/'
          end_url: '.page'      # Results in /kb/Page_Name.page
          space_sep: '_'
    ```

## Technical Overview

`mdx-steroids` is a collection of pluggable extensions for the widely-used `Python-Markdown` library. Each extension is typically a Python class inheriting from `markdown.Extension`. These extensions hook into various stages of the Markdown processing pipeline:

*   **Preprocessors:** Modify the raw Markdown text before any parsing occurs (e.g., `md_mako`, `wikilink`, `comments`, `interlink`).
*   **Block Processors:** Handle multi-line blocks of text (e.g., `img_smart`).
*   **Inline Processors:** Handle patterns within blocks of text, like emphasis or links (e.g., `keys`, `figcap`).
*   **Tree Processors:** Manipulate the ElementTree (an XML-like structure) after the HTML structure is built but before serialization (e.g., `absimgsrc`, `replimgsrc`).
*   **Postprocessors:** Modify the final HTML output string after it has been serialized from the ElementTree (e.g., `kill_tags`, `translate_no`).

This modular architecture allows `mdx-steroids` to provide diverse functionalities by targeting the most appropriate stage of conversion.

## Contributing

Contributions are welcome! Whether it's bug reports, feature suggestions, or code contributions, please feel free to engage with the project.

### Development Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/twardoch/markdown-steroids.git
    cd markdown-steroids
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
    ```
3.  **Install dependencies:**
    For basic usage and testing the core package:
    ```bash
    pip install -e .
    ```
    For development, including all tools and optional dependencies for all extensions:
    ```bash
    pip install -r py-requirements.txt
    ```
    (You might also need to install `pytest`, `black`, `flake8` separately if not in `py-requirements.txt`: `pip install pytest black flake8`)

### Coding Standards

*   **Formatting:** This project uses [Black](https://github.com/psf/black) for code formatting. Please format your code by running `black .` before committing. Configuration is in `pyproject.toml`.
*   **Linting:** [Flake8](https://flake8.pycqa.org/en/latest/) is used for linting. Check your code with `flake8 .`. Configuration is in `.flake8`.

### Running Tests

Tests are written using `pytest`. Run them from the project root:

```bash
pytest
```
Test configurations can be found in `pyproject.toml` and `pytest.ini`.

### Submitting Changes

1.  Fork the repository on GitHub.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes, ensuring code is formatted and linted, and tests pass.
4.  Write clear commit messages.
5.  Push your branch to your fork.
6.  Open a pull request against the main `markdown-steroids` repository. Provide a clear description of your changes.

### Reporting Issues

If you encounter any bugs or have suggestions for new features, please open an issue on the [GitHub Issues page](https://github.com/twardoch/markdown-steroids/issues).

## License

`mdx-steroids` is licensed under the **BSD 3-Clause License**. See the [LICENSE](LICENSE) file for the full text.

This project incorporates or is based on code from several sources, and their respective licenses are compatible with the BSD 3-Clause License. Copyright notices for these are also included in the LICENSE file.

## Acknowledgements

*   **Adam Twardoch:** Primary author and maintainer.
*   **Isaac Muse:** Original author of `pymdownx.keys`, which `mdx_steroids.keys` is based on.
*   **mszk:** Original author of `mdx_figcap`, which `mdx_steroids.figcap` is based on.
*   **Bernhard Fisseni:** Original author of the YAML meta-data extension, which `mdx_steroids.meta_yaml` is based on.
*   The **Python Markdown Project** and its contributors for the core library.
*   All other contributors to the `markdown-steroids` project and the projects it derives from.

---

This `README.md` was last updated on ${today_date}. <!-- You might want a Mako variable or similar if this README itself is processed -->
If you find it helpful, consider starring the project on GitHub!
```
