"""
    pygments.lexers.scdoc
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for scdoc, a simple man page generator.

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer
from pygments.lexer import bygroups
from pygments.lexer import include
from pygments.lexer import this
from pygments.lexer import using
from pygments.token import Comment
from pygments.token import Generic
from pygments.token import Keyword
from pygments.token import String
from pygments.token import Text

__all__ = ['ScdocLexer']


class ScdocLexer(RegexLexer):
    """
    `scdoc` is a simple man page generator for POSIX systems written in C99.
    https://git.sr.ht/~sircmpwn/scdoc

    .. versionadded:: 2.5
    """
    name = 'scdoc'
    aliases = ['scdoc', 'scd']
    filenames = ['*.scd', '*.scdoc']
    flags = re.MULTILINE

    tokens = {
        'root': [
            # comment
            (r'^(;.+\n)', bygroups(Comment)),

            # heading with pound prefix
            (r'^(#)([^#].+\n)', bygroups(Generic.Heading, Text)),
            (r'^(#{2})(.+\n)', bygroups(Generic.Subheading, Text)),
            # bulleted lists
            (r'^(\s*)([*-])(\s)(.+\n)',
            bygroups(Text, Keyword, Text, using(this, state='inline'))),
            # numbered lists
            (r'^(\s*)(\.+\.)( .+\n)',
            bygroups(Text, Keyword, using(this, state='inline'))),
            # quote
            (r'^(\s*>\s)(.+\n)', bygroups(Keyword, Generic.Emph)),
            # text block
            (r'^(```\n)([\w\W]*?)(^```$)', bygroups(String, Text, String)),

            include('inline'),
        ],
        'inline': [
            # escape
            (r'\\.', Text),
            # underlines
            (r'(\s)(_[^_]+_)(\W|\n)', bygroups(Text, Generic.Emph, Text)),
            # bold
            (r'(\s)(\*[^*]+\*)(\W|\n)', bygroups(Text, Generic.Strong, Text)),
            # inline code
            (r'`[^`]+`', String.Backtick),

            # general text, must come last!
            (r'[^\\\s]+', Text),
            (r'.', Text),
        ],
    }

    def analyse_text(text):
        """This is very similar to markdown, save for the escape characters
        needed for * and _."""
        result = 0

        if '\\*' in text:
            result += 0.01

        if '\\_' in text:
            result += 0.01

        return result
