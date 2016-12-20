# mdx_steroids

A small collection of Python Markdown extensions

## mdx_steroids.mdx_figcaption

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

## mdx_steroids.mdx_wikilink

Extension for [Python-Markdown](https://pypi.python.org/pypi/Markdown) to parse wikilinks in the style of the  [Gollum](https://github.com/gollum/gollum) wiki and the [Github Wiki system](https://help.github.com/articles/about-github-wikis/). It will convert links such as `[[Page name]]` to `[Page name](Page-name.md)` (it expects the linked files to be in the same folder).

Markdown in Github wiki:
```
The Sketchboard is a good place for working with scanned images. You will find all the details about working with images in the [[Importing artwork]] and [[Bitmap Images]] sections.
```

Output after further processing:
```html
<p>The Sketchboard is a good place for working with scanned images. You will find all the details about working with images in the <a class="wikilink" href="../Importing-artwork/">Importing artwork</a> and <a class="wikilink" href="../Bitmap-Images/">Bitmap Images</a> sections.</p>
```

## mdx_steroids.mdx_kbd

Extension for [Python-Markdown](https://pypi.python.org/pypi/Markdown) to convert syntax for user keyboard entry: `||Cmd+K||` into `<kbd>Cmd+K</kbd>`. 

# Installation

```
pip install --user --upgrade  git+https://github.com/twardoch/markdown-steroids.git
```

# Usage in MkDocs

In your `mkdocs.yaml` include:

```yaml
markdown_extensions:
  - mdx_steroids.mdx_figcaption
  - mdx_steroids.mdx_wikilink
  - mdx_steroids.mdx_kbd
```

### License

* Copyright © 2016 by [Adam Twardoch](https://github.com/twardoch)
* Licensed under the BSD 3-Clause License.
