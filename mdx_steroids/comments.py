#!/usr/bin/env python
"""
# mdx_steroids.comments

The `mdx_steroids.comments` ignores HTML comments opened by three dashes and 
any whitespace prior to them. I believe pandoc has similar functionality.

Based on code © 2015 by ryneeverett (https://github.com/ryneeverett/python-markdown-comments)

```html
<!-- This is a standard html comment which will remain in the output. -->
<!--- This is a markdown comment which this extension removes. -->
```

Installation
------------

```sh
pip install git+https://github.com/ryneeverett/python-markdown-comments.git
```

Example
-------
```python
>>> import markdown
>>> import mkdcomments
>>> comments = mkdcomments.CommentsExtension()
>>> markdowner = markdown.Markdown(extensions=[comments])
>>> markdowner.convert(\"\"\"\
... blah blah blah  <!--- inline comment -->
...
... <!---multiline comment
... multiline comment
... multiline comment-->
...
... even more text.\"\"\")
u'<p>blah blah blah</p>\n<p>even more text.</p>'
```

Infrequently Asked Questions
----------------------------

### How can I write about markdown comments without them being removed?

In order to render markdown comments, you must *(a)*use them in an html block (which are not processed as markdown) and *(b)*escape the brackets so the browser won't think they're html comments. E.g.:

```html
<pre>
&lt;!--- meta markdown comment --&gt;
</pre>
```

"""

import re

from markdown import Extension
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor

PREFIX_PLACEHOLDER = "OMtxTKldR2f1LZ5Q"


class CommentsExtension(Extension):
    def __init__(self, *args, **kwargs):
        """Initialize."""
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.preprocessors.add("comment_munger", CommentMunger(md), "<html_block")
        md.preprocessors.add("comment_remover", CommentRemover(md), ">html_block")
        md.postprocessors.add(
            "raw_comment_replacer", RawCommentReplacer(md), ">raw_html"
        )


class CommentMunger(Preprocessor):
    def run(self, lines):
        return [re.sub(r"<!---", PREFIX_PLACEHOLDER, line) for line in lines]


class CommentRemover(Preprocessor):
    def run(self, lines):
        new_lines = []
        is_multi = False
        for line in lines:
            if not is_multi:
                new_line, is_multi = self._uncommenter(line)
            else:
                new_line, is_multi = self._unmultiliner(line)
            new_lines.append(new_line)
        return new_lines

    def _uncommenter(self, line):
        # inline
        line = re.sub(r"\s*" + PREFIX_PLACEHOLDER + r".*?-->", "", line)

        # start multiline
        line, count = re.subn(r"\s*" + PREFIX_PLACEHOLDER + r".*", "", line)

        return line, bool(count)

    def _unmultiliner(self, line):
        new_line, count = re.subn(r".*?-->", "", line, count=1)

        # end multiline
        if count > 0:
            return self._uncommenter(new_line)

        # continue multiline
        else:
            return ("", True)


class RawCommentReplacer(Postprocessor):
    def run(self, text):
        return re.sub(PREFIX_PLACEHOLDER, "<!---", text)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return CommentsExtension(*args, **kwargs)
