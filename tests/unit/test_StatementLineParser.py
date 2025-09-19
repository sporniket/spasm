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

import pytest
from spasm.parsers import StatementLineParser
from spasm.pp.statement_line import StatementLineBuilderOnParse


def buildParser():
    parser = StatementLineParser()
    parser.listener = StatementLineBuilderOnParse()
    return parser


def test_that__StatementLineParser_requires_listener():
    with pytest.raises(ValueError) as verr:
        StatementLineParser().parse("whatever")
    assert "no.listener" in str(verr)


def test_that__StatementLineParser_parse__captures_last_position_comment():
    statement = buildParser().parse("aShortLabel operation operand1,operand2 comment")
    assert statement.label == "aShortLabel"
    assert statement.mnemonic == "operation"
    assert statement.operands == "operand1,operand2"
    assert statement.comment == "comment"


def test_that__StatementLineParser_parse__captures_last_position_operand():
    statement = buildParser().parse("aShortLabel operation operand1,operand2")
    assert statement.label == "aShortLabel"
    assert statement.mnemonic == "operation"
    assert statement.operands == "operand1,operand2"
    assert statement.comment == ""


def test_that__StatementLineParser__parse_captures_last_position_mnemonic():
    statement = buildParser().parse("aShortLabel operation")
    assert statement.label == "aShortLabel"
    assert statement.mnemonic == "operation"
    assert statement.operands == ""
    assert statement.comment == ""


def test_that__StatementLineParser_parse__captures_last_position_label():
    statement = buildParser().parse("aShortLabel")
    assert statement.label == "aShortLabel"
    assert statement.mnemonic == ""
    assert statement.operands == ""
    assert statement.comment == ""


def test_that__StatementLineParser_parse__supports_comment_only_statement():
    # semi-colon comment line
    # -- with some white spaces before
    statement = buildParser().parse(" ; just a semi-colon comment")
    assert statement.label == ""
    assert statement.mnemonic == ""
    assert statement.operands == ""
    assert statement.comment == "just a semi-colon comment"

    # -- immediately start comment
    statement = buildParser().parse("; just a semi-colon comment")
    assert statement.label == ""
    assert statement.mnemonic == ""
    assert statement.operands == ""
    assert statement.comment == "just a semi-colon comment"

    # star comment line
    # -- with some white spaces before
    statement = buildParser().parse(" * just a star comment")
    assert statement.label == ""
    assert statement.mnemonic == ""
    assert statement.operands == ""
    assert statement.comment == "just a star comment"

    # -- immediately start comment
    statement = buildParser().parse("* just a star comment")
    assert statement.label == ""
    assert statement.mnemonic == ""
    assert statement.operands == ""
    assert statement.comment == "just a star comment"


def test_that__StatementLineParser_parse__ignore_spaces_in_string_operands():
    """Bug report #4"""
    statement = buildParser().parse(
        'messThatsAll            dc.b                    "Done, press any key to quit.",0',
    )
    assert statement.label == "messThatsAll"
    assert statement.mnemonic == "dc.b"
    assert statement.operands == '"Done, press any key to quit.",0'
    assert statement.comment == ""
