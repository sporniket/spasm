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

from spasm.parsers import StatementLineParserListener
from .model import StatementLine


class StatementLineBuilderOnParse(StatementLineParserListener):
    """Builtin implementation of StatementLineParserEventListener that emit a StatementLine at the end."""

    def onStartOfLine(self, sourceLine: str):
        self._currentLineContent = sourceLine
        self._wipStatement = StatementLine()

    def onLabel(self, start: int, end: int):
        self._wipStatement.label = self._currentLineContent[start:end]

    def onMnemonic(self, start: int, end: int):
        self._wipStatement.mnemonic = self._currentLineContent[start:end]

    def onOperands(self, start: int, end: int):
        self._wipStatement.operands = self._currentLineContent[start:end]

    def onComment(self, start: int, end: int):
        self._wipStatement.comment = self._currentLineContent[start:end]

    def onEndOfLine(self) -> any:
        """Processing is done, returns a StatementLine.

        Returns:
            any: a fully completed StatementLine.
        """
        self._currentLineContent = None
        return self._wipStatement
