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

from spasm.pp.statement_line import StatementLine


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
