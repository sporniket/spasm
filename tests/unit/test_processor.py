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

from spasm.pp.processor import StatementLine, StatementLineParser, StatementLineRenderer


######################################################## Test suite for StatementLine


def test_that__StatementLine__properties_work():
    statement = StatementLine()
    statement.label = "that's"
    statement.mnemonic = "all"
    statement.operands = "folks"
    statement.comment = "end of line"
    assert statement.label == "that's"
    assert statement.mnemonic == "all"
    assert statement.operands == "folks"
    assert statement.comment == "end of line"


def test_that__StatementLine_isCommentOnly__works():
    statement = StatementLine()
    statement.label = ""
    statement.mnemonic = ""
    statement.operands = ""
    statement.comment = "end of line"
    assert statement.isCommentOnly()

    statement.label = "foo"
    assert not statement.isCommentOnly()
    statement.label = None

    statement.mnemonic = "foo"
    assert not statement.isCommentOnly()
    statement.mnemonic = None

    statement.operands = "foo"
    assert not statement.isCommentOnly()
    statement.operands = None


######################################################## Test suite for StatementLineRenderer


def test_that__StatementLineRenderer_render__works():
    statement = StatementLine()
    statement.label = "that's"
    statement.mnemonic = "all"
    statement.operands = "folks"
    statement.comment = "end of line"
    assert (
        StatementLineRenderer().render(statement)
        == "                      that's: all folks            ; end of line"
    )


def test_that__StatementLineRenderer_render__supports_comment_only_statement():
    statement = StatementLine()
    statement.label = None
    statement.mnemonic = None
    statement.operands = None
    statement.comment = "just a comment"
    renderer = StatementLineRenderer()
    assert (
        renderer.render(statement) == "                              ; just a comment"
    )
    renderer.denyCommentBlock()
    assert (
        renderer.render(statement)
        == "                                                   ; just a comment"
    )


######################################################## Test suite for StatementLineParser


def test_that__StatementLineParser_parse__captures_last_position_comment():
    statement = StatementLineParser().parse(
        "aShortLabel operation operand1,operand2 comment"
    )
    assert statement.label == "aShortLabel"
    assert statement.mnemonic == "operation"
    assert statement.operands == "operand1,operand2"
    assert statement.comment == "comment"


def test_that__StatementLineParser_parse__captures_last_position_operand():
    statement = StatementLineParser().parse("aShortLabel operation operand1,operand2")
    assert statement.label == "aShortLabel"
    assert statement.mnemonic == "operation"
    assert statement.operands == "operand1,operand2"
    assert statement.comment == ""


def test_that__StatementLineParser__parse_captures_last_position_mnemonic():
    statement = StatementLineParser().parse("aShortLabel operation")
    assert statement.label == "aShortLabel"
    assert statement.mnemonic == "operation"
    assert statement.operands == ""
    assert statement.comment == ""


def test_that__StatementLineParser_parse__captures_last_position_label():
    statement = StatementLineParser().parse("aShortLabel")
    assert statement.label == "aShortLabel"
    assert statement.mnemonic == ""
    assert statement.operands == ""
    assert statement.comment == ""


def test_that__StatementLineParser_parse__supports_comment_only_statement():
    statement = StatementLineParser().parse(" ; just a semi-colon comment")
    assert statement.label == ""
    assert statement.mnemonic == ""
    assert statement.operands == ""
    assert statement.comment == "just a semi-colon comment"

    statement = StatementLineParser().parse(" * just a star comment")
    assert statement.label == ""
    assert statement.mnemonic == ""
    assert statement.operands == ""
    assert statement.comment == "just a star comment"


def test_that__StatementLineParser_parse__ignore_spaces_in_string_operands():
    """Bug report #4"""
    statement = StatementLineParser().parse(
        'messThatsAll            dc.b                    "Done, press any key to quit.",0'
    )
    assert statement.label == "messThatsAll"
    assert statement.mnemonic == "dc.b"
    assert statement.operands == '"Done, press any key to quit.",0'
    assert statement.comment == ""
