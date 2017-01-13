# mdx_steroids

A small collection of Python Markdown extensions


## steroids.wikilink

The `steroids.wikilink` extension parses wikilinks in the style of the  [Gollum](https://github.com/gollum/gollum) wiki and the [Github Wiki system](https://help.github.com/articles/about-github-wikis/). It will convert links such as `[[Page name]]` to `[Page name](/Page-name/)`. You can specify the start, end and separator strings.

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

````markdown
This is a [[Wiki Link]] of some sorts. 
````

#### Output HTML

````html
<p>This is a <a class="wikilink" href="/Wiki-Link/">Wiki Link</a> of some sorts.</p>
````



## steroids.kbd

The `steroids.kbd` extension converts syntax for user keyboard entry: `||Cmd+K||` into `<kbd>Cmd+K</kbd>`.

### Installation

```bash
pip install --user --upgrade git+https://github.com/twardoch/markdown-steroids.git
```

### Docs

* https://github.com/twardoch/markdown-steroids

### Options

```yaml
  steroids.kbd:
    repl_mac       : false                # Replace macOS symbols
    html_class     : 'kbd'                # CSS hook. Leave blank for none
```

### Example

---

||Cmd+K||

---

#### Input Markdown

````markdown
||Cmd+K||
````

#### Output HTML

````html
<kbd class="kbd">Cmd+K</kbd>
````


## steroids.replimgsrc

The `steroids.replimgsrc` extension finds and replaces portions of an image URL. 

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

````markdown
````

#### Output HTML

````html
````


## steroids.absimgsrc

The `steroids.absimgsrc` replaces relative image URLs with absolute ones. 

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



# Installation

```
pip install --user --upgrade  git+https://github.com/twardoch/markdown-steroids.git
```



## Usage in MkDocs

In your `mkdocs.yaml` include:

```yaml
steroids.wikilinks
markdown_extensions:
- steroids.kbd:
    repl_mac       : false                # Replace macOS symbols
    html_class     : 'kbd'                # CSS hook. Leave blank for none
- steroids.replimgsrc: 
    find           : 'https://github.com/repo/blob/master/images/'
    replace        : '../img/'
- steroids.absimgsrc: 
    base_url       : 'https://github.com/repo/blob/master/images/' 
    # Base URL to which the relative paths will be appended
```

### Copyright and License

* Copyright © 2016 [Adam Twardoch](https://github.com/twardoch)
* Copyright © 2008 [Waylan Limberg](http://achinghead.com) 
* Copyright © 2008-2014 The Python Markdown Project
* Copyright © 2014-2015 Isaac Muse <isaacmuse@gmail.com> 
* License: [BSD 3-Clause License](./LICENSE)

### Projects related to Markdown and MkDocs by Adam Twardoch: 

* [https://twardoch.github.io/markdown-rundown/](https://twardoch.github.io/markdown-rundown/) — summary of Markdown formatting styles [git](https://github.com/twardoch/markdown-rundown)
* [https://twardoch.github.io/markdown-steroids/](https://twardoch.github.io/markdown-steroids/) — Some extensions for Python Markdown [git](https://github.com/twardoch/markdown-steroids)
* [https://twardoch.github.io/markdown-utils/](https://twardoch.github.io/markdown-utils/) — various utilities for working with Markdown-based documents [git](https://github.com/twardoch/markdown-utils)
* [https://twardoch.github.io/mkdocs-combine/](https://twardoch.github.io/mkdocs-combine/) — convert an MkDocs Markdown source site to a single Markdown document [git](https://github.com/twardoch/mkdocs-combine)
* [https://github.com/twardoch/noto-mkdocs-theme/tree/rework](https://github.com/twardoch/noto-mkdocs-theme/tree/rework) — great Material Design-inspired theme for MkDocs [git](https://github.com/twardoch/noto-mkdocs-theme)
* [https://twardoch.github.io/clinker-mktheme/](https://twardoch.github.io/clinker-mktheme/) — great theme for MkDocs [git](https://github.com/twardoch/clinker-mktheme)
