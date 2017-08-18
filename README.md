# mdx_steroids

A small collection of Python Markdown extensions.

* [mdx_steroids.absimgsrc](#mdx_steroidsabsimgsrc)
* [mdx_steroids.keys](#mdx_steroidskeys)
* [mdx_steroids.kill_tags](#mdx_steroidskill_tags)
* [mdx_steroids.md_mako](#mdx_steroidsmd_mako)
* [mdx_steroids.replimgsrc](#mdx_steroidsreplimgsrc)
* [mdx_steroids.wikilink](#mdx_steroidswikilink)

# Installation

```
pip install --user --upgrade  git+https://github.com/twardoch/markdown-steroids.git
```


# Usage in MkDocs

In your `mkdocs.yaml` include:

```yaml
markdown_extensions:
- mdx_steroids.absimgsrc:
    base_url       : 'https://github.com/repo/blob/master/images/'
    # Base URL to which the relative paths will be appended
- mdx_steroids.keys:
    camel_case: true
    strict: false
    separator: ''
- mdx_steroids.kill_tags:
    kill_known: true
    kill_empty:
      - p
    normalize: false
- mdx_steroids.md_mako:
    python_block  : 'my_md_mako.py'
    meta:
      author: 'John Doe'
- mdx_steroids.meta_yaml
- mdx_steroids.replimgsrc:
    find           : 'https://github.com/repo/blob/master/images'
    replace        : '../img/'
- mdx_steroids.wikilink:
    base_url       : '/'
    end_url        : '/'
    html_class     : 'wikilink'
    space_sep      : '-'
```

----

# mdx_steroids.absimgsrc

The `mdx_steroids.absimgsrc` replaces relative image URLs with absolute ones.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids/

### Options

```yaml
  steroids.absimgsrc:
    base_url       : 'https://github.com/repo/blob/master/images/'
    # Base URL to which the relative paths will be appended
```

### Example

---



---

#### Input Markdown

````markdown
````

#### Output HTML

````html
````

----

# mdx_steroids.keys

The `mdx_steroids.keys` extension converts syntax for user keyboard entry: `++Cmd+K++` into `<kbd>Cmd+K</kbd>`.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids

It wraps the syntax `++key+key+key++` (for individual keystrokes with modifiers)
or `++"string"++` (for continuous keyboard input) into HTML `<kbd>` elements.

If a key is found in the extension's database, its `<kbd>` element gets a matching class.
Common synonyms are included, e.g. `++pg-up++` will match as `++page-up++`.

## Config

If `strict` is `True`, the entire series of keystrokes is wrapped into an outer`<kbd>` element, and then,
each keystroke is wrapped into a separate inner `<kbd>` element, which matches the HTML5 spec.
If `strict` is `False`, an outer `<span>` is used, which matches the practice on Github or StackOverflow.

The resulting `<kbd>` elements are separated by `separator` (`+` by default, can be `''` or something else).

If `camel_case` is `True`, `++PageUp++` will match the same as `++page-up++`.

The database can be extended or modified with the `key_map` dict.

## Examples

### Input

```markdown
Press ++Shift+Alt+PgUp++, type in ++"Hello"++ and press ++Enter++.
```

### Config 1

```yaml
  pymdownx.keys:
    camel_case: true
    strict: false
    separator: '+'
```

### Output 1

```html
<p>Press <span class="keys"><kbd class="key-shift">Shift</kbd><span>+</span><kbd
class="key-alt">Alt</kbd><span>+</span><kbd class="key-page-up">Page Up</kbd></span>, type in <span
class="keys"><kbd>Hello</kbd></span> and press <span class="keys"><kbd class="key-enter">Enter</kbd></span>.</p>
```

### Config 2

```yaml
  pymdownx.keys:
    camel_case: true
    strict: true
    separator: ''
```

### Output 2

```html
<p>Press <kbd class="keys"><kbd class="key-shift">Shift</kbd><kbd class="key-alt">Alt</kbd><kbd
class="key-page-up">Page Up</kbd></kbd>, type in <kbd class="keys"><kbd>Hello</kbd></kbd> and press <kbd
class="keys"><kbd class="key-enter">Enter</kbd></kbd>.</p>
```

----

# mdx_steroids.kill_tags

The `mdx_steroids.kill_tags` removes requested HTML elements from final HTML output.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids

### Options

* The `kill` option allows to specify a list of CSS selectors or (when using the "!" prefix), XPath selectors.
Elements matching to these selectors will be completely removed from the final HTML.

* The `kill_known` option allows to remove (if true) or keep (if false) certain hardcoded selectors.

* The `kill_empty` option allows to specify a list of simple element tags which will be removed if they’re empty.

* The `normalize` option will pass the final HTML through BeautifulSoup if true.

```yaml
  steroids.kill_tags:
    normalize: false  # Do not use BeautifulSoup for post-processing
    kill:             # List of CSS selectors or (with "!" prefix) XPath selectors to delete
      - "!//pre[@class and contains(concat(' ', normalize-space(@class), ' '), ' hilite ') and code[@class and
      contains(concat(' ', normalize-space(@class), ' '), ' language-del ')]]"
      - del
    kill_known: false # Do not remove some hardcoded "known" selectors
    kill_empty:       # List of HTML tags (simple) to be removed if they’re empty
      - p
      - div
```

----

# mdx_steroids.md_mako

The `mdx_steroids.md_mako` feeds Markdown through the Mako templating system.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids

### Options

```yaml
  steroids.md_mako:
    include_base    : '.'        # Default location from which to evaluate relative paths for the `<%include file="..."/>` statement.
    include_encoding: 'utf-8'    # Encoding of the files used by the `<%include file="..."/>` statement.
    include_auto    : 'head.md'  # Path to Mako file to be automatically included at the beginning.
    python_block    : 'head.py'  # Path to Python file to be automatically included at the beginning as a module block. Useful for global imports and functions.
    meta:                        # Dict of args passed to `mako.Template().render()`. Can be overriden through Markdown YAML metadata.
      author        : 'John Doe' # Can be referred inside the Markdown via `${author}`
      status        : 'devel'    # Can be referred inside the Markdown via `${status}`
```

### Example

#### Input Markdown

This assumes that the `meta` or `steroids.meta_yaml` extension is enabled,
so parsing metadata at the beginning of the file works.

```markdown
---
author: John Doe
---
<%!
import datetime
def today():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d')
%>

${author} has last edited this on ${today()}.

% for number in ['one', 'two', 'three']:
* ${number}
% endfor
```

#### Output HTML

```html
<p>John Doe has last edited this on 2017-08-17.</p>
<ul>
<li>one</li>
<li>two</li>
<li>three</li>
</ul>
```

----

# mdx_steroids.replimgsrc

The `mdx_steroids.replimgsrc` extension finds and replaces portions of an image URL.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids/

### Options

```yaml
  steroids.replimgsrc:
    find           : 'https://github.com/repo/blob/master/images/'
    replace        : '../img/'
```

### Example

---



---

#### Input Markdown

```markdown
```

#### Output HTML

```html
```

----

# mdx_steroids.wikilink

The `mdx_steroids.wikilink` extension parses wikilinks in the style of the  [Gollum](https://github.com/gollum/gollum) wiki and the [Github Wiki system](https://help.github.com/articles/about-github-wikis/). It will convert links such as `[[Page name]]` to `[Page name](/Page-name/)`. You can specify the start, end and separator strings.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids

### Options

```yaml
  steroids.wikilink:
    base_url       : '/'                  # String to append to beginning or URL.
    end_url        : '/'                  # String to append to end of URL.
    html_class     : 'wikilink'           # CSS hook. Leave blank for none.
    space_sep      : '-'                  # String that replaces the space, "-" by default.
    build_url      : build_url            # Alternative callable formats URL from label.
```

### Example

---

This is a [[Wiki Link]] of some sorts.

---

#### Input Markdown

```markdown
This is a [[Wiki Link]] of some sorts.
```

#### Output HTML

```html
<p>This is a <a class="wikilink" href="/Wiki-Link/">Wiki Link</a> of some sorts.</p>
```

----

### Copyright and License

* Copyright © 2016 [Adam Twardoch](https://github.com/twardoch)
* Copyright © 2008 [Waylan Limberg](http://achinghead.com) 
* Copyright © 2008-2014 The Python Markdown Project
* Copyright © 2014-2015 Isaac Muse <isaacmuse@gmail.com> 
* License: [BSD 3-Clause License](./LICENSE)

### Projects related to Markdown and MkDocs by Adam Twardoch: 

* [https://twardoch.github.io/markdown-rundown/](https://twardoch.github.io/markdown-rundown/) — summary of Markdown formatting styles [git](https://github.com/twardoch/markdown-rundown)
* [https://twardoch.github.io/markdown-steroids/](https://twardoch.github.io/markdown-steroids/) — Some extensions for Python Markdown [git](https://github.com/twardoch/markdown-steroids)
* [https://twardoch.github.io/markdown-utils/](https://twardoch.github.io/markdown-utils/) — various utilities for working with Markdown-based documents [git](https://github.com/twardoch/markdown-utils)
* [https://twardoch.github.io/mkdocs-combine/](https://twardoch.github.io/mkdocs-combine/) — convert an MkDocs Markdown source site to a single Markdown document [git](https://github.com/twardoch/mkdocs-combine)
* [https://github.com/twardoch/noto-mkdocs-theme/tree/rework](https://github.com/twardoch/noto-mkdocs-theme/tree/rework) — great Material Design-inspired theme for MkDocs [git](https://github.com/twardoch/noto-mkdocs-theme)
* [https://twardoch.github.io/clinker-mktheme/](https://twardoch.github.io/clinker-mktheme/) — great theme for MkDocs [git](https://github.com/twardoch/clinker-mktheme)
