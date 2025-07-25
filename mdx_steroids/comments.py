#!/usr/bin/env python
# this_file: mdx_steroids/comments.py
"""Comments Extension for Python-Markdown.

This extension removes special HTML comments that start with three dashes (<!---)
from the Markdown output. Standard HTML comments (<!--) are preserved.

This is useful for:
- Adding notes in Markdown source that won't appear in output
- Draft comments and TODOs
- Metadata or instructions for other processors

Based on code © 2015 by ryneeverett (https://github.com/ryneeverett/python-markdown-comments)

## Basic Usage

```python
import markdown

text = '''
This is visible text.
<!--- This comment will be removed -->
<!-- This standard HTML comment remains -->
More visible text.
'''

html = markdown.markdown(text, extensions=['mdx_steroids.comments'])
# Result: The <!--- comment is removed, but <!-- comment remains
```

## Examples

```markdown
# My Document

This paragraph is visible.

<!--- TODO: Add more content here -->

<!--- 
Multi-line comment
that will be removed
from the output
-->

<!-- This HTML comment stays in the output -->
```

"""

import re
from typing import List, Tuple, Any

from markdown import Extension, Markdown
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor

PREFIX_PLACEHOLDER: str = "OMtxTKldR2f1LZ5Q"


class CommentsExtension(Extension):
    """Extension to remove special markdown comments.
    
    This extension processes comments in three stages:
    1. Munge: Replace <!--- with a placeholder to protect from Markdown processing
    2. Remove: Strip out the protected comments
    3. Replace: Restore any remaining placeholders (in code blocks, etc.)
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the extension."""
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        """Register processors with the Markdown instance.
        
        Args:
            md: The Markdown instance to extend
        """
        md.registerExtension(self)
        md.preprocessors.register(CommentMunger(md), "comment_munger", 25)
        md.preprocessors.register(CommentRemover(md), "comment_remover", 15)
        md.postprocessors.register(
            RawCommentReplacer(md), "raw_comment_replacer", 5
        )


class CommentMunger(Preprocessor):
    """Replace markdown comment markers with placeholders.
    
    This protects them from being processed as regular HTML.
    """
    
    def run(self, lines: List[str]) -> List[str]:
        """Replace <!--- with placeholder in all lines.
        
        Args:
            lines: The lines of source text
            
        Returns:
            Lines with comment markers replaced
        """
        return [re.sub(r"<!---", PREFIX_PLACEHOLDER, line) for line in lines]


class CommentRemover(Preprocessor):
    """Remove markdown comments from the source.
    
    Handles both inline and multi-line comments.
    """
    
    def run(self, lines: List[str]) -> List[str]:
        """Process all lines to remove comments.
        
        Args:
            lines: The lines of source text
            
        Returns:
            Lines with comments removed
        """
        new_lines: List[str] = []
        is_multi: bool = False
        
        for line in lines:
            if not is_multi:
                new_line, is_multi = self._uncommenter(line)
            else:
                new_line, is_multi = self._unmultiliner(line)
            new_lines.append(new_line)
        return new_lines

    def _uncommenter(self, line: str) -> Tuple[str, bool]:
        """Remove inline comments and detect multi-line comment starts.
        
        Args:
            line: A single line of text
            
        Returns:
            Tuple of (processed line, whether multi-line comment started)
        """
        # Remove complete inline comments
        line = re.sub(r"\s*" + PREFIX_PLACEHOLDER + r".*?-->", "", line)

        # Check for start of multiline comment
        line, count = re.subn(r"\s*" + PREFIX_PLACEHOLDER + r".*", "", line)

        return line, bool(count)

    def _unmultiliner(self, line: str) -> Tuple[str, bool]:
        """Process lines within a multi-line comment.
        
        Args:
            line: A line within a multi-line comment
            
        Returns:
            Tuple of (processed line, whether still in multi-line comment)
        """
        new_line, count = re.subn(r".*?-->", "", line, count=1)

        # Check if this line ends the multiline comment
        if count > 0:
            # Process remainder of line for new comments
            return self._uncommenter(new_line)
        else:
            # Still inside multiline comment
            return ("", True)


class RawCommentReplacer(Postprocessor):
    """Restore protected comment markers in the final output.
    
    This handles cases where comment markers appear in code blocks
    and should be preserved in the output.
    """
    
    def run(self, text: str) -> str:
        """Replace placeholders with original comment markers.
        
        Args:
            text: The processed HTML text
            
        Returns:
            Text with placeholders replaced
        """
        return re.sub(PREFIX_PLACEHOLDER, "<!---", text)


def makeExtension(*args: Any, **kwargs: Any) -> CommentsExtension:
    """Create and return an instance of the CommentsExtension.
    
    This is the entry point for Markdown to load the extension.
    
    Args:
        *args: Positional arguments for the extension
        **kwargs: Keyword arguments for the extension
        
    Returns:
        An instance of CommentsExtension
    """
    return CommentsExtension(*args, **kwargs)