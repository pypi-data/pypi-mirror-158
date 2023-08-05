"""
    pygments.styles.xcode
    ~~~~~~~~~~~~~~~~~~~~~

    Style similar to the `Xcode` default theme.

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.style import Style
from pygments.token import Comment
from pygments.token import Error
from pygments.token import Keyword
from pygments.token import Literal
from pygments.token import Name
from pygments.token import Number
from pygments.token import Operator
from pygments.token import String


class XcodeStyle(Style):
    """
    Style similar to the Xcode default colouring theme.
    """

    default_style = ''

    styles = {
        Comment:                '#177500',
        Comment.Preproc:        '#633820',

        String:                 '#C41A16',
        String.Char:            '#2300CE',

        Operator:               '#000000',

        Keyword:                '#A90D91',

        Name:                   '#000000',
        Name.Attribute:         '#836C28',
        Name.Class:             '#3F6E75',
        Name.Function:          '#000000',
        Name.Builtin:           '#A90D91',
        # In Obj-C code this token is used to colour Cocoa types
        Name.Builtin.Pseudo:    '#5B269A',
        Name.Variable:          '#000000',
        Name.Tag:               '#000000',
        Name.Decorator:         '#000000',
        # Workaround for a BUG here: lexer treats multiline method signatres as labels
        Name.Label:             '#000000',

        Literal:                '#1C01CE',
        Number:                 '#1C01CE',
        Error:                  '#000000',
    }
