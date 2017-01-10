# mdx_steroids

A small collection of Python Markdown extensions


## [mdx_steroids.figcaption](mdx_steroids/figcaption.py)

Extension for [Python-Markdown](https://pypi.python.org/pypi/Markdown) to parse images with captions inside a figure element.

Markdown:

```markdown
    ![](http://lorempixel.com/350/150/)
    :   Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Praesent at consequat magna, faucibus ornare eros. Nam et
        mattis urna. Cras sodales, massa id gravida
```

Output:

```html
    <figure>
        <img alt="" src="http://lorempixel.com/350/150/" />
        <figcaption>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Praesent at consequat magna, faucibus ornare eros. Nam et
            mattis urna. Cras sodales, massa id gravida</p>
        </figcaption>
    </figure>
```


## [mdx_steroids.kbd](mdx_steroids/kbd.py)

Extension for [Python-Markdown](https://pypi.python.org/pypi/Markdown) to convert syntax for user keyboard entry: `||Cmd+K||` into `<kbd>Cmd+K</kbd>`. 


## [mdx_steroids.wikilink](mdx_steroids/wikilink.py)

Extension for [Python-Markdown](https://pypi.python.org/pypi/Markdown) to parse wikilinks in the style of the  [Gollum](https://github.com/gollum/gollum) wiki and the [Github Wiki system](https://help.github.com/articles/about-github-wikis/). It will convert links such as `[[Page name]]` to `[Page name](Page-name.md)` (it expects the linked files to be in the same folder).

Markdown in Github wiki:
```
The Sketchboard is a good place for working with scanned images. You will find all the details about working with images in the [[Importing artwork]] and [[Bitmap Images]] sections.
```

Output after further processing:
```html
<p>The Sketchboard is a good place for working with scanned images. You will find all the details about working with images in the <a class="wikilink" href="../Importing-artwork/">Importing artwork</a> and <a class="wikilink" href="../Bitmap-Images/">Bitmap Images</a> sections.</p>
```


# Installation

```
pip install --user --upgrade  git+https://github.com/twardoch/markdown-steroids.git
```

# Usage in MkDocs

In your `mkdocs.yaml` include:

```yaml
markdown_extensions:
  - mdx_steroidsfigcaption
  - mdx_steroids.wikilink
  - mdx_steroids.kbd
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
