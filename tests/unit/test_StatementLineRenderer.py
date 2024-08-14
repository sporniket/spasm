"""
---
(c) 2024 David SPORN
---
This is part of SPASM -- Sporniket's toolbox for assembly language.

SPASM is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

SPASM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with SPASM.
If not, see <https://www.gnu.org/licenses/>. 
---
"""

from spasm.pp.stylesheet.builtin import SPORNIKET, HERITAGE
from spasm.pp.statement_line import StatementLine, StatementLineRenderer


def test_that__StatementLineRenderer_render__works():
    statement = StatementLine()
    statement.label = "that's"
    statement.mnemonic = "all"
    statement.operands = "folks"
    statement.comment = "end of line"
    assert (
        StatementLineRenderer().render(statement, SPORNIKET)
        == "                      that's: all folks           ; end of line"
    )
    assert (
        StatementLineRenderer().render(statement, HERITAGE)
        == "that's          all     folks   ; end of line"
    )


def test_that__StatementLineRenderer_render__supports_comment_only_statement():
    statement = StatementLine()
    statement.label = None
    statement.mnemonic = None
    statement.operands = None
    statement.comment = "just a comment"
    renderer = StatementLineRenderer()
    assert (
        renderer.render(statement, SPORNIKET)
        == "                              ; just a comment"
    )
    renderer.denyCommentBlock()
    assert (
        renderer.render(statement, SPORNIKET)
        == "                                                  ; just a comment"
    )


def test_that_StatementLineRenderer_renderLineBody__supports_long_operands():
    statement = StatementLine()
    statement.label = None
    statement.mnemonic = "line"
    statement.operands = "very,long,long,long,long,long,long,long,long,long,long"
    statement.comment = None
    renderer = StatementLineRenderer()
    assert (
        renderer.renderLineBody(statement, HERITAGE, 16, 16)
        == "line    very,long,long,long,long,long,long,long,long,long,long"
    )


def test_that_StatementLineRenderer_renderLineBody__pads_short_operations():
    statement = StatementLine()
    statement.label = None
    statement.mnemonic = "all"
    statement.operands = "folks"
    statement.comment = None
    renderer = StatementLineRenderer()
    assert (
        renderer.renderLineBody(statement, SPORNIKET, 30, 1) == "all folks           "
    )
